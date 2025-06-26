#!/usr/bin/env python3
"""
Test the improved webhook handler with actual Notion payload format
"""

import requests
import json

# Your Railway app URL
APP_URL = "https://jobbuilder-production.up.railway.app"

# Sample payload that matches the Notion automation format you received
test_payload = {
    "source": {
        "type": "automation",
        "automation_id": "21ef7879-ec1d-8045-b4fb-004d3e7fa3d8",
        "action_id": "21ef7879-ec1d-80e0-a686-005a0c2e9975",
        "event_id": "de6e55cb-c3e9-4310-9210-cd0ddd0ac67c",
        "attempt": 1
    },
    "data": {
        "object": "page",
        "id": "21ef7879-ec1d-8022-b3c2-e69017fcc88e",
        "created_time": "2025-06-26T22:26:00.000Z",
        "last_edited_time": "2025-06-26T23:31:00.000Z",
        "properties": {
            "Job Title": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Software Engineering Intern",
                            "link": None
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": "Software Engineering Intern",
                        "href": None
                    }
                ]
            },
            "Company": {
                "id": "company",
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Lockheed Martin",
                            "link": None
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": "Lockheed Martin",
                        "href": None
                    }
                ]
            },
            "Job Description": {
                "id": "description",
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "Join Lockheed Martin as a Software Engineering Intern and work on cutting-edge aerospace and defense technologies. This internship offers hands-on experience with software development, systems integration, and engineering best practices in a dynamic and innovative environment. You'll collaborate with experienced engineers on real projects that make a difference in national security and space exploration.",
                            "link": None
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": "Join Lockheed Martin as a Software Engineering Intern and work on cutting-edge aerospace and defense technologies. This internship offers hands-on experience with software development, systems integration, and engineering best practices in a dynamic and innovative environment. You'll collaborate with experienced engineers on real projects that make a difference in national security and space exploration.",
                        "href": None
                    }
                ]
            }
        }
    }
}

def test_webhook():
    print("🧪 Testing improved webhook handler...")
    print(f"📡 Sending to: {APP_URL}/webhook/notion")
    
    try:
        response = requests.post(
            f"{APP_URL}/webhook/notion",
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Webhook processed successfully!")
            print("🔄 Check Railway logs for processing details")
        else:
            print("❌ Webhook failed")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_webhook()
