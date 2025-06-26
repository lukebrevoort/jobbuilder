from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import logging

from .models.job import JobData, WebhookPayload
from .services.notion_service import NotionService  
from .services.ai_service import AIService
from .services.template_service import TemplateService
from .services.pdf_service import PDFService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="JobBuilder API",
    description="Automated job application generation system",
    version="1.0.0"
)

# Initialize services
notion_service = NotionService()
ai_service = AIService()
template_service = TemplateService()
pdf_service = PDFService()

# Create output directory if it doesn't exist
os.makedirs(os.getenv("OUTPUT_DIR", "./output"), exist_ok=True)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "JobBuilder API is running",
        "timestamp": datetime.now().isoformat(),
        "status": "healthy"
    }

@app.post("/webhook/notion")
async def notion_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Webhook endpoint for Notion database updates
    Processes job postings and generates application materials
    """
    try:
        # Get raw payload
        payload = await request.json()
        logger.info(f"Received webhook from Notion")
        logger.info(f"Payload keys: {list(payload.keys())}")
        
        # Validate webhook (basic validation for now)
        if not payload:
            raise HTTPException(status_code=400, detail="Empty payload")
        
        # Quick validation of payload structure
        page_data = payload.get("data", payload)
        if not page_data.get("properties"):
            logger.warning("No properties found in payload")
            return {"status": "ignored", "message": "No properties in payload"}
        
        # Process the job application in background
        background_tasks.add_task(process_job_application, payload)
        
        return {"status": "accepted", "message": "Job application processing started"}
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in webhook payload: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")

async def process_job_application(payload: dict):
    """
    Background task to process job application
    """
    try:
        logger.info("Starting job application processing...")
        
        # Extract job data from Notion payload
        job_data = extract_job_data_from_payload(payload)
        
        if not job_data:
            logger.warning("No valid job data found in payload")
            return
        
        logger.info(f"Processing job: {job_data.job_title} at {job_data.company_name}")
        
        # Generate cover letter
        logger.info("Generating cover letter...")
        cover_letter = await ai_service.generate_cover_letter(job_data)
        
        # Generate customized resume
        logger.info("Customizing resume...")
        resume_data = await ai_service.customize_resume(job_data)
        
        # Create PDF documents
        logger.info("Creating PDF documents...")
        output_dir = os.getenv("OUTPUT_DIR", "./output")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate cover letter PDF
        cover_letter_path = os.path.join(
            output_dir, 
            f"cover_letter_{job_data.company_name.replace(' ', '_')}_{timestamp}.pdf"
        )
        pdf_service.create_cover_letter_pdf(cover_letter, job_data, cover_letter_path)
        
        # Generate resume PDF
        resume_path = os.path.join(
            output_dir,
            f"resume_{job_data.company_name.replace(' ', '_')}_{timestamp}.pdf"
        )
        pdf_service.create_resume_pdf(resume_data, job_data, resume_path)
        
        # Update Notion with completion status
        await notion_service.update_job_status(
            job_data.notion_page_id,
            status="Generated",
            files=[cover_letter_path, resume_path]
        )
        
        logger.info(f"Job application processing completed for {job_data.company_name}")
        
    except Exception as e:
        logger.error(f"Error processing job application: {str(e)}")
        # Could update Notion with error status here

def extract_job_data_from_payload(payload: dict) -> JobData:
    """
    Extract job data from Notion webhook payload
    Handles both direct page data and automation webhook format
    """
    try:
        # Handle automation webhook format (has 'data' wrapper)
        page_data = payload.get("data", payload)
        
        properties = page_data.get("properties", {})
        notion_page_id = page_data.get("id", "")
        
        logger.info(f"Extracting from page ID: {notion_page_id}")
        logger.info(f"Available properties: {list(properties.keys())}")
        
        job_title = ""
        company_name = ""
        job_description = ""
        
        # Extract job title - handle corrupted JSON
        if "Job Title" in properties:
            title_prop = properties["Job Title"]
            logger.info(f"Job Title property: {title_prop}")
            
            if title_prop.get("type") == "title" and title_prop.get("title"):
                # Handle array of title objects
                title_items = title_prop["title"]
                if title_items and len(title_items) > 0:
                    # Try to get plain_text first, fallback to content
                    first_item = title_items[0]
                    job_title = first_item.get("plain_text") or first_item.get("text", {}).get("content", "")
        
        # Extract company name
        if "Company" in properties:
            company_prop = properties["Company"]
            logger.info(f"Company property: {company_prop}")
            
            if company_prop.get("type") == "rich_text" and company_prop.get("rich_text"):
                rich_text_items = company_prop["rich_text"]
                if rich_text_items and len(rich_text_items) > 0:
                    first_item = rich_text_items[0]
                    company_name = first_item.get("plain_text") or first_item.get("text", {}).get("content", "")
        
        # Extract job description
        if "Job Description" in properties:
            desc_prop = properties["Job Description"]
            logger.info(f"Job Description property type: {desc_prop.get('type')}")
            
            if desc_prop.get("type") == "rich_text" and desc_prop.get("rich_text"):
                rich_text_items = desc_prop["rich_text"]
                if rich_text_items and len(rich_text_items) > 0:
                    # Combine all rich text items
                    description_parts = []
                    for item in rich_text_items:
                        text_content = item.get("plain_text") or item.get("text", {}).get("content", "")
                        if text_content:
                            description_parts.append(text_content)
                    job_description = " ".join(description_parts)
        
        logger.info(f"Extracted - Title: '{job_title}', Company: '{company_name}', Description length: {len(job_description)}")
        
        # Create JobData if we have at least title and company
        if job_title and company_name:
            # Use a default description if none provided
            if not job_description:
                job_description = f"Position: {job_title} at {company_name}"
                logger.warning("No job description found, using default")
            
            return JobData(
                job_title=job_title,
                company_name=company_name,
                job_description=job_description,
                notion_page_id=notion_page_id
            )
        else:
            logger.error(f"Missing required data - Title: '{job_title}', Company: '{company_name}'")
            return None
        
    except Exception as e:
        logger.error(f"Error extracting job data: {str(e)}")
        logger.error(f"Payload structure: {json.dumps(payload, indent=2)[:500]}...")
        return None

@app.get("/jobs/status/{page_id}")
async def get_job_status(page_id: str):
    """Get the status of a job application"""
    try:
        status = await notion_service.get_job_status(page_id)
        return {"page_id": page_id, "status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/{filename}")
async def download_file(filename: str):
    """Download generated files"""
    output_dir = os.getenv("OUTPUT_DIR", "./output")
    file_path = os.path.join(output_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/pdf'
    )

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "notion": notion_service.is_healthy(),
            "ai": ai_service.is_healthy(),
            "pdf": pdf_service.is_healthy()
        },
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        host=os.getenv("APP_HOST", "0.0.0.0"),
        port=int(os.getenv("APP_PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
