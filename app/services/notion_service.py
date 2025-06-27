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
                prop_type = status_prop.get("type")
                
                if prop_type == "select" and status_prop.get("select"):
                    status = status_prop["select"]["name"]
                elif prop_type == "status" and status_prop.get("status"):
                    status = status_prop["status"]["name"]
                elif prop_type == "multi_select" and status_prop.get("multi_select"):
                    # Take first status if multiple
                    multi_select = status_prop["multi_select"]
                    if multi_select:
                        status = multi_select[0]["name"]
            
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
            # First, get the current page to understand the property structure
            page = self.client.pages.retrieve(page_id=page_id)
            current_properties = page.get("properties", {})
            
            # Prepare properties to update
            properties = {}
            
            # Handle Status field - try different formats
            if "Status" in current_properties:
                status_prop = current_properties["Status"]
                status_type = status_prop.get("type", "")
                
                logger.info(f"Status property type: {status_type}")
                
                if status_type == "select":
                    properties["Status"] = {
                        "select": {
                            "name": status
                        }
                    }
                elif status_type == "multi_select":
                    properties["Status"] = {
                        "multi_select": [
                            {
                                "name": status
                            }
                        ]
                    }
                elif status_type == "status":
                    # Handle native status property type
                    # For status properties, we need to match against available options
                    # Try to map common status names to your available options
                    status_mapping = {
                        "Applied": "Applied",
                        "In Progress": "In progress", 
                        "Complete": "Done",
                        "Completed": "Done",
                        "Not Started": "Not started",
                        "Not started": "Not started",
                        "Done": "Done"
                    }
                    
                    # Use mapping if available, otherwise use the status as-is
                    mapped_status = status_mapping.get(status, status)
                    
                    properties["Status"] = {
                        "status": {
                            "name": mapped_status
                        }
                    }
                elif status_type == "rich_text":
                    properties["Status"] = {
                        "rich_text": [
                            {
                                "text": {
                                    "content": status
                                }
                            }
                        ]
                    }
                else:
                    logger.warning(f"Unknown status property type: {status_type}")
            
            # Handle Application Generated checkbox
            if "Application Generated" in current_properties:
                properties["Application Generated"] = {
                    "checkbox": True
                }
            
            # Handle Generated Date  
            if "Generated Date" in current_properties:
                properties["Generated Date"] = {
                    "date": {
                        "start": self._get_current_date()
                    }
                }
            
            # Handle Generated Files
            if files and "Generated Files" in current_properties:
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
            
            logger.info(f"Updating page {page_id} with properties: {list(properties.keys())}")
            
            # Update the page
            self.client.pages.update(
                page_id=page_id,
                properties=properties
            )
            
            logger.info(f"Updated Notion page {page_id} with status: {status}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating job status: {str(e)}")
            # Try a simpler update with just the status
            try:
                logger.info("Attempting simplified status update...")
                
                # Map status name to match your Notion options
                status_mapping = {
                    "Applied": "Applied",
                    "In Progress": "In progress", 
                    "Complete": "Done",
                    "Completed": "Done",
                    "Not Started": "Not started",
                    "Not started": "Not started",
                    "Done": "Done"
                }
                mapped_status = status_mapping.get(status, status)
                
                simple_properties = {
                    "Status": {
                        "status": {
                            "name": mapped_status
                        }
                    }
                }
                
                self.client.pages.update(
                    page_id=page_id,
                    properties=simple_properties
                )
                
                logger.info(f"Simplified update successful for page {page_id}")
                return True
                
            except Exception as e2:
                logger.error(f"Simplified update also failed: {str(e2)}")
                return False
            
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
    
    async def create_child_page(self, parent_page_id: str, title: str, content: str) -> str:
        """Create a child page with markdown content"""
        if not self.client:
            raise Exception("Notion client not initialized")
        
        try:
            # Convert markdown content to Notion blocks
            blocks = self._markdown_to_notion_blocks(content)
            
            # Create the child page
            page = self.client.pages.create(
                parent={
                    "type": "page_id",
                    "page_id": parent_page_id
                },
                properties={
                    "title": {
                        "title": [
                            {
                                "text": {
                                    "content": title
                                }
                            }
                        ]
                    }
                },
                children=blocks
            )
            
            logger.info(f"Created child page: {title}")
            return page["id"]
            
        except Exception as e:
            logger.error(f"Error creating child page: {str(e)}")
            raise Exception(f"Failed to create child page: {str(e)}")
    
    def _markdown_to_notion_blocks(self, markdown_content: str) -> list:
        """Convert markdown content to Notion blocks"""
        blocks = []
        lines = markdown_content.split('\n')
        current_paragraph = []
        
        for line in lines:
            line = line.rstrip()
            
            # Handle headers
            if line.startswith('# '):
                if current_paragraph:
                    blocks.append(self._create_paragraph_block('\n'.join(current_paragraph)))
                    current_paragraph = []
                blocks.append(self._create_heading_block(line[2:], 1))
            elif line.startswith('## '):
                if current_paragraph:
                    blocks.append(self._create_paragraph_block('\n'.join(current_paragraph)))
                    current_paragraph = []
                blocks.append(self._create_heading_block(line[3:], 2))
            elif line.startswith('### '):
                if current_paragraph:
                    blocks.append(self._create_paragraph_block('\n'.join(current_paragraph)))
                    current_paragraph = []
                blocks.append(self._create_heading_block(line[4:], 3))
            
            # Handle horizontal rules
            elif line.strip() == '---':
                if current_paragraph:
                    blocks.append(self._create_paragraph_block('\n'.join(current_paragraph)))
                    current_paragraph = []
                blocks.append({"type": "divider", "divider": {}})
            
            # Handle bullet points
            elif line.startswith('- '):
                if current_paragraph:
                    blocks.append(self._create_paragraph_block('\n'.join(current_paragraph)))
                    current_paragraph = []
                blocks.append(self._create_bullet_block(line[2:]))
            
            # Handle empty lines
            elif line.strip() == '':
                if current_paragraph:
                    blocks.append(self._create_paragraph_block('\n'.join(current_paragraph)))
                    current_paragraph = []
            
            # Regular text lines
            else:
                current_paragraph.append(line)
        
        # Add any remaining paragraph
        if current_paragraph:
            blocks.append(self._create_paragraph_block('\n'.join(current_paragraph)))
        
        return blocks
    
    def _create_heading_block(self, text: str, level: int) -> dict:
        """Create a Notion heading block"""
        heading_types = {1: "heading_1", 2: "heading_2", 3: "heading_3"}
        heading_type = heading_types.get(level, "heading_2")
        
        return {
            "type": heading_type,
            heading_type: {
                "rich_text": self._parse_rich_text(text)
            }
        }
    
    def _create_paragraph_block(self, text: str) -> dict:
        """Create a Notion paragraph block"""
        return {
            "type": "paragraph",
            "paragraph": {
                "rich_text": self._parse_rich_text(text)
            }
        }
    
    def _create_bullet_block(self, text: str) -> dict:
        """Create a Notion bulleted list item block"""
        return {
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": self._parse_rich_text(text)
            }
        }
    
    def _parse_rich_text(self, text: str) -> list:
        """Parse markdown-style formatting in text to Notion rich text format"""
        # Handle basic markdown formatting
        import re
        rich_text = []
        
        # Handle links [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        text_with_links = re.sub(link_pattern, lambda m: f"__LINK__{m.group(1)}__URL__{m.group(2)}__ENDLINK__", text)
        
        # Split by bold markers (**text**)
        parts = re.split(r'(\*\*[^*]+\*\*)', text_with_links)
        
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                # Bold text
                bold_text = part[2:-2]
                rich_text.append({
                    "type": "text",
                    "text": {"content": bold_text},
                    "annotations": {"bold": True}
                })
            elif '__LINK__' in part:
                # Handle links
                link_parts = part.split('__LINK__')
                for link_part in link_parts:
                    if '__URL__' in link_part and '__ENDLINK__' in link_part:
                        link_text, rest = link_part.split('__URL__', 1)
                        url, remaining = rest.split('__ENDLINK__', 1)
                        rich_text.append({
                            "type": "text",
                            "text": {"content": link_text, "link": {"url": url}}
                        })
                        if remaining:
                            rich_text.append({
                                "type": "text",
                                "text": {"content": remaining}
                            })
                    elif link_part:
                        rich_text.append({
                            "type": "text",
                            "text": {"content": link_part}
                        })
            elif part:
                # Regular text
                rich_text.append({
                    "type": "text",
                    "text": {"content": part}
                })
        
        return rich_text if rich_text else [{"type": "text", "text": {"content": text}}]
    
    def _get_current_date(self) -> str:
        """Get current date in ISO format"""
        from datetime import datetime
        return datetime.now().isoformat()
