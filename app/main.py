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
        logger.info(f"Received webhook payload: {json.dumps(payload, indent=2)}")
        
        # Validate webhook (basic validation for now)
        if not payload:
            raise HTTPException(status_code=400, detail="Empty payload")
        
        # Process the job application in background
        background_tasks.add_task(process_job_application, payload)
        
        return {"status": "accepted", "message": "Job application processing started"}
        
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
    This will need to be customized based on your Notion database structure
    """
    try:
        # This is a simplified extraction - adjust based on your Notion database schema
        properties = payload.get("properties", {})
        
        job_title = ""
        company_name = ""
        job_description = ""
        notion_page_id = payload.get("id", "")
        
        # Extract job title
        if "Job Title" in properties:
            title_prop = properties["Job Title"]
            if title_prop.get("type") == "title" and title_prop.get("title"):
                job_title = title_prop["title"][0]["plain_text"]
        
        # Extract company name
        if "Company" in properties:
            company_prop = properties["Company"]
            if company_prop.get("type") == "rich_text" and company_prop.get("rich_text"):
                company_name = company_prop["rich_text"][0]["plain_text"]
        
        # Extract job description
        if "Job Description" in properties:
            desc_prop = properties["Job Description"]
            if desc_prop.get("type") == "rich_text" and desc_prop.get("rich_text"):
                job_description = desc_prop["rich_text"][0]["plain_text"]
        
        if job_title and company_name and job_description:
            return JobData(
                job_title=job_title,
                company_name=company_name,
                job_description=job_description,
                notion_page_id=notion_page_id
            )
        
        return None
        
    except Exception as e:
        logger.error(f"Error extracting job data: {str(e)}")
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
