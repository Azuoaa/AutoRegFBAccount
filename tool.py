import requests
import json
import os
from typing import Tuple, Optional
import time


def find_string(s: str, st: str, ed: str) -> str:
    """Extract string between start and end delimiters."""
    if (st in s) and (ed in s):
        if st == '':
            tmp = s
        else:
            tmp = s[(s.find(st) + len(st)):]
        if ed == '':
            return tmp
        elif ed in tmp:
            s = tmp[:(tmp.find(ed))]
            return s
        else:
            return ''
    else:
        return ''


def load_config() -> dict:
    """Load configuration from config.json or environment variables."""
    config_file = 'config.json'
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    # Fallback to environment variables
    return {
        'app_id': os.getenv('FB_APP_ID', ''),
        'name': os.getenv('FB_NAME', ''),
        'password': os.getenv('FB_PASSWORD', ''),
        'cookie': os.getenv('FB_COOKIE', ''),
        'number': int(os.getenv('FB_NUMBER', '10'))
    }


def save_config(config: dict):
    """Save configuration to config.json."""
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_headers(cookie: str) -> dict:
    """Get updated headers with modern user agent."""
    return {
        'authority': 'developers.facebook.com',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'viewport-width': '1030',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': cookie,
    }


def reg_run(app_id: str, cookie: str) -> Tuple[Optional[str], Optional[str], Optional[str], str, str]:
    """Register a new Facebook test user account."""
    try:
        headers = get_headers(cookie)
        
        # Get initial test users count
        url = f'https://developers.facebook.com/apps/{app_id}/roles/test-users/'
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        stt1 = len(response.text.rsplit('/apps/async/test-users/permissions/dialog/?app_id='))
        
        # Get Facebook tokens
        res = requests.get('https://mbasic.facebook.com/', headers=headers, timeout=30)
        res.raise_for_status()
        
        fb_dtsg = find_string(str(res.text).replace("'", '"'), '<input type="hidden" name="fb_dtsg" value="', '"')
        jazoest = find_string(str(res.text).replace("'", '"'), '<input type="hidden" name="jazoest" value="', '"')
        
        if not fb_dtsg or not jazoest:
            print("Failed to extract Facebook tokens")
            return None, None, None, app_id, cookie
        
        data = {
            'jazoest': jazoest,
            'fb_dtsg': fb_dtsg,
            'count': '1',
            'platform_version': 'v10.0',
            'age': '18',
            'language': 'en-US',
            '__a': '1',
            '__csr': '',
            '__req': 'a',
            '__beoa': '0',
            'dpr': '1',
        }
        
        response = requests.post(
            f'https://developers.facebook.com/apps/async/test-users/create/?app_id={app_id}',
            headers=headers,
            data=data,
            timeout=30
        )
        response.raise_for_status()
        
        if len(response.text) > 1000:
            # Get updated test users count
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            stt2 = len(response.text.rsplit('/apps/async/test-users/permissions/dialog/?app_id='))
            out_stt = stt2 - stt1
            
            if out_stt > 0:
                uid = response.text.rsplit('/apps/async/test-users/permissions/dialog/?app_id=')[out_stt].split('test_user_id=')[1].rsplit('"')[0]
                return uid, jazoest, fb_dtsg, app_id, cookie
        
        print("Failed to create test user")
        return None, None, None, app_id, cookie
        
    except requests.RequestException as e:
        print(f"Request error during registration: {e}")
        return None, None, None, app_id, cookie
    except Exception as e:
        print(f"Unexpected error during registration: {e}")
        return None, None, None, app_id, cookie


def change_run(uid: str, jazoest: str, fb_dtsg: str, app_id: str, cookie: str, name: str, password: str) -> Optional[str]:
    """Change test user account details."""
    try:
        headers = get_headers(cookie)
        
        data = {
            'jazoest': jazoest,
            'fb_dtsg': fb_dtsg,
            'name': name,
            'password': password,
            'confirm_password': password,
            '__a': '1',
            '__csr': '',
            '__req': 'a',
            '__beoa': '0',
            'dpr': '1'
        }
        
        response = requests.post(
            f'https://developers.facebook.com/apps/async/test-users/edit/?app_id={app_id}&test_user_id={uid}',
            headers=headers,
            data=data,
            timeout=30
        )
        response.raise_for_status()
        
        return f'{name}|{uid}|{password}'
        
    except requests.RequestException as e:
        print(f"Request error during account update: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during account update: {e}")
        return None


def main():
    """Main function to run the Facebook test user creation tool."""
    print("Facebook Test User Account Creator")
    print("=" * 40)
    
    # Load configuration
    config = load_config()
    
    # Check if configuration is complete
    if not all([config['app_id'], config['name'], config['password'], config['cookie']]):
        print("Configuration incomplete. Please check config.json or environment variables.")
        print("Required: FB_APP_ID, FB_NAME, FB_PASSWORD, FB_COOKIE")
        return
    
    print(f"App ID: {config['app_id']}")
    print(f"Creating {config['number']} test user accounts...")
    print("-" * 40)
    
    successful_accounts = 0
    
    for i in range(config['number']):
        print(f"Creating account {i+1}/{config['number']}...")
        
        # Register new account
        result = reg_run(config['app_id'], config['cookie'])
        if result[0] is None:  # uid is None
            print(f"Failed to create account {i+1}")
            continue
            
        uid, jazoest, fb_dtsg, app_id, cookie = result
        
        # Update account details
        acc = change_run(uid, jazoest, fb_dtsg, app_id, cookie, config['name'], config['password'])
        if acc:
            print(f"✓ Account {i+1}: {acc}")
            successful_accounts += 1
            
            # Save to file
            with open('done.txt', 'a+', encoding='utf-8') as f:
                f.write(acc + '\n')
        else:
            print(f"✗ Failed to update account {i+1}")
        
        # Add delay to avoid rate limiting
        if i < config['number'] - 1:
            time.sleep(2)
    
    print("-" * 40)
    print(f"Completed! {successful_accounts}/{config['number']} accounts created successfully.")
    print("Results saved to done.txt")


if __name__ == "__main__":
    main()