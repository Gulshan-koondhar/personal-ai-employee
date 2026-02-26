"""
Test Twitter and LinkedIn API Integration
"""
import sys
import os
from pathlib import Path

# Add gold directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'gold'))

from config_loader import get_env_variable

def test_twitter_api():
    """Test Twitter API with actual credentials"""
    print("=" * 60)
    print("Testing Twitter API Integration")
    print("=" * 60)
    
    # Load credentials
    api_key = get_env_variable('TWITTER_API_KEY')
    api_secret = get_env_variable('TWITTER_API_SECRET')
    access_token = get_env_variable('TWITTER_ACCESS_TOKEN')
    access_token_secret = get_env_variable('TWITTER_ACCESS_TOKEN_SECRET')
    
    print(f"\nCredentials loaded:")
    print(f"  API Key: {api_key[:10]}...{api_key[-5:] if len(api_key) > 15 else '***'}")
    print(f"  API Secret: {api_secret[:10]}...{api_secret[-5:] if len(api_secret) > 15 else '***'}")
    print(f"  Access Token: {access_token[:10]}...{access_token[-5:] if len(access_token) > 15 else '***'}")
    print(f"  Access Token Secret: {access_token_secret[:10]}...{'***'}")
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("\n[FAIL] FAILED: Missing Twitter credentials")
        return False
    
    try:
        import tweepy
        
        # Authenticate
        print("\nAuthenticating with Twitter API...")
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True
        )
        
        # Get user info to verify authentication
        print("Fetching user info...")
        me = client.get_me()
        if me.data:
            print(f"\n[OK] SUCCESS: Authenticated as @{me.data.username}")
            print(f"   Name: {me.data.name}")
            print(f"   ID: {me.data.id}")
        else:
            print("\n[WARN] WARNING: Could not fetch user info")
        
        # Create a test tweet with unique timestamp
        timestamp = Path(__file__).stat().st_mtime
        test_tweet = f"[AI TEST {timestamp}] Automated testing of Twitter integration for Personal AI Employee project #{int(timestamp) % 10000} #AI #Automation"
        
        print(f"\nPosting test tweet...")
        print(f"Content: {test_tweet[:100]}...")
        
        # Post tweet
        response = client.create_tweet(text=test_tweet)
        tweet_id = response.data['id']
        
        print(f"\n[OK] TWEET POSTED SUCCESSFULLY!")
        print(f"   Tweet ID: {tweet_id}")
        print(f"   URL: https://twitter.com/status/{tweet_id}")
        
        # Delete the test tweet
        print(f"\nDeleting test tweet...")
        client.delete_tweet(id=tweet_id)
        print(f"[OK] Tweet deleted")
        
        return True
        
    except ImportError:
        print("\n[FAIL] FAILED: tweepy not installed")
        print("   Install with: pip install tweepy")
        return False
    except Exception as e:
        print(f"\n[FAIL] FAILED: {type(e).__name__}")
        print(f"   Error: {str(e)}")
        return False

def test_linkedin_api():
    """Test LinkedIn API with actual credentials"""
    print("\n" + "=" * 60)
    print("Testing LinkedIn API Integration")
    print("=" * 60)
    
    # Load credentials
    access_token = get_env_variable('LINKEDIN_ACCESS_TOKEN')
    person_urn = get_env_variable('LINKEDIN_PERSON_URN')
    
    print(f"\nCredentials loaded:")
    print(f"  Access Token: {access_token[:10]}...{'***'}")
    print(f"  Person URN: {person_urn}")
    
    if not all([access_token, person_urn]):
        print("\n[FAIL] FAILED: Missing LinkedIn credentials")
        return False
    
    try:
        import requests
        
        # Test authentication by getting profile info
        print("\nTesting authentication...")
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        # Get profile info
        profile_url = "https://api.linkedin.com/v2/me"
        response = requests.get(profile_url, headers=headers)
        
        if response.status_code == 200:
            profile = response.json()
            print(f"\n[OK] SUCCESS: Authenticated")
            print(f"   ID: {profile.get('id', 'N/A')}")
        else:
            print(f"\n[WARN] WARNING: Profile fetch returned {response.status_code}")
            print(f"   Response: {response.text[:200]}")
        
        # Create a test post
        test_post = f"""[AI] AI Employee Test - Automated Testing

Testing LinkedIn integration for my Personal AI Employee project.

This is a unique test post (timestamp=9999) to verify LinkedIn integration.

#AI #Automation #LinkedInAPI #Test"""

        print(f"\nPosting test update to LinkedIn...")
        
        # Post to LinkedIn
        post_url = "https://api.linkedin.com/v2/ugcPosts"
        payload = {
            'author': person_urn,
            'lifecycleState': 'PUBLISHED',
            'specificContent': {
                'com.linkedin.ugc.ShareContent': {
                    'shareCommentary': {'text': test_post},
                    'shareMediaCategory': 'NONE'
                }
            },
            'visibility': {
                'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
            }
        }
        
        response = requests.post(post_url, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            post_data = response.json()
            post_id = post_data.get('id', 'unknown')
            
            print(f"\n[OK] LINKEDIN POST SUCCESS!")
            print(f"   Post ID: {post_id}")
            print(f"   Status: Published")
            
            # Note: LinkedIn doesn't have a simple delete API for posts
            print(f"\n[WARN] NOTE: LinkedIn post created successfully")
            print(f"   You may want to delete it manually from LinkedIn")
            
            return True
        else:
            print(f"\n[FAIL] FAILED: LinkedIn API error")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:300]}")
            return False
        
    except ImportError:
        print("\n[FAIL] FAILED: requests not installed")
        print("   Install with: pip install requests")
        return False
    except Exception as e:
        print(f"\n[FAIL] FAILED: {type(e).__name__}")
        print(f"   Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PERSONAL AI EMPLOYEE - SOCIAL MEDIA API TEST")
    print("=" * 60)
    
    twitter_result = test_twitter_api()
    linkedin_result = test_linkedin_api()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Twitter API:   {'[OK] PASS' if twitter_result else '[FAIL] FAIL'}")
    print(f"LinkedIn API:  {'[OK] PASS' if linkedin_result else '[FAIL] FAIL'}")
    print("=" * 60)
    
    if twitter_result and linkedin_result:
        print("\n[SUCCESS] All API tests passed!")
        print("Your Personal AI Employee can now post to Twitter and LinkedIn!")
    else:
        print("\n[WARN] Some tests failed. Check the errors above.")
    
    input("\nPress Enter to exit...")
