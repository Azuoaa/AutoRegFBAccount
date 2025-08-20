# AutoRegFBAccount

Tool for creating Facebook test user accounts (Python)

## Features

- Automatically creates Facebook test user accounts for your app
- Updates account credentials with custom names and passwords
- Configurable settings via JSON configuration file
- Error handling and retry logic
- Rate limiting protection
- Modern user agent strings

## Setup

1. **Install dependencies:**
   ```bash
   pip install requests
   ```

2. **Configure your settings:**
   - Edit `config.json` with your Facebook app details
   - Replace `YOUR_APP_ID_HERE` with your actual Facebook app ID
   - Replace `YOUR_COOKIE_HERE` with your Facebook developer cookie

3. **Run the tool:**
   ```bash
   python tool.py
   ```

## Configuration Options

- `app_id`: Your Facebook app ID
- `name`: Base name for test users (will be appended with numbers)
- `password`: Base password for test users (will be appended with numbers)
- `cookie`: Your Facebook developer session cookie
- `number_of_accounts`: How many test accounts to create
- `delay_between_requests`: Delay in seconds between account creation requests

## Output

- Account details are saved to `done.txt` in the format: `name|user_id|password`
- Console output shows progress and any errors
- Successful accounts are marked with ✓, failed ones with ✗

## Security Notes

- Never commit your `config.json` with real credentials
- Keep your Facebook developer cookie secure
- The tool includes rate limiting to avoid triggering Facebook's anti-spam measures

## Recent Updates

- ✅ Updated to Chrome 120 user agent
- ✅ Added comprehensive error handling
- ✅ Moved configuration to external JSON file
- ✅ Added rate limiting and delays
- ✅ Improved code structure and type hints
- ✅ Better error messages and logging
- ✅ Added timeout protection for requests
