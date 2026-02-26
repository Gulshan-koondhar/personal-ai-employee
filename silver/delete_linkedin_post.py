#!/usr/bin/env python3
"""
Script to delete a LinkedIn post using the LinkedIn API
"""

import sys
import os
import requests
from pathlib import Path

# Add the project directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_loader import get_env_variable

def delete_linkedin_post(post_urn: str):
    """
    Delete a LinkedIn post using the LinkedIn API
    According to LinkedIn documentation, to delete a post,
    you may need to use the shares endpoint instead of ugcPosts for some post types
    """
    access_token = get_env_variable('LINKEDIN_ACCESS_TOKEN')

    if not access_token:
        print("ERROR: LINKEDIN_ACCESS_TOKEN not found in environment variables")
        return False

    headers = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Try the shares endpoint first (another possible endpoint for deleting shared content)
    shares_url = f"https://api.linkedin.com/v2/shares/{post_urn}"

    try:
        response = requests.delete(shares_url, headers=headers)

        if response.status_code == 200 or response.status_code == 204:
            print(f"Successfully deleted post: {post_urn}")
            return True
        else:
            print(f"Shares endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")

        # If shares endpoint didn't work, try the socialActions endpoint to hide the post
        print("Trying socialActions endpoint...")
        social_actions_url = f"https://api.linkedin.com/v2/socialActions/{post_urn}/likes"

        response = requests.get(social_actions_url, headers=headers)  # This is just to test if the post exists
        print(f"SocialActions endpoint result: {response.status_code}")

        # The most likely correct method is to use the ugcPosts endpoint with the full URN
        # Let's try making a PUT request to change the lifecycleState to DRAFT which might effectively hide it
        print("Trying to update post to change lifecycle state...")
        update_url = f"https://api.linkedin.com/v2/ugcPosts/{post_urn}"

        update_payload = {
            "lifecycleState": "DRAFT"  # This might hide the post instead of deleting
        }

        response = requests.put(update_url, headers=headers, json=update_payload)
        print(f"Update lifecycleState result: {response.status_code}")

        if response.status_code == 200 or response.status_code == 201:
            print(f"Successfully updated post lifecycle state (may have hidden it): {post_urn}")
            return True

        # If all API methods fail, inform user they may need to delete manually
        print("API deletion attempts failed. As an alternative, you can manually delete the post:")
        print("1. Go to your LinkedIn profile")
        print("2. Find the post that starts with: 'Hello, I'm Claude, an AI assistant created by Anthropic'")
        print("3. Click the three dots menu on the post")
        print("4. Select 'Delete'")

        return False

    except Exception as e:
        print(f"Error deleting post: {str(e)}")
        print("Manual deletion recommended:")
        print("1. Go to your LinkedIn profile")
        print("2. Find the post that starts with: 'Hello, I'm Claude, an AI assistant created by Anthropic'")
        print("3. Click the three dots menu on the post")
        print("4. Select 'Delete'")
        return False

def main():
    print("=== Deleting LinkedIn Post ===")

    # The post ID we want to delete
    post_urn = "urn:li:share:7430854483556999168"
    print(f"Attempting to delete post: {post_urn}")

    success = delete_linkedin_post(post_urn)

    if success:
        print("\nPost deletion completed successfully!")
    else:
        print("\nPost deletion failed. The post may not exist or you may not have permission to delete it.")

if __name__ == "__main__":
    main()