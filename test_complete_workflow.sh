#!/bin/bash

# Complete JobBuilder Workflow Test
APP_URL="https://jobbuilder-production.up.railway.app"

echo "🎯 Complete JobBuilder Workflow Test"
echo "======================================"
echo ""

# Test webhook with sample job data
echo "📋 Testing webhook with sample job posting..."

# Sample job data that mimics Notion's webhook payload
SAMPLE_PAYLOAD='{
  "object": "page",
  "id": "test-page-id-12345",
  "created_time": "2025-06-26T23:30:00.000Z",
  "last_edited_time": "2025-06-26T23:30:00.000Z",
  "properties": {
    "Job Title": {
      "type": "title",
      "title": [
        {
          "plain_text": "Senior Python Developer"
        }
      ]
    },
    "Company": {
      "type": "rich_text",
      "rich_text": [
        {
          "plain_text": "Tech Innovations Inc."
        }
      ]
    },
    "Job Description": {
      "type": "rich_text",
      "rich_text": [
        {
          "plain_text": "We are seeking a Senior Python Developer with 5+ years of experience in building scalable web applications. The ideal candidate will have expertise in Python, FastAPI, PostgreSQL, and AWS. You will be responsible for designing and implementing robust APIs, working with cross-functional teams, and mentoring junior developers. Strong problem-solving skills and experience with agile methodologies are required."
        }
      ]
    }
  },
  "url": "https://notion.so/test-page"
}'

echo "🚀 Sending webhook request..."
RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST \
  "$APP_URL/webhook/notion" \
  -H "Content-Type: application/json" \
  -d "$SAMPLE_PAYLOAD")

HTTP_STATUS=$(echo "$RESPONSE" | grep "HTTP_STATUS" | cut -d: -f2)
RESPONSE_BODY=$(echo "$RESPONSE" | grep -v "HTTP_STATUS")

echo "📊 Response Status: $HTTP_STATUS"
echo "📋 Response Body: $RESPONSE_BODY"
echo ""

if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ Webhook accepted successfully!"
    echo "🔄 Job application processing started in background"
    echo ""
    echo "⏳ Wait 30-60 seconds for processing to complete..."
    echo "📁 Generated files should appear in your Railway logs"
    echo "🔍 Check Railway logs for processing status"
else
    echo "❌ Webhook failed with status $HTTP_STATUS"
    echo "🔍 Check Railway logs for error details"
fi

echo ""
echo "🎯 Manual Testing Steps:"
echo "1. Check Railway logs for processing messages"
echo "2. Look for 'Job application processing completed' message"
echo "3. Verify PDF files were generated"
echo "4. Test with real Notion database entry"
echo ""
echo "📚 View API docs: $APP_URL/docs"
echo "🔍 Check health: $APP_URL/health"
