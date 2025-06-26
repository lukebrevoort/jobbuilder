#!/usr/bin/env python3
"""
Quick test script to verify the JobBuilder setup and basic functionality
"""

import sys
import os
import json
import asyncio
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.job import JobData
from app.services.ai_service import AIService
from app.services.template_service import TemplateService
from app.services.pdf_service import PDFService
from app.services.notion_service import NotionService

async def test_basic_functionality():
    """Test basic functionality of all services"""
    print("🚀 Testing JobBuilder functionality...\n")
    
    # Test data
    test_job = JobData(
        job_title="Senior Python Developer",
        company_name="Tech Innovations Inc.",
        job_description="""
        We are seeking a Senior Python Developer to join our growing team. 
        The ideal candidate will have experience with Python, FastAPI, PostgreSQL, 
        and cloud technologies like AWS. You will be responsible for building 
        scalable web applications and APIs that serve millions of users.
        
        Requirements:
        - 5+ years of Python development experience
        - Experience with FastAPI or similar web frameworks
        - Knowledge of PostgreSQL and database design
        - AWS experience preferred
        - Strong problem-solving skills
        """,
        notion_page_id="test-page-id"
    )
    
    print(f"📋 Test Job: {test_job.job_title} at {test_job.company_name}")
    
    # Test AI Service
    print("\n🤖 Testing AI Service...")
    ai_service = AIService()
    print(f"   ✓ AI Service healthy: {ai_service.is_healthy()}")
    
    try:
        cover_letter = await ai_service.generate_cover_letter(test_job)
        print(f"   ✓ Cover letter generated ({len(cover_letter)} characters)")
        
        resume_data = await ai_service.customize_resume(test_job)
        print(f"   ✓ Resume customized ({len(resume_data.get('skills', []))} skills)")
    except Exception as e:
        print(f"   ✗ AI Service error: {str(e)}")
    
    # Test Template Service
    print("\n📄 Testing Template Service...")
    template_service = TemplateService()
    
    try:
        # Load personal info for template data
        with open('data/personal_info.json', 'r') as f:
            personal_info = json.load(f)
        
        template_data = {
            'personal_info': personal_info,
            'job_data': test_job,
            'date': datetime.now().strftime("%B %d, %Y"),
            'relevant_skills': ['Python', 'FastAPI', 'PostgreSQL', 'AWS'],
            'matching_skills': ['Python', 'FastAPI', 'AWS'],
            'key_qualifications': [
                '5+ years of Python development experience',
                'Strong experience with web frameworks',
                'Cloud platform expertise'
            ],
            'company_connection': f"I am particularly excited about {test_job.company_name}'s innovative approach to technology.",
            'job_highlights': 'building scalable applications that serve millions of users'
        }
        
        cover_letter_rendered = template_service.render_cover_letter(template_data)
        print(f"   ✓ Cover letter template rendered ({len(cover_letter_rendered)} characters)")
        
    except Exception as e:
        print(f"   ✗ Template Service error: {str(e)}")
    
    # Test PDF Service
    print("\n📑 Testing PDF Service...")
    pdf_service = PDFService()
    print(f"   ✓ PDF Service healthy: {pdf_service.is_healthy()}")
    
    try:
        # Create output directory
        os.makedirs('output', exist_ok=True)
        
        # Test simple PDF creation
        test_content = f"""Test Cover Letter
        
Dear Hiring Manager,

This is a test cover letter for the {test_job.job_title} position at {test_job.company_name}.

Best regards,
Test User"""
        
        pdf_service.create_simple_document(
            test_content, 
            'output/test_cover_letter.pdf', 
            'Test Cover Letter'
        )
        print("   ✓ Test PDF created successfully")
        
    except Exception as e:
        print(f"   ✗ PDF Service error: {str(e)}")
    
    # Test Notion Service (will show warning if not configured)
    print("\n📝 Testing Notion Service...")
    notion_service = NotionService()
    print(f"   ✓ Notion Service healthy: {notion_service.is_healthy()}")
    
    if not notion_service.is_healthy():
        print("   ⚠️  Notion service not configured - this is expected for initial setup")
    
    print("\n✅ Basic functionality test completed!")
    print("\n📋 Next Steps:")
    print("1. Update data/personal_info.json with your information")
    print("2. Update data/base_resume.json with your resume data")
    print("3. Set up Notion integration by updating .env file")
    print("4. Install dependencies: pip install -r requirements.txt")
    print("5. Run the server: uvicorn app.main:app --reload")

if __name__ == "__main__":
    asyncio.run(test_basic_functionality())
