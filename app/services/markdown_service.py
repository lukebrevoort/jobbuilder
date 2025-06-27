import logging
from datetime import datetime
from typing import Dict, Any

from ..models.job import JobData

logger = logging.getLogger(__name__)

class MarkdownService:
    """Service for generating markdown-formatted documents"""
    
    def __init__(self):
        pass
    
    def is_healthy(self) -> bool:
        """Check if markdown service is working"""
        try:
            return True
        except Exception as e:
            logger.error(f"Markdown service health check failed: {str(e)}")
            return False
    
    def create_cover_letter_markdown(self, cover_letter_text: str, job_data: JobData) -> str:
        """Create a markdown-formatted cover letter"""
        try:
            # Add date header
            date_text = datetime.now().strftime("%B %d, %Y")
            
            # Format the cover letter with proper markdown structure
            markdown_content = f"""# Cover Letter

**Date:** {date_text}  
**Position:** {job_data.job_title}  
**Company:** {job_data.company_name}

---

{self._format_cover_letter_content(cover_letter_text)}

---

*Generated automatically by JobBuilder*
"""
            
            logger.info(f"Cover letter markdown created for {job_data.company_name}")
            return markdown_content
            
        except Exception as e:
            logger.error(f"Error creating cover letter markdown: {str(e)}")
            raise Exception(f"Failed to create cover letter markdown: {str(e)}")
    
    def create_resume_markdown(self, resume_data: Dict[str, Any], job_data: JobData) -> str:
        """Create a markdown-formatted resume"""
        try:
            personal_info = resume_data.get('personal_info', {})
            
            # Build markdown resume
            markdown_content = []
            
            # Header with name
            name = personal_info.get('full_name', 'Your Name')
            markdown_content.append(f"# {name}")
            markdown_content.append("")
            
            # Contact information
            contact_parts = []
            if personal_info.get('email'):
                contact_parts.append(f"📧 {personal_info['email']}")
            if personal_info.get('phone'):
                contact_parts.append(f"📞 {personal_info['phone']}")
            if personal_info.get('address'):
                contact_parts.append(f"📍 {personal_info['address']}")
            
            if contact_parts:
                markdown_content.append(" | ".join(contact_parts))
                markdown_content.append("")
            
            # Professional links
            links = []
            if personal_info.get('linkedin_url'):
                links.append(f"[LinkedIn]({personal_info['linkedin_url']})")
            if personal_info.get('github_url'):
                links.append(f"[GitHub]({personal_info['github_url']})")
            
            if links:
                markdown_content.append(" | ".join(links))
                markdown_content.append("")
            
            markdown_content.append("---")
            markdown_content.append("")
            
            # Professional Summary
            if personal_info.get('professional_summary'):
                markdown_content.append("## Professional Summary")
                markdown_content.append("")
                markdown_content.append(personal_info['professional_summary'])
                markdown_content.append("")
            
            # Technical Skills
            skills = resume_data.get('skills', [])
            if skills:
                markdown_content.append("## Technical Skills")
                markdown_content.append("")
                # Group skills in a nice format
                skills_line = " • ".join(skills)
                markdown_content.append(skills_line)
                markdown_content.append("")
            
            # Professional Experience
            experience = resume_data.get('experience', [])
            if experience:
                markdown_content.append("## Professional Experience")
                markdown_content.append("")
                
                for exp in experience:
                    # Job title and company
                    title = exp.get('title', 'Job Title')
                    company = exp.get('company', 'Company Name')
                    markdown_content.append(f"### {title} | {company}")
                    
                    # Location and dates
                    location = exp.get('location', '')
                    start_date = exp.get('start_date', '')
                    end_date = exp.get('end_date', '')
                    if location or start_date or end_date:
                        date_location = f"*{location} | {start_date} - {end_date}*"
                        markdown_content.append(date_location)
                    markdown_content.append("")
                    
                    # Description
                    if exp.get('description'):
                        markdown_content.append(exp['description'])
                        markdown_content.append("")
                    
                    # Achievements
                    if exp.get('achievements'):
                        markdown_content.append("**Key Achievements:**")
                        for achievement in exp['achievements']:
                            markdown_content.append(f"- {achievement}")
                        markdown_content.append("")
            
            # Education
            education = resume_data.get('education', [])
            if education:
                markdown_content.append("## Education")
                markdown_content.append("")
                
                for edu in education:
                    degree = edu.get('degree', 'Degree')
                    school = edu.get('school', 'School Name')
                    markdown_content.append(f"### {degree}")
                    markdown_content.append(f"**{school}**")
                    
                    details = []
                    if edu.get('location'):
                        details.append(edu['location'])
                    if edu.get('graduation_date'):
                        details.append(f"Graduated: {edu['graduation_date']}")
                    if edu.get('gpa'):
                        details.append(f"GPA: {edu['gpa']}")
                    
                    if details:
                        markdown_content.append(f"*{' | '.join(details)}*")
                    markdown_content.append("")
            
            # Projects
            projects = resume_data.get('projects', [])
            if projects:
                markdown_content.append("## Projects")
                markdown_content.append("")
                
                for project in projects:
                    name = project.get('name', 'Project Name')
                    markdown_content.append(f"### {name}")
                    
                    if project.get('description'):
                        markdown_content.append(project['description'])
                        markdown_content.append("")
                    
                    if project.get('technologies'):
                        tech_text = f"**Technologies:** {', '.join(project['technologies'])}"
                        markdown_content.append(tech_text)
                    
                    if project.get('url'):
                        markdown_content.append(f"**Link:** [{project['url']}]({project['url']})")
                    
                    markdown_content.append("")
            
            # Certifications
            certifications = resume_data.get('certifications', [])
            if certifications:
                markdown_content.append("## Certifications")
                markdown_content.append("")
                
                for cert in certifications:
                    cert_name = cert.get('name', 'Certification')
                    cert_line = f"- **{cert_name}**"
                    
                    if cert.get('issuer'):
                        cert_line += f" - {cert['issuer']}"
                    if cert.get('date'):
                        cert_line += f" ({cert['date']})"
                    
                    markdown_content.append(cert_line)
                markdown_content.append("")
            
            # Footer
            markdown_content.append("---")
            markdown_content.append(f"*Resume customized for {job_data.job_title} at {job_data.company_name}*")
            markdown_content.append(f"*Generated on {datetime.now().strftime('%B %d, %Y')}*")
            
            result = "\n".join(markdown_content)
            logger.info(f"Resume markdown created for {job_data.company_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error creating resume markdown: {str(e)}")
            raise Exception(f"Failed to create resume markdown: {str(e)}")
    
    def _format_cover_letter_content(self, cover_letter_text: str) -> str:
        """Format cover letter content with proper markdown structure"""
        # Split into paragraphs and format nicely
        paragraphs = [p.strip() for p in cover_letter_text.split('\n\n') if p.strip()]
        
        formatted_paragraphs = []
        for paragraph in paragraphs:
            # Clean up line breaks within paragraphs
            clean_paragraph = paragraph.replace('\n', ' ').strip()
            formatted_paragraphs.append(clean_paragraph)
        
        return "\n\n".join(formatted_paragraphs)
