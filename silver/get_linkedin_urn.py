#!/usr/bin/env python3
"""
Helper script to get your LinkedIn person URN using the access token
"""

import sys
import os
import requests
from pathlib import Path

# Add the project directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_loader import get_env_variable

def get_linkedin_profile_info():
    access_token = get_env_variable('LINKEDIN_ACCESS_TOKEN')

    if not access_token:
        print("ERROR: LINKEDIN_ACCESS_TOKEN not found in environment variables")
        return None

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Get the user's profile information
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
            print("Could not get person ID from LinkedIn profile")
            print(f"Response: {profile_data}")
            return None
    else:
        print(f"Could not get LinkedIn profile: {response.status_code}")
        print(f"Response: {response.text}")

        # Different error handling based on the specific error
        if response.status_code == 403:
            print("\nThis is typically due to insufficient permissions.")
            print("Your LinkedIn app may need the following permissions:")
            print("- r_liteprofile")
            print("- r_emailaddress")
            print("- w_member_social")
        elif response.status_code == 401:
            print("\nThis indicates your access token may be invalid or expired.")

        return None

if __name__ == "__main__":
    get_linkedin_profile_info()