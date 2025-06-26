#!/bin/bash

# JobBuilder Deployment Test Script
echo "🧪 Testing JobBuilder Deployment..."

# Get your Railway URL (replace with your actual URL)
read -p "Enter your Railway app URL (e.g., https://jobbuilder-production-xyz.up.railway.app): " APP_URL

if [ -z "$APP_URL" ]; then
    echo "❌ Please provide your Railway app URL"
    exit 1
fi

echo ""
echo "🎯 Testing deployment: $APP_URL"
echo ""

# Test 1: Basic health check
echo "1️⃣ Testing basic health check..."
curl -s "$APP_URL/" | head -5
echo ""

# Test 2: Detailed health check
echo "2️⃣ Testing detailed health check..."
curl -s "$APP_URL/health" | jq '.' 2>/dev/null || curl -s "$APP_URL/health"
echo ""

# Test 3: API documentation
echo "3️⃣ Testing API docs accessibility..."
curl -s -o /dev/null -w "Status: %{http_code}\n" "$APP_URL/docs"
echo ""

# Test 4: Webhook endpoint
echo "4️⃣ Testing webhook endpoint..."
curl -s -o /dev/null -w "Status: %{http_code}\n" -X POST "$APP_URL/webhook/notion" -H "Content-Type: application/json" -d '{}'
echo ""

echo "✅ Basic deployment tests complete!"
echo ""
echo "📋 Next steps:"
echo "1. If all tests show 200 status codes, your deployment is working!"
echo "2. Visit $APP_URL/docs to see the API documentation"
echo "3. Your webhook URL is: $APP_URL/webhook/notion"
echo "4. Now set up Notion integration with this webhook URL"
