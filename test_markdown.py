#!/usr/bin/env python3
"""
Test script for the new markdown functionality
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.models.job import JobData
from app.services.ai_service import AIService
from app.services.markdown_service import MarkdownService

async def test_markdown_generation():
    """Test the markdown generation functionality"""
    
    print("🧪 Testing Markdown Generation...")
    
    # Create test job data
    job_data = JobData(
        notion_page_id="test-page-id",
        job_title="Senior Python Developer",
        company_name="Tech Innovations Inc",
        job_description="""
        We are looking for a Senior Python Developer with expertise in:
        - Python programming and web frameworks like FastAPI
        - Cloud technologies, particularly AWS
        - Database management with SQL
        - API development and integration
        - Git version control
        - Docker containerization
        
        The ideal candidate will have experience building scalable web applications
        and working in an agile development environment.
        """
    )
    
    # Initialize services
    ai_service = AIService()
    markdown_service = MarkdownService()
    
    try:
        print("📝 Generating cover letter...")
        cover_letter = await ai_service.generate_cover_letter(job_data)
        print("✅ Cover letter generated")
        
        print("📋 Customizing resume...")
        resume_data = await ai_service.customize_resume(job_data)
        print("✅ Resume customized")
        
        print("🎨 Creating markdown documents...")
        
        # Generate markdown versions
        cover_letter_markdown = markdown_service.create_cover_letter_markdown(cover_letter, job_data)
        resume_markdown = markdown_service.create_resume_markdown(resume_data, job_data)
        
        # Save to files for inspection
        with open("test_cover_letter.md", "w") as f:
            f.write(cover_letter_markdown)
        
        with open("test_resume.md", "w") as f:
            f.write(resume_markdown)
        
        print("✅ Markdown documents created!")
        print("\n📄 Files generated:")
        print("  - test_cover_letter.md")
        print("  - test_resume.md")
        
        print("\n🎉 Test completed successfully!")
        print("\n📖 You can now view the generated markdown files to see the formatted output.")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Run the test
    asyncio.run(test_markdown_generation())
