#!/usr/bin/env python3
"""
Helper script to get your LinkedIn person URN using the access token
Tries multiple endpoints based on available permissions
"""

import sys
import os
import requests
from pathlib import Path

# Add the project directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_loader import get_env_variable

def get_linkedin_urn_alternative():
    access_token = get_env_variable('LINKEDIN_ACCESS_TOKEN')

    if not access_token:
        print("ERROR: LINKEDIN_ACCESS_TOKEN not found in environment variables")
        return None

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Try the standard endpoint first
    print("Trying standard endpoint: https://api.linkedin.com/v2/me")
    profile_url = "https://api.linkedin.com/v2/me"
    response = requests.get(profile_url, headers=headers)

    if response.status_code == 200:
        profile_data = response.json()
        print("=== LinkedIn Profile Information ===")
        print(f"Profile Data: {profile_data}")

        person_id = profile_data.get('id')
        if person_id:
            urn = f"urn:li:person:{person_id}"
            print(f"\nYour LinkedIn Person URN is: {urn}")
            print(f"\nTo use this in the future, add this line to your .env file:")
            print(f"LINKEDIN_PERSON_URN={urn}")
            return urn
        else:
            print("Could not get person ID from LinkedIn profile via /me endpoint")
    else:
        print(f"Standard endpoint failed: {response.status_code}")
        print(f"Response: {response.text}")

    # Try the alternative endpoint for basic profile info
    print("\nTrying alternative endpoint: https://api.linkedin.com/v2/userinfo")
    userinfo_url = "https://api.linkedin.com/v2/userinfo"
    response = requests.get(userinfo_url, headers=headers)

    if response.status_code == 200:
        userinfo_data = response.json()
        print("=== LinkedIn User Information ===")
        print(f"User Info: {userinfo_data}")

        sub = userinfo_data.get('sub')  # This might be the ID we need
        if sub:
            # LinkedIn sometimes returns the sub as the person ID
            urn = f"urn:li:person:{sub}"
            print(f"\nYour LinkedIn Person URN might be: {urn}")
            print(f"\nTo use this in the future, add this line to your .env file:")
            print(f"LINKEDIN_PERSON_URN={urn}")
            return urn
        else:
            print("Could not get person ID from LinkedIn userinfo endpoint")
    else:
        print(f"Userinfo endpoint failed: {response.status_code}")
        print(f"Response: {response.text}")

    # If both methods fail, provide instructions
    print("\n=== Troubleshooting ===")
    print("If both methods failed, try these approaches:")
    print("1. Check that your OAuth token includes the correct scopes: r_liteprofile, r_emailaddress, w_member_social")
    print("2. Try refreshing your access token")
    print("3. Make sure your LinkedIn App is properly configured in the developer portal")
    print("4. As a last resort, you can manually find your LinkedIn ID by:")
    print("   a. Going to your LinkedIn profile")
    print("   b. Right-clicking 'Contact info' on the right side of your profile")
    print("   c. Looking for a URL like 'https://www.linkedin.com/in/YOUR_PUBLIC_ID/'")
    print("   d. Using a tool like https://www.linkedin.com/help/linkedin/answer/a547077 to find your internal ID")

    return None

if __name__ == "__main__":
    get_linkedin_urn_alternative()