# Markdown Output Feature

## Overview

The JobBuilder now supports **markdown output** as the primary method for generating job application materials. This replaces the previous PDF-only approach and provides better integration with Notion.

## Why Markdown?

✅ **Native Notion Support**: Content is directly viewable and editable in Notion  
✅ **No Download Issues**: No need to download files - everything is accessible in Notion  
✅ **Better User Experience**: Immediate viewing, editing, and copying  
✅ **Mobile Friendly**: Works perfectly on all devices  
✅ **Version Control**: Notion's built-in versioning works with the content  
✅ **Easy Sharing**: Share via Notion's native sharing features  

## How It Works

1. **Job Processing**: When a job is processed, the system generates:
   - A markdown-formatted cover letter
   - A markdown-formatted resume customized for the job

2. **Notion Integration**: The system creates two child pages under your job entry:
   - `Cover Letter - [Company Name]`
   - `Resume - [Company Name]`

3. **Rich Formatting**: The markdown includes:
   - **Headers** for section organization
   - **Bold text** for emphasis
   - **Bullet points** for skills and achievements
   - **Links** for GitHub/LinkedIn profiles
   - **Horizontal rules** for visual separation

## Configuration

Set the output format using the `OUTPUT_FORMAT` environment variable:

```bash
# Use markdown (recommended)
OUTPUT_FORMAT=markdown

# Use PDF (legacy)
OUTPUT_FORMAT=pdf
```

Default: `markdown`

## Sample Output Structure

### Cover Letter Format
```markdown
# Cover Letter

**Date:** June 26, 2025  
**Position:** Senior Python Developer  
**Company:** Tech Innovations Inc

---

Dear Hiring Manager,

I am writing to express my strong interest in the **Senior Python Developer** position at **Tech Innovations Inc**...

## Why I'm a Great Fit

In my previous roles, I have developed expertise in:
- **Python**
- **FastAPI**
- **AWS**
- **SQL**

## About Tech Innovations Inc

I am particularly drawn to Tech Innovations Inc's innovative approach...

---

*Generated automatically by JobBuilder*
```

### Resume Format
```markdown
# John Doe

📧 john.doe@email.com | 📞 (555) 123-4567 | 📍 City, State

[LinkedIn](https://linkedin.com/in/johndoe) | [GitHub](https://github.com/johndoe)

---

## Professional Summary

Experienced software developer with expertise in Python...

## Technical Skills

Python • FastAPI • AWS • SQL • Git • Docker • APIs • Agile

## Professional Experience

### Senior Developer | Previous Company
*San Francisco, CA | 2020-01 - Present*

Led development of scalable web applications...

**Key Achievements:**
- Improved application performance by 40%
- Led team of 5 developers

---

*Resume customized for Senior Python Developer at Tech Innovations Inc*
*Generated on June 26, 2025*
```

## Benefits for Users

1. **Immediate Access**: No waiting for downloads or file management
2. **Easy Editing**: Make quick edits directly in Notion if needed
3. **Professional Formatting**: Clean, modern appearance with proper structure
4. **Copy-Paste Ready**: Easy to copy sections for other applications
5. **Mobile Accessible**: Full functionality on mobile devices
6. **Searchable**: Content is searchable within Notion

## Testing

Run the test script to verify markdown generation:

```bash
python test_markdown.py
```

This will generate sample markdown files that you can inspect before deploying.

## Migration from PDF

If you were previously using PDF output:

1. **Automatic Migration**: Simply set `OUTPUT_FORMAT=markdown` 
2. **Hybrid Approach**: The system supports both formats
3. **Gradual Transition**: Test with markdown while keeping PDF as backup
4. **No Data Loss**: All existing PDF functionality remains available

## Troubleshooting

### Common Issues

1. **Child pages not appearing**: Check Notion API permissions
2. **Formatting issues**: Verify markdown syntax in generated content
3. **Long content**: Notion has block limits; content may be truncated

### Debugging

Enable debug logging to see markdown generation details:

```bash
DEBUG=true python -m app.main
```

## Future Enhancements

- **Rich Media Support**: Images and embedded content
- **Custom Templates**: User-defined markdown templates
- **Advanced Formatting**: Tables, code blocks, callouts
- **Export Options**: One-click export to PDF from Notion
