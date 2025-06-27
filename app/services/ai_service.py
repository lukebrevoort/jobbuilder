import os
import json
import logging
from typing import Dict, Any
from ..models.job import JobData, ResumeData, PersonalInfo

logger = logging.getLogger(__name__)

class AIService:
    """Service for AI-powered content generation"""
    
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.2")
        self.personal_info = self._load_personal_info()
        self.base_resume = self._load_base_resume()
        
    def is_healthy(self) -> bool:
        """Check if AI service is available"""
        try:
            # For now, just check if we have the necessary data
            return self.personal_info is not None and self.base_resume is not None
        except Exception as e:
            logger.error(f"AI service health check failed: {str(e)}")
            return False
    
    def _load_personal_info(self) -> Dict[str, Any]:
        """Load personal information from file"""
        try:
            data_dir = os.getenv("DATA_DIR", "./data")
            personal_info_path = os.path.join(data_dir, "personal_info.json")
            
            if os.path.exists(personal_info_path):
                with open(personal_info_path, 'r') as f:
                    return json.load(f)
            else:
                # Return default template if file doesn't exist
                logger.warning("Personal info file not found, using template")
                return self._get_default_personal_info()
                
        except Exception as e:
            logger.error(f"Error loading personal info: {str(e)}")
            return self._get_default_personal_info()
    
    def _load_base_resume(self) -> Dict[str, Any]:
        """Load base resume data from file"""
        try:
            data_dir = os.getenv("DATA_DIR", "./data")
            resume_path = os.path.join(data_dir, "base_resume.json")
            
            if os.path.exists(resume_path):
                with open(resume_path, 'r') as f:
                    return json.load(f)
            else:
                logger.warning("Base resume file not found, using template")
                return self._get_default_resume()
                
        except Exception as e:
            logger.error(f"Error loading base resume: {str(e)}")
            return self._get_default_resume()
    
    async def generate_cover_letter(self, job_data: JobData) -> str:
        """Generate a personalized cover letter"""
        try:
            # For now, use template-based generation
            # Later can be replaced with actual AI calls to Ollama
            
            template = self._get_cover_letter_template()
            
            # Simple template substitution
            cover_letter = template.format(
                company_name=job_data.company_name,
                job_title=job_data.job_title,
                full_name=self.personal_info.get("full_name", "Your Name"),
                relevant_experience=self._extract_relevant_experience(job_data),
                skills_match=self._extract_matching_skills(job_data),
                company_connection=self._generate_company_connection(job_data)
            )
            
            return cover_letter
            
        except Exception as e:
            logger.error(f"Error generating cover letter: {str(e)}")
            raise Exception(f"Failed to generate cover letter: {str(e)}")
    
    async def customize_resume(self, job_data: JobData) -> Dict[str, Any]:
        """Customize resume based on job requirements"""
        try:
            # Start with base resume
            customized_resume = self.base_resume.copy()
            
            # Get matching skills for prioritization
            job_desc_lower = job_data.job_description.lower()
            my_skills = self.base_resume.get("skills", [])
            
            matching_skills = []
            for skill in my_skills:
                if skill.lower() in job_desc_lower:
                    matching_skills.append(skill)
            
            # Reorder skills to prioritize matching ones
            all_skills = customized_resume.get("skills", [])
            prioritized_skills = matching_skills + [skill for skill in all_skills if skill not in matching_skills]
            customized_resume["skills"] = prioritized_skills[:15]  # Limit to top 15 skills
            
            # Customize professional summary
            original_summary = customized_resume.get("personal_info", {}).get("professional_summary", "")
            if matching_skills:
                customized_summary = f"{original_summary} Particularly interested in {job_data.job_title} roles with expertise in {', '.join(matching_skills[:3])}."
            else:
                customized_summary = f"{original_summary} Excited about the {job_data.job_title} opportunity at {job_data.company_name}."
            
            if "personal_info" not in customized_resume:
                customized_resume["personal_info"] = {}
            customized_resume["personal_info"]["professional_summary"] = customized_summary
            
            return customized_resume
            
        except Exception as e:
            logger.error(f"Error customizing resume: {str(e)}")
            raise Exception(f"Failed to customize resume: {str(e)}")
    
    def _extract_relevant_experience(self, job_data: JobData) -> str:
        """Extract relevant experience based on job description"""
        # This is a simplified version - can be enhanced with actual AI analysis
        experience_items = self.base_resume.get("experience", [])
        
        if not experience_items:
            return "My diverse professional experience"
        
        # For now, just return the most recent experience
        recent_experience = experience_items[0] if experience_items else {}
        
        return f"My experience as {recent_experience.get('title', 'a professional')} at {recent_experience.get('company', 'my previous role')}"
    
    def _extract_matching_skills(self, job_data: JobData) -> str:
        """Extract skills that match the job description and format as markdown list"""
        job_desc_lower = job_data.job_description.lower()
        my_skills = self.base_resume.get("skills", [])
        
        matching_skills = []
        for skill in my_skills:
            if skill.lower() in job_desc_lower:
                matching_skills.append(skill)
        
        if not matching_skills:
            # If no exact matches, return top skills
            matching_skills = my_skills[:5]
        
        # Format as markdown list
        if matching_skills:
            skills_list = "\n".join([f"- **{skill}**" for skill in matching_skills[:8]])
            return f"\n{skills_list}\n"
        else:
            return "\n- **Professional experience** in relevant technologies\n"
    
    def _generate_company_connection(self, job_data: JobData) -> str:
        """Generate a connection to the company"""
        # This is simplified - could be enhanced with company research
        return f"I am particularly drawn to {job_data.company_name}'s innovative approach and would be excited to contribute to your team's success."
    
    def _get_cover_letter_template(self) -> str:
        """Get the cover letter template"""
        return """Dear Hiring Manager,

I am writing to express my strong interest in the **{job_title}** position at **{company_name}**. {relevant_experience} aligns perfectly with the requirements outlined in your job posting.

## Why I'm a Great Fit

In my previous roles, I have developed expertise in:
{skills_match}

These skills directly translate to the requirements for this position and would allow me to contribute immediately to your team.

## About {company_name}

{company_connection}

## Next Steps

I would welcome the opportunity to discuss how my background and enthusiasm can contribute to {company_name}'s continued success. I'm excited about the possibility of joining your team and am available for an interview at your convenience.

Thank you for your consideration.

**Sincerely,**  
{full_name}"""
    
    def _get_default_personal_info(self) -> Dict[str, Any]:
        """Return default personal info template"""
        return {
            "full_name": "Your Full Name",
            "email": "your.email@example.com",
            "phone": "(555) 123-4567",
            "address": "Your City, State",
            "linkedin_url": "https://linkedin.com/in/yourprofile",
            "github_url": "https://github.com/yourusername",
            "professional_summary": "Experienced professional with a passion for technology and innovation."
        }
    
    def _get_default_resume(self) -> Dict[str, Any]:
        """Return default resume template"""
        return {
            "personal_info": self._get_default_personal_info(),
            "experience": [
                {
                    "title": "Your Job Title",
                    "company": "Company Name",
                    "location": "City, State",
                    "start_date": "2020-01",
                    "end_date": "Present",
                    "description": "Description of your role and achievements",
                    "achievements": [
                        "Key achievement 1",
                        "Key achievement 2"
                    ]
                }
            ],
            "education": [
                {
                    "degree": "Your Degree",
                    "school": "University Name",
                    "location": "City, State",
                    "graduation_date": "2020-05",
                    "gpa": "3.8"
                }
            ],
            "skills": [
                "Python", "JavaScript", "React", "Node.js", "SQL", 
                "Git", "AWS", "Docker", "APIs", "Agile"
            ],
            "projects": [
                {
                    "name": "Project Name",
                    "description": "Brief description of the project",
                    "technologies": ["Tech1", "Tech2"],
                    "url": "https://github.com/yourusername/project"
                }
            ]
        }

    async def call_ollama_api(self, prompt: str) -> str:
        """Call Ollama API for AI generation (placeholder for future implementation)"""
        # This is a placeholder for when you want to integrate actual Ollama API calls
        # For now, we'll use template-based generation
        
        try:
            import requests
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return ""
                
        except Exception as e:
            logger.error(f"Error calling Ollama API: {str(e)}")
            return ""
