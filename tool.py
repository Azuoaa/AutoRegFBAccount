import requests
import json
import time
from typing import Tuple, Optional


def find_string(s: str, st: str, ed: str) -> str:
    """Extract substring between start and end markers."""
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


def reg_run(app_id: str, cookie: str) -> Tuple[str, str, str, str, str]:
    """Create a new test user account."""
    try:
        headers = get_headers(cookie)
        
        # Get initial count
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
            raise ValueError("Failed to extract Facebook tokens")
        
        # Create test user
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
            # Get updated count and extract user ID
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            stt2 = len(response.text.rsplit('/apps/async/test-users/permissions/dialog/?app_id='))
            out_stt = stt2 - stt1
            
            if out_stt > 0:
                uid = response.text.rsplit('/apps/async/test-users/permissions/dialog/?app_id=')[out_stt].split('test_user_id=')[1].rsplit('"')[0]
                return uid, jazoest, fb_dtsg, app_id, cookie
            else:
                raise ValueError("No new test user created")
        else:
            raise ValueError("Test user creation failed")
            
    except requests.RequestException as e:
        raise Exception(f"Network error during registration: {e}")
    except Exception as e:
        raise Exception(f"Registration failed: {e}")


def change_run(uid: str, jazoest: str, fb_dtsg: str, app_id: str, cookie: str, name: str, password: str) -> str:
    """Update test user credentials."""
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
        raise Exception(f"Network error during credential update: {e}")
    except Exception as e:
        raise Exception(f"Credential update failed: {e}")


def load_config() -> dict:
    """Load configuration from config.json file."""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default config if file doesn't exist
        default_config = {
            "app_id": "YOUR_APP_ID_HERE",
            "name": "TestUser",
            "password": "TestPass123",
            "cookie": "YOUR_COOKIE_HERE",
            "number_of_accounts": 10,
            "delay_between_requests": 2
        }
        with open('config.json', 'w') as f:
            json.dump(default_config, f, indent=2)
        print("Created config.json with default values. Please update it with your actual credentials.")
        return default_config


def main():
    """Main function to run the account creation process."""
    try:
        # Load configuration
        config = load_config()
        
        # Check if configuration is properly set
        if (config["app_id"] == "YOUR_APP_ID_HERE" or 
            config["cookie"] == "YOUR_COOKIE_HERE"):
            print("Please update config.json with your actual Facebook app ID and cookie.")
            return
        
        app_id = config["app_id"]
        name = config["name"]
        password = config["password"]
        cookie = config["cookie"]
        number = config["number_of_accounts"]
        delay = config["delay_between_requests"]
        
        print(f"Starting creation of {number} test user accounts...")
        print(f"App ID: {app_id}")
        print(f"Base name: {name}")
        print(f"Base password: {password}")
        print("-" * 50)
        
        successful_accounts = 0
        
        for i in range(number):
            try:
                print(f"Creating account {i+1}/{number}...")
                
                uid, jazoest, fb_dtsg, app_id, cookie = reg_run(app_id, cookie)
                acc = change_run(uid, jazoest, fb_dtsg, app_id, cookie, f"{name}{i+1}", f"{password}{i+1}")
                
                print(f"✓ Account {i+1}: {acc}")
                
                # Save to file
                with open('done.txt', 'a+', encoding='utf-8') as f:
                    f.write(acc + '\n')
                
                successful_accounts += 1
                
                # Add delay between requests to avoid rate limiting
                if i < number - 1:  # Don't delay after the last request
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"✗ Failed to create account {i+1}: {e}")
                continue
        
        print("-" * 50)
        print(f"Process completed. {successful_accounts}/{number} accounts created successfully.")
        
        if successful_accounts > 0:
            print("Account details saved to 'done.txt'")
        
    except Exception as e:
        print(f"Fatal error: {e}")


if __name__ == "__main__":
    main()