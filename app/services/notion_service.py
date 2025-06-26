import os
from typing import Dict, Any, Optional
from notion_client import Client
import logging

logger = logging.getLogger(__name__)

class NotionService:
    """Service for interacting with Notion API"""
    
    def __init__(self):
        self.api_key = os.getenv("NOTION_API_KEY")
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        self.client = None
        
        if self.api_key:
            self.client = Client(auth=self.api_key)
        else:
            logger.warning("Notion API key not found in environment variables")
    
    def is_healthy(self) -> bool:
        """Check if the Notion service is properly configured and accessible"""
        if not self.client or not self.api_key:
            return False
        
        try:
            # Test connection by retrieving user info
            self.client.users.me()
            return True
        except Exception as e:
            logger.error(f"Notion health check failed: {str(e)}")
            return False
    
    async def get_job_status(self, page_id: str) -> Dict[str, Any]:
        """Get the current status of a job from Notion"""
        if not self.client:
            raise Exception("Notion client not initialized")
        
        try:
            page = self.client.pages.retrieve(page_id=page_id)
            
            # Extract status from properties
            properties = page.get("properties", {})
            status = "unknown"
            
            if "Status" in properties:
                status_prop = properties["Status"]
                if status_prop.get("type") == "select" and status_prop.get("select"):
                    status = status_prop["select"]["name"]
            
            return {
                "status": status,
                "last_edited": page.get("last_edited_time"),
                "properties": properties
            }
            
        except Exception as e:
            logger.error(f"Error getting job status: {str(e)}")
            raise Exception(f"Failed to get job status: {str(e)}")
    
    async def update_job_status(self, page_id: str, status: str, files: Optional[list] = None) -> bool:
        """Update the status of a job in Notion"""
        if not self.client:
            logger.warning("Notion client not initialized, skipping status update")
            return False
        
        try:
            # Prepare properties to update
            properties = {
                "Status": {
                    "select": {
                        "name": status
                    }
                },
                "Application Generated": {
                    "checkbox": True
                },
                "Generated Date": {
                    "date": {
                        "start": self._get_current_date()
                    }
                }
            }
            
            # Add file information if provided
            if files:
                file_names = [os.path.basename(f) for f in files]
                properties["Generated Files"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": ", ".join(file_names)
                            }
                        }
                    ]
                }
            
            # Update the page
            self.client.pages.update(
                page_id=page_id,
                properties=properties
            )
            
            logger.info(f"Updated Notion page {page_id} with status: {status}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating job status: {str(e)}")
            return False
    
    async def get_job_details(self, page_id: str) -> Dict[str, Any]:
        """Get detailed job information from Notion page"""
        if not self.client:
            raise Exception("Notion client not initialized")
        
        try:
            page = self.client.pages.retrieve(page_id=page_id)
            return page
            
        except Exception as e:
            logger.error(f"Error getting job details: {str(e)}")
            raise Exception(f"Failed to get job details: {str(e)}")
    
    async def create_job_entry(self, job_data: Dict[str, Any]) -> str:
        """Create a new job entry in Notion (for testing purposes)"""
        if not self.client or not self.database_id:
            raise Exception("Notion client or database ID not configured")
        
        try:
            properties = {
                "Job Title": {
                    "title": [
                        {
                            "text": {
                                "content": job_data.get("job_title", "")
                            }
                        }
                    ]
                },
                "Company": {
                    "rich_text": [
                        {
                            "text": {
                                "content": job_data.get("company_name", "")
                            }
                        }
                    ]
                },
                "Job Description": {
                    "rich_text": [
                        {
                            "text": {
                                "content": job_data.get("job_description", "")
                            }
                        }
                    ]
                },
                "Status": {
                    "select": {
                        "name": "Not Started"
                    }
                }
            }
            
            page = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            
            return page["id"]
            
        except Exception as e:
            logger.error(f"Error creating job entry: {str(e)}")
            raise Exception(f"Failed to create job entry: {str(e)}")
    
    def _get_current_date(self) -> str:
        """Get current date in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
