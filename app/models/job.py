from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class JobData(BaseModel):
    """Model for job posting data"""
    job_title: str = Field(..., description="The job title")
    company_name: str = Field(..., description="The company name")
    job_description: str = Field(..., description="The full job description")
    notion_page_id: str = Field(..., description="Notion page ID")
    salary_range: Optional[str] = Field(None, description="Salary range if available")
    location: Optional[str] = Field(None, description="Job location")
    employment_type: Optional[str] = Field(None, description="Full-time, part-time, contract, etc.")
    required_skills: Optional[List[str]] = Field(default_factory=list, description="List of required skills")
    preferred_skills: Optional[List[str]] = Field(default_factory=list, description="List of preferred skills")
    experience_level: Optional[str] = Field(None, description="Entry, mid, senior level")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class WebhookPayload(BaseModel):
    """Model for Notion webhook payload"""
    object: str
    id: str
    created_time: datetime
    last_edited_time: datetime
    properties: Dict[str, Any]
    url: str
    
class ApplicationData(BaseModel):
    """Model for generated application data"""
    job_data: JobData
    cover_letter: str
    resume_data: Dict[str, Any]
    generated_at: datetime = Field(default_factory=datetime.now)
    files_generated: List[str] = Field(default_factory=list)
    status: str = Field(default="pending", description="pending, generated, reviewed, submitted")

class PersonalInfo(BaseModel):
    """Model for personal information"""
    full_name: str
    email: str
    phone: str
    address: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    professional_summary: str
    
class ResumeData(BaseModel):
    """Model for resume data"""
    personal_info: PersonalInfo
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    skills: List[str]
    certifications: Optional[List[Dict[str, Any]]] = None
    projects: Optional[List[Dict[str, Any]]] = None
    achievements: Optional[List[str]] = None
    
class CoverLetterData(BaseModel):
    """Model for cover letter data"""
    content: str
    personalized_intro: str
    relevant_experience: str
    company_connection: str
    closing: str
