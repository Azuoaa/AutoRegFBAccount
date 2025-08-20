# AutoRegFBAccount
Tool Reg (Create) Facebook Account (Python)

## What's New in This Update

This tool has been completely modernized and improved with the following enhancements:

### 🔧 **Code Improvements**
- **Modern Python practices**: Added type hints, better error handling, and improved code structure
- **Updated User-Agent**: Now uses Chrome 120 (latest stable version) instead of outdated Chrome 90
- **Better error handling**: Comprehensive try-catch blocks with meaningful error messages
- **Rate limiting protection**: Added delays between requests to avoid being blocked

### 🛡️ **Security & Configuration**
- **Configuration management**: Moved from hardcoded values to external config file
- **Environment variables support**: Can use environment variables for sensitive data
- **No more hardcoded credentials**: App ID, cookies, and passwords are now externalized

### 📁 **File Structure**
- `tool.py` - Main application with improved code
- `config.json` - Configuration file (create this with your credentials)
- `done.txt` - Output file with created accounts

## Setup Instructions

### 1. Install Dependencies
```bash
pip install requests
```

### 2. Configure the Tool
Create a `config.json` file with your Facebook app details:

```json
{
  "app_id": "your_facebook_app_id_here",
  "name": "TestUserName",
  "password": "TestUserPassword123",
  "cookie": "your_facebook_cookie_here",
  "number": 10
}
```

**Or use environment variables:**
```bash
export FB_APP_ID="your_app_id"
export FB_NAME="TestUserName"
export FB_PASSWORD="TestUserPassword123"
export FB_COOKIE="your_cookie"
export FB_NUMBER="10"
```

### 3. Run the Tool
```bash
python tool.py
```

## Features

- ✅ **Automatic test user creation** for Facebook apps
- ✅ **Batch processing** - create multiple accounts at once
- ✅ **Error handling** - continues even if some accounts fail
- ✅ **Progress tracking** - shows creation status for each account
- ✅ **Results logging** - saves all created accounts to `done.txt`
- ✅ **Rate limiting protection** - prevents Facebook from blocking requests

## Output Format

Each created account is saved in the format:
```
TestUserName|user_id|TestUserPassword123
```

## Important Notes

- **Facebook Developer Account Required**: You need a Facebook developer account with an app
- **Valid Cookie**: The cookie must be from a logged-in Facebook session
- **Rate Limiting**: The tool includes delays to avoid being blocked by Facebook
- **Test Users Only**: This creates test users for development purposes only

## Troubleshooting

- **"Configuration incomplete"**: Check your `config.json` file or environment variables
- **"Failed to extract Facebook tokens"**: Your cookie might be expired or invalid
- **"Request error"**: Check your internet connection and Facebook's status

## Security Warning

⚠️ **Never commit your `config.json` file to version control!** It contains sensitive information like cookies and passwords. Add it to your `.gitignore` file.
