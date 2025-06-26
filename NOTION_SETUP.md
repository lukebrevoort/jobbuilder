# 📝 Notion Setup for JobBuilder

## Step 1: Create Notion Integration

1. **Go to:** https://www.notion.so/my-integrations
2. **Click:** "New integration"
3. **Fill out:**
   - Name: `JobBuilder`
   - Logo: (optional)
   - Associated workspace: Select your workspace
4. **Click:** "Submit"
5. **Copy the "Internal Integration Token"** → This is your `NOTION_API_KEY`

## Step 2: Create Job Database

### Option A: Use This Template (Recommended)

Create a new page in Notion and paste this database:

```
Job Title | Company | Job Description | Status | Application Generated | Generated Date | Generated Files
```

### Option B: Manual Setup

1. **Create a new database** in Notion
2. **Add these properties:**

| Property Name | Type | Options |
|---------------|------|---------|
| `Job Title` | Title | (default) |
| `Company` | Text | |
| `Job Description` | Text | |
| `Status` | Select | Not Started, In Progress, Applied, Generated |
| `Application Generated` | Checkbox | |
| `Generated Date` | Date | |
| `Generated Files` | Text | (optional) |

## Step 3: Share Database with Integration

1. **Click the "Share" button** on your database
2. **Click "Invite"**
3. **Search for "JobBuilder"** (your integration name)
4. **Select it and click "Invite"**

## Step 4: Get Database ID

1. **Open your database** in Notion
2. **Copy the URL** - it looks like:
   ```
   https://notion.so/your-workspace/abc123def456?v=...
   ```
3. **Extract the database ID:** `abc123def456`
4. **This is your `NOTION_DATABASE_ID`**

## Step 5: Set Up Automation

1. **In your database, click "•••" (more options)**
2. **Select "Automations"**
3. **Click "New automation"**
4. **Configure:**

### Trigger:
- **When:** Property is edited
- **Property:** Status
- **Condition:** Equals "In Progress"

### Action:
- **Do:** Make an HTTP request
- **URL:** `https://your-app.railway.app/webhook/notion`
- **Method:** POST
- **Headers:** 
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Body:** Use Notion's default webhook payload

5. **Click "Create automation"**

## Step 6: Update Environment Variables

Add these to your Railway deployment:

```bash
NOTION_API_KEY=secret_abc123...
NOTION_DATABASE_ID=abc123def456...
WEBHOOK_SECRET=any-random-string-here
```

## Step 7: Test the Integration

1. **Add a test job** to your Notion database:
   - **Job Title:** "Test Developer"
   - **Company:** "Test Company"
   - **Job Description:** "This is a test job posting for Python development."
   - **Status:** "Not Started"

2. **Change Status to "In Progress"**

3. **Check Railway logs** to see if webhook was received

4. **Wait 30-60 seconds** for processing

5. **Check if Status changed to "Generated"**

## 🎯 Complete Example Entry

Here's what a complete job entry looks like:

| Field | Value |
|-------|-------|
| Job Title | Senior Python Developer |
| Company | Tech Innovations Inc. |
| Job Description | We are seeking a Senior Python Developer with 5+ years experience... |
| Status | In Progress → Generated (auto-updated) |
| Application Generated | ☑️ (auto-checked) |
| Generated Date | 2025-06-26 (auto-filled) |
| Generated Files | cover_letter_Tech_Innovations_Inc_20250626_143022.pdf, resume_Tech_Innovations_Inc_20250626_143022.pdf |

## 🔧 Troubleshooting

### Webhook Not Triggered
- ✅ Check automation is enabled
- ✅ Verify database is shared with integration
- ✅ Confirm webhook URL is correct
- ✅ Test with different status changes

### Integration Permissions
- ✅ Database must be explicitly shared with integration
- ✅ Integration needs read/write access
- ✅ Check integration is active in workspace

### Common Issues
1. **Database ID wrong format** - should be 32 characters
2. **API key starts with "secret_"** - copy the full token
3. **Webhook URL missing /webhook/notion** - include the endpoint
4. **Status values case sensitive** - use exact matches

## 🎉 You're Connected!

Once working, every time you:
1. **Add a job** to Notion
2. **Set status to "In Progress"**
3. **JobBuilder automatically:**
   - Analyzes the job description
   - Generates personalized cover letter
   - Customizes your resume
   - Creates PDF documents
   - Updates Notion with completion status

Your automated job application system is now live! 🚀
