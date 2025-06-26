#!/usr/bin/env python3
"""
Debug script to check Notion database Status property type
"""
import os
import sys
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def debug_notion_status():
    """Debug the Notion Status property type"""
    api_key = os.getenv("NOTION_API_KEY")
    database_id = os.getenv("NOTION_DATABASE_ID")
    
    if not api_key or not database_id:
        print("❌ Missing NOTION_API_KEY or NOTION_DATABASE_ID")
        return
    
    client = Client(auth=api_key)
    
    try:
        # Get database schema
        print("🔍 Retrieving database schema...")
        database = client.databases.retrieve(database_id=database_id)
        
        properties = database.get("properties", {})
        
        print(f"\n📊 Database Properties:")
        for prop_name, prop_data in properties.items():
            prop_type = prop_data.get("type", "unknown")
            print(f"  • {prop_name}: {prop_type}")
            
            # Show details for Status property
            if prop_name == "Status":
                print(f"    Full Status property data:")
                print(f"    {prop_data}")
                
                # If it's a status type, show options
                if prop_type == "status":
                    options = prop_data.get("status", {}).get("options", [])
                    print(f"    Available status options:")
                    for option in options:
                        print(f"      - {option.get('name', 'Unknown')} (id: {option.get('id', 'Unknown')})")
                
                # If it's a select type, show options
                elif prop_type == "select":
                    options = prop_data.get("select", {}).get("options", [])
                    print(f"    Available select options:")
                    for option in options:
                        print(f"      - {option.get('name', 'Unknown')} (id: {option.get('id', 'Unknown')})")
        
        # Get a sample page to see current structure
        print(f"\n📄 Sample page data:")
        query_result = client.databases.query(database_id=database_id, page_size=1)
        
        if query_result.get("results"):
            sample_page = query_result["results"][0]
            page_id = sample_page["id"]
            print(f"Sample page ID: {page_id}")
            
            status_prop = sample_page.get("properties", {}).get("Status", {})
            print(f"Status property in sample page: {status_prop}")
            
        else:
            print("No pages found in database")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_notion_status()
