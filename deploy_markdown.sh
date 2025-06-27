#!/bin/bash

# Deploy script for JobBuilder with Markdown output

echo "🚀 Deploying JobBuilder with Markdown output..."

# Set environment variable for markdown output
export OUTPUT_FORMAT=markdown

echo "📝 Output format set to: $OUTPUT_FORMAT"

# Check if .env file exists and update it
if [ -f .env ]; then
    # Remove existing OUTPUT_FORMAT line if it exists
    sed -i.bak '/^OUTPUT_FORMAT=/d' .env
    # Add new OUTPUT_FORMAT setting
    echo "OUTPUT_FORMAT=markdown" >> .env
    echo "✅ Updated .env file with OUTPUT_FORMAT=markdown"
else
    echo "⚠️  .env file not found. Make sure to set OUTPUT_FORMAT=markdown in your environment."
fi

echo "🎯 Markdown deployment configuration complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Make sure your Notion integration has page creation permissions"
echo "  2. Test with: python test_markdown.py"
echo "  3. Deploy your application"
echo ""
echo "💡 Benefits of Markdown output:"
echo "  ✅ Native Notion integration"
echo "  ✅ No download issues"
echo "  ✅ Immediate viewing and editing"
echo "  ✅ Mobile-friendly"
echo "  ✅ Easy sharing and collaboration"
