#!/usr/bin/env python3
"""
Test script to verify Notion status update functionality
"""
import os
import sys
import asyncio
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from services.notion_service import NotionService

async def test_status_update():
    """Test updating Notion status"""
    print("🧪 Testing Notion status update...")
    
    # Initialize service
    notion_service = NotionService()
    
    if not notion_service.is_healthy():
        print("❌ Notion service is not healthy")
        return
    
    # Get a sample page ID from database
    database_id = os.getenv("NOTION_DATABASE_ID")
    client = Client(auth=os.getenv("NOTION_API_KEY"))
    
    try:
        query_result = client.databases.query(database_id=database_id, page_size=1)
        
        if not query_result.get("results"):
            print("❌ No pages found in database")
            return
            
        sample_page_id = query_result["results"][0]["id"]
        print(f"📄 Using sample page: {sample_page_id}")
        
        # Test status update with "Applied"
        print("🔄 Testing status update to 'Applied'...")
        success = await notion_service.update_job_status(sample_page_id, "Applied")
        
        if success:
            print("✅ Status update to 'Applied' successful!")
            
            # Wait a moment then check the current status
            await asyncio.sleep(1)
            status_info = await notion_service.get_job_status(sample_page_id)
            print(f"📊 Current status: {status_info.get('status', 'unknown')}")
            
            # Test with "In progress" 
            print("🔄 Testing status update to 'In progress'...")
            success2 = await notion_service.update_job_status(sample_page_id, "In progress")
            
            if success2:
                print("✅ Status update to 'In progress' successful!")
            else:
                print("❌ Status update to 'In progress' failed")
                
        else:
            print("❌ Status update to 'Applied' failed")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_status_update())
