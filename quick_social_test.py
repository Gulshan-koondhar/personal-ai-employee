"""
Quick test of Twitter and LinkedIn APIs with unique content
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import random

# Add gold directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'gold'))
from config_loader import get_env_variable

def test_twitter():
    """Test Twitter API"""
    print("\n" + "="*60)
    print("TWITTER API TEST")
    print("="*60)
    
    api_key = get_env_variable('TWITTER_API_KEY')
    api_secret = get_env_variable('TWITTER_API_SECRET')
    access_token = get_env_variable('TWITTER_ACCESS_TOKEN')
    access_token_secret = get_env_variable('TWITTER_ACCESS_TOKEN_SECRET')
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("[FAIL] Missing credentials")
        return False
    
    try:
        import tweepy
        
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        
        # Auth test
        me = client.get_me()
        print(f"[OK] Authenticated as @{me.data.username}")
        
        # Post unique tweet
        unique_id = datetime.now().strftime('%H%M%S') + str(random.randint(1000, 9999))
        tweet_text = f"AI Employee Test {unique_id} - Testing Twitter integration for Personal AI Employee project #AI #Test{unique_id}"
        
        print(f"[INFO] Posting: {tweet_text[:80]}...")
        
        response = client.create_tweet(text=tweet_text)
        tweet_id = response.data['id']
        
        print(f"[OK] Tweet posted! ID: {tweet_id}")
        print(f"[OK] URL: https://twitter.com/status/{tweet_id}")
        
        # Delete test tweet
        client.delete_tweet(id=tweet_id)
        print(f"[OK] Test tweet deleted")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] {type(e).__name__}: {str(e)}")
        return False

def test_linkedin():
    """Test LinkedIn API"""
    print("\n" + "="*60)
    print("LINKEDIN API TEST")
    print("="*60)
    
    access_token = get_env_variable('LINKEDIN_ACCESS_TOKEN')
    person_urn = get_env_variable('LINKEDIN_PERSON_URN')
    
    if not all([access_token, person_urn]):
        print("[FAIL] Missing credentials")
        return False
    
    try:
        import requests
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        # Post unique content
        unique_id = datetime.now().strftime('%H%M%S') + str(random.randint(1000, 9999))
        post_text = f"""AI Employee Test {unique_id}

Testing LinkedIn API integration for Personal AI Employee project.

Unique ID: {unique_id}
#AI #Automation #Test"""

        print(f"[INFO] Posting to LinkedIn...")
        
        payload = {
            'author': person_urn,
            'lifecycleState': 'PUBLISHED',
            'specificContent': {
                'com.linkedin.ugc.ShareContent': {
                    'shareCommentary': {'text': post_text},
                    'shareMediaCategory': 'NONE'
                }
            },
            'visibility': {
                'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
            }
        }
        
        response = requests.post('https://api.linkedin.com/v2/ugcPosts', 
                                headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            post_id = response.json().get('id')
            print(f"[OK] LinkedIn post published! ID: {post_id}")
            return True
        else:
            print(f"[FAIL] Status {response.status_code}")
            print(f"[FAIL] {response.text[:200]}")
            return False
        
    except Exception as e:
        print(f"[FAIL] {type(e).__name__}: {str(e)}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("SOCIAL MEDIA API TEST")
    print("="*60)
    
    twitter_ok = test_twitter()
    linkedin_ok = test_linkedin()
    
    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    print(f"Twitter:  {'[OK] PASS' if twitter_ok else '[FAIL] FAIL'}")
    print(f"LinkedIn: {'[OK] PASS' if linkedin_ok else '[FAIL] FAIL'}")
    print("="*60)
