import os
import logging
from jinja2 import Environment, FileSystemLoader, Template

logger = logging.getLogger(__name__)

class TemplateService:
    """Service for managing document templates"""
    
    def __init__(self):
        self.templates_dir = os.getenv("TEMPLATES_DIR", "./templates")
        self.env = None
        self._setup_jinja_environment()
    
    def _setup_jinja_environment(self):
        """Set up Jinja2 environment for template rendering"""
        try:
            if os.path.exists(self.templates_dir):
                self.env = Environment(loader=FileSystemLoader(self.templates_dir))
            else:
                logger.warning(f"Templates directory not found: {self.templates_dir}")
                # Create directory and add default templates
                os.makedirs(self.templates_dir, exist_ok=True)
                self._create_default_templates()
                self.env = Environment(loader=FileSystemLoader(self.templates_dir))
        except Exception as e:
            logger.error(f"Error setting up template environment: {str(e)}")
    
    def render_cover_letter(self, template_data: dict) -> str:
        """Render cover letter using template"""
        try:
            if not self.env:
                return self._get_fallback_cover_letter(template_data)
            
            template = self.env.get_template("cover_letter.j2")
            return template.render(**template_data)
            
        except Exception as e:
            logger.error(f"Error rendering cover letter template: {str(e)}")
            return self._get_fallback_cover_letter(template_data)
    
    def render_resume(self, template_data: dict) -> str:
        """Render resume using template"""
        try:
            if not self.env:
                return self._get_fallback_resume(template_data)
            
            template = self.env.get_template("resume.j2")
            return template.render(**template_data)
            
        except Exception as e:
            logger.error(f"Error rendering resume template: {str(e)}")
            return self._get_fallback_resume(template_data)
    
    def _create_default_templates(self):
        """Create default template files"""
        try:
            # Create cover letter template
            cover_letter_template = self._get_default_cover_letter_template()
            with open(os.path.join(self.templates_dir, "cover_letter.j2"), 'w') as f:
                f.write(cover_letter_template)
            
            # Create resume template
            resume_template = self._get_default_resume_template()
            with open(os.path.join(self.templates_dir, "resume.j2"), 'w') as f:
                f.write(resume_template)
            
            logger.info("Created default templates")
            
        except Exception as e:
            logger.error(f"Error creating default templates: {str(e)}")
    
    def _get_default_cover_letter_template(self) -> str:
        """Get default cover letter template"""
        return """{{ personal_info.full_name }}
{{ personal_info.email }} | {{ personal_info.phone }}
{% if personal_info.address %}{{ personal_info.address }}{% endif %}
{% if personal_info.linkedin_url %}{{ personal_info.linkedin_url }}{% endif %}

{{ date }}

Dear Hiring Manager,

I am writing to express my strong interest in the {{ job_data.job_title }} position at {{ job_data.company_name }}. With my background in {{ relevant_skills|join(', ') }}, I am confident that I would be a valuable addition to your team.

{% if relevant_experience %}
{{ relevant_experience }}
{% endif %}

In reviewing the job description, I was particularly excited about {{ job_highlights }}. My experience with {{ matching_skills|join(', ') }} makes me well-suited for this role.

Key qualifications I bring include:
{% for qualification in key_qualifications %}
• {{ qualification }}
{% endfor %}

{{ company_connection }}

I would welcome the opportunity to discuss how my background and enthusiasm can contribute to {{ job_data.company_name }}'s continued success. Thank you for your consideration, and I look forward to hearing from you.

Sincerely,
{{ personal_info.full_name }}"""
    
    def _get_default_resume_template(self) -> str:
        """Get default resume template"""
        return """{{ personal_info.full_name }}
{{ personal_info.email }} | {{ personal_info.phone }}
{% if personal_info.address %}{{ personal_info.address }}{% endif %}
{% if personal_info.linkedin_url %}LinkedIn: {{ personal_info.linkedin_url }}{% endif %}
{% if personal_info.github_url %}GitHub: {{ personal_info.github_url }}{% endif %}

PROFESSIONAL SUMMARY
{{ personal_info.professional_summary }}

TECHNICAL SKILLS
{{ skills|join(' • ') }}

PROFESSIONAL EXPERIENCE
{% for exp in experience %}
{{ exp.title }} | {{ exp.company }}
{{ exp.location }} | {{ exp.start_date }} - {{ exp.end_date }}

{{ exp.description }}

{% if exp.achievements %}
Key Achievements:
{% for achievement in exp.achievements %}
• {{ achievement }}
{% endfor %}
{% endif %}

{% endfor %}

EDUCATION
{% for edu in education %}
{{ edu.degree }}
{{ edu.school }}, {{ edu.location }}
{% if edu.graduation_date %}Graduated: {{ edu.graduation_date }}{% endif %}
{% if edu.gpa %}GPA: {{ edu.gpa }}{% endif %}

{% endfor %}

{% if projects %}
PROJECTS
{% for project in projects %}
{{ project.name }}
{{ project.description }}
Technologies: {{ project.technologies|join(', ') }}
{% if project.url %}{{ project.url }}{% endif %}

{% endfor %}
{% endif %}

{% if certifications %}
CERTIFICATIONS
{% for cert in certifications %}
• {{ cert.name }}{% if cert.issuer %} - {{ cert.issuer }}{% endif %}{% if cert.date %} ({{ cert.date }}){% endif %}
{% endfor %}
{% endif %}"""
    
    def _get_fallback_cover_letter(self, data: dict) -> str:
        """Fallback cover letter when template fails"""
        personal_info = data.get('personal_info', {})
        job_data = data.get('job_data')
        
        return f"""{personal_info.get('full_name', 'Your Name')}
{personal_info.get('email', 'your.email@example.com')} | {personal_info.get('phone', '(555) 123-4567')}

Dear Hiring Manager,

I am writing to express my strong interest in the {job_data.job_title if job_data else 'position'} at {job_data.company_name if job_data else 'your company'}.

{personal_info.get('professional_summary', 'I am an experienced professional with a passion for technology and innovation.')}

I believe my skills and experience make me an ideal candidate for this role. I would welcome the opportunity to discuss how I can contribute to your team's success.

Thank you for your consideration.

Sincerely,
{personal_info.get('full_name', 'Your Name')}"""
    
    def _get_fallback_resume(self, data: dict) -> str:
        """Fallback resume when template fails"""
        personal_info = data.get('personal_info', {})
        skills = data.get('skills', [])
        
        return f"""{personal_info.get('full_name', 'Your Name')}
{personal_info.get('email', 'your.email@example.com')} | {personal_info.get('phone', '(555) 123-4567')}

PROFESSIONAL SUMMARY
{personal_info.get('professional_summary', 'Experienced professional with a passion for technology.')}

TECHNICAL SKILLS
{' • '.join(skills) if skills else 'Various technical skills'}

EXPERIENCE
Please add your work experience details.

EDUCATION
Please add your education details."""
