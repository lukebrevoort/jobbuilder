#!/bin/bash

# Notion Database Structure Validator
echo "🔍 Notion Database Structure Validator"
echo "======================================"
echo ""

APP_URL="https://jobbuilder-production.up.railway.app"

echo "📋 Testing Notion database structure..."
echo ""

# Create test payload with proper structure
echo "🧪 Testing with properly structured payload..."

PROPER_PAYLOAD='{
  "data": {
    "object": "page",
    "id": "test-page-id-123",
    "properties": {
      "Job Title": {
        "type": "title",
        "title": [
          {
            "type": "text",
            "text": {
              "content": "Software Engineering Intern"
            },
            "plain_text": "Software Engineering Intern"
          }
        ]
      },
      "Company": {
        "type": "rich_text",
        "rich_text": [
          {
            "type": "text",
            "text": {
              "content": "Lockheed Martin"
            },
            "plain_text": "Lockheed Martin"
          }
        ]
      },
      "Job Description": {
        "type": "rich_text",
        "rich_text": [
          {
            "type": "text",
            "text": {
              "content": "Seeking a software engineering intern to work on advanced aerospace projects. Requirements include Python, C++, and systems programming experience."
            },
            "plain_text": "Seeking a software engineering intern to work on advanced aerospace projects. Requirements include Python, C++, and systems programming experience."
          }
        ]
      }
    }
  }
}'

echo "🚀 Sending test webhook..."
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST \
  "$APP_URL/webhook/notion" \
  -H "Content-Type: application/json" \
  -d "$PROPER_PAYLOAD")

HTTP_STATUS=$(echo "$RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
RESPONSE_BODY=$(echo "$RESPONSE" | grep -v "HTTP_STATUS")

echo "📊 Response Status: $HTTP_STATUS"
echo "📋 Response Body: $RESPONSE_BODY"
echo ""

if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ Webhook processed successfully!"
    echo "🔄 Check Railway logs for detailed processing information"
    echo ""
    echo "📋 Look for these log messages:"
    echo "   - 'Extracted job title: Software Engineering Intern'"
    echo "   - 'Extracted company name: Lockheed Martin'"
    echo "   - 'Processing job: Software Engineering Intern at Lockheed Martin'"
    echo "   - 'Job application processing completed'"
else
    echo "❌ Webhook failed with status $HTTP_STATUS"
fi

echo ""
echo "🎯 Notion Database Setup Checklist:"
echo ""
echo "✅ Required Properties (exact names):"
echo "   📝 Job Title (Type: Title)"
echo "   🏢 Company (Type: Text or Rich Text)"
echo "   📄 Job Description (Type: Text or Rich Text)"
echo "   🎯 Status (Type: Select with options: Not Started, In Progress, Applied, Generated)"
echo ""
echo "✅ Integration Setup:"
echo "   🔗 Database shared with 'JobBuilder' integration"
echo "   🔑 Integration has read/write permissions"
echo "   🤖 Automation triggers on Status = 'In Progress'"
echo "   📡 Webhook URL: $APP_URL/webhook/notion"
echo ""
echo "🚨 If still having issues:"
echo "   1. Check property names match exactly (case sensitive)"
echo "   2. Verify integration permissions"
echo "   3. Test automation with a simple entry"
echo "   4. Check Railway logs for detailed error messages"
