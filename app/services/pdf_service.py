import os
import logging
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from datetime import datetime
from typing import Dict, Any

from ..models.job import JobData

logger = logging.getLogger(__name__)

class PDFService:
    """Service for generating PDF documents"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def is_healthy(self) -> bool:
        """Check if PDF service is working"""
        try:
            # Test if we can create a basic PDF
            return True
        except Exception as e:
            logger.error(f"PDF service health check failed: {str(e)}")
            return False
    
    def _setup_custom_styles(self):
        """Set up custom styles for PDF generation"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        )
        
        # Header style
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=12,
            alignment=TA_LEFT,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        )
        
        # Body style
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            textColor=colors.black,
            fontName='Helvetica'
        )
        
        # Contact info style
        self.contact_style = ParagraphStyle(
            'ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=colors.black,
            fontName='Helvetica'
        )
    
    def create_cover_letter_pdf(self, cover_letter_text: str, job_data: JobData, output_path: str):
        """Create a PDF cover letter"""
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=inch,
                leftMargin=inch,
                topMargin=inch,
                bottomMargin=inch
            )
            
            story = []
            
            # Add date
            date_text = datetime.now().strftime("%B %d, %Y")
            story.append(Paragraph(date_text, self.body_style))
            story.append(Spacer(1, 12))
            
            # Add cover letter content
            # Split the cover letter into paragraphs
            paragraphs = cover_letter_text.split('\n\n')
            
            for paragraph in paragraphs:
                if paragraph.strip():
                    # Clean up the paragraph text
                    clean_text = paragraph.strip().replace('\n', ' ')
                    story.append(Paragraph(clean_text, self.body_style))
                    story.append(Spacer(1, 6))
            
            # Build the PDF
            doc.build(story)
            logger.info(f"Cover letter PDF created: {output_path}")
            
        except Exception as e:
            logger.error(f"Error creating cover letter PDF: {str(e)}")
            raise Exception(f"Failed to create cover letter PDF: {str(e)}")
    
    def create_resume_pdf(self, resume_data: Dict[str, Any], job_data: JobData, output_path: str):
        """Create a PDF resume"""
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=inch,
                leftMargin=inch,
                topMargin=inch,
                bottomMargin=inch
            )
            
            story = []
            
            # Personal Information Header
            personal_info = resume_data.get('personal_info', {})
            
            # Name as title
            name = personal_info.get('full_name', 'Your Name')
            story.append(Paragraph(name, self.title_style))
            
            # Contact information
            contact_parts = []
            if personal_info.get('email'):
                contact_parts.append(personal_info['email'])
            if personal_info.get('phone'):
                contact_parts.append(personal_info['phone'])
            if personal_info.get('address'):
                contact_parts.append(personal_info['address'])
            
            contact_text = ' | '.join(contact_parts)
            story.append(Paragraph(contact_text, self.contact_style))
            
            # LinkedIn and GitHub
            links = []
            if personal_info.get('linkedin_url'):
                links.append(f"LinkedIn: {personal_info['linkedin_url']}")
            if personal_info.get('github_url'):
                links.append(f"GitHub: {personal_info['github_url']}")
            
            if links:
                story.append(Paragraph(' | '.join(links), self.contact_style))
            
            story.append(Spacer(1, 12))
            
            # Professional Summary
            if personal_info.get('professional_summary'):
                story.append(Paragraph("PROFESSIONAL SUMMARY", self.header_style))
                story.append(Paragraph(personal_info['professional_summary'], self.body_style))
                story.append(Spacer(1, 6))
            
            # Skills
            skills = resume_data.get('skills', [])
            if skills:
                story.append(Paragraph("TECHNICAL SKILLS", self.header_style))
                skills_text = ' • '.join(skills)
                story.append(Paragraph(skills_text, self.body_style))
                story.append(Spacer(1, 6))
            
            # Experience
            experience = resume_data.get('experience', [])
            if experience:
                story.append(Paragraph("PROFESSIONAL EXPERIENCE", self.header_style))
                
                for exp in experience:
                    # Job title and company
                    title_text = f"<b>{exp.get('title', 'Job Title')}</b> | {exp.get('company', 'Company Name')}"
                    story.append(Paragraph(title_text, self.body_style))
                    
                    # Location and dates
                    location_date = f"{exp.get('location', '')} | {exp.get('start_date', '')} - {exp.get('end_date', '')}"
                    story.append(Paragraph(location_date, self.body_style))
                    story.append(Spacer(1, 3))
                    
                    # Description
                    if exp.get('description'):
                        story.append(Paragraph(exp['description'], self.body_style))
                    
                    # Achievements
                    if exp.get('achievements'):
                        story.append(Spacer(1, 3))
                        for achievement in exp['achievements']:
                            story.append(Paragraph(f"• {achievement}", self.body_style))
                    
                    story.append(Spacer(1, 12))
            
            # Education
            education = resume_data.get('education', [])
            if education:
                story.append(Paragraph("EDUCATION", self.header_style))
                
                for edu in education:
                    degree_text = f"<b>{edu.get('degree', 'Degree')}</b>"
                    story.append(Paragraph(degree_text, self.body_style))
                    
                    school_text = f"{edu.get('school', 'School Name')}, {edu.get('location', '')}"
                    story.append(Paragraph(school_text, self.body_style))
                    
                    if edu.get('graduation_date'):
                        grad_text = f"Graduated: {edu['graduation_date']}"
                        if edu.get('gpa'):
                            grad_text += f" | GPA: {edu['gpa']}"
                        story.append(Paragraph(grad_text, self.body_style))
                    
                    story.append(Spacer(1, 6))
            
            # Projects
            projects = resume_data.get('projects', [])
            if projects:
                story.append(Paragraph("PROJECTS", self.header_style))
                
                for project in projects:
                    project_name = f"<b>{project.get('name', 'Project Name')}</b>"
                    story.append(Paragraph(project_name, self.body_style))
                    
                    if project.get('description'):
                        story.append(Paragraph(project['description'], self.body_style))
                    
                    if project.get('technologies'):
                        tech_text = f"Technologies: {', '.join(project['technologies'])}"
                        story.append(Paragraph(tech_text, self.body_style))
                    
                    if project.get('url'):
                        story.append(Paragraph(project['url'], self.body_style))
                    
                    story.append(Spacer(1, 6))
            
            # Certifications
            certifications = resume_data.get('certifications', [])
            if certifications:
                story.append(Paragraph("CERTIFICATIONS", self.header_style))
                
                for cert in certifications:
                    cert_text = f"• {cert.get('name', 'Certification')}"
                    if cert.get('issuer'):
                        cert_text += f" - {cert['issuer']}"
                    if cert.get('date'):
                        cert_text += f" ({cert['date']})"
                    story.append(Paragraph(cert_text, self.body_style))
            
            # Build the PDF
            doc.build(story)
            logger.info(f"Resume PDF created: {output_path}")
            
        except Exception as e:
            logger.error(f"Error creating resume PDF: {str(e)}")
            raise Exception(f"Failed to create resume PDF: {str(e)}")
    
    def create_simple_document(self, content: str, output_path: str, title: str = "Document"):
        """Create a simple PDF document with just text content"""
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=inch,
                leftMargin=inch,
                topMargin=inch,
                bottomMargin=inch
            )
            
            story = []
            
            # Add title
            story.append(Paragraph(title, self.title_style))
            story.append(Spacer(1, 12))
            
            # Add content
            paragraphs = content.split('\n\n')
            for paragraph in paragraphs:
                if paragraph.strip():
                    story.append(Paragraph(paragraph.strip(), self.body_style))
                    story.append(Spacer(1, 6))
            
            doc.build(story)
            logger.info(f"Simple PDF document created: {output_path}")
            
        except Exception as e:
            logger.error(f"Error creating simple PDF: {str(e)}")
            raise Exception(f"Failed to create simple PDF: {str(e)}")
