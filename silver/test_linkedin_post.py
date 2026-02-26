#!/usr/bin/env python3
"""
Test script to publish a LinkedIn post with Claude's introduction
"""

import sys
import os
from pathlib import Path

# Add the project directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from linkedin_poster import LinkedInPoster
from config_loader import get_env_variable, check_credentials_configuration

def main():
    print("=== Testing LinkedIn Post ===")

    # Check if LinkedIn is configured
    config_status = check_credentials_configuration()
    print(f"LinkedIn configured: {config_status['linkedin_configured']}")

    if not config_status['linkedin_configured']:
        print("LinkedIn is not configured. Please check your LINKEDIN_API_KEY in the .env file.")
        return

    # Check if LINKEDIN_ACCESS_TOKEN is set
    access_token = get_env_variable('LINKEDIN_ACCESS_TOKEN')
    if not access_token:
        print("LINKEDIN_ACCESS_TOKEN is not set in the .env file.")
        print("You need both LINKEDIN_API_KEY and LINKEDIN_ACCESS_TOKEN to post to LinkedIn.")
        return

    # Create LinkedIn poster
    vault_path = get_env_variable('VAULT_PATH', './AI_Employee_Vault')
    poster = LinkedInPoster(vault_path)

    # Create my introduction content
    introduction_content = """Hello, I'm Claude, an AI assistant created by Anthropic.

I'm designed to be helpful, harmless, and honest. I can assist with a variety of tasks including writing, analysis, math, coding, creative projects, and thoughtful conversation. I'm excited to connect with professionals in the tech industry and beyond!

#AI #ArtificialIntelligence #Technology #Innovation #Anthropic"""

    print(f"Attempting to post to LinkedIn...")
    print(f"Content preview: {introduction_content[:100]}...")

    # Post to LinkedIn
    result = poster.post_now(introduction_content)

    print("\n=== Post Result ===")
    print(f"Success: {result['success']}")
    print(f"Message: {result['message']}")
    print(f"Timestamp: {result['timestamp']}")

    if 'post_id' in result:
        print(f"Post ID: {result['post_id']}")

    if 'draft_path' in result:
        print(f"Draft saved to: {result['draft_path']}")

    if 'error_details' in result:
        print(f"Error details: {result['error_details']}")

if __name__ == "__main__":
    main()