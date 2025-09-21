#!/usr/bin/env python3
"""
Test script for Spotify Music Therapy Backend
"""

import os
import sys
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_spotify_endpoints():
    """Test all Spotify API endpoints"""
    base_url = "http://127.0.0.1:8000"
    
    print("🎵 Testing Spotify Music Therapy Backend...")
    print("=" * 50)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    tests = [
        {
            'name': 'Spotify Token',
            'endpoint': '/api/spotify/token',
            'method': 'GET'
        },
        {
            'name': 'Search Tracks',
            'endpoint': '/api/spotify/search?q=calm&type=track&limit=5',
            'method': 'GET'
        },
        {
            'name': 'Happy Mood Tracks',
            'endpoint': '/api/spotify/tracks/happy',
            'method': 'GET'
        },
        {
            'name': 'Calm Mood Playlists',
            'endpoint': '/api/spotify/playlists/calm',
            'method': 'GET'
        },
        {
            'name': 'Mood Categories',
            'endpoint': '/api/spotify/mood-categories',
            'method': 'GET'
        },
        {
            'name': 'Recommendations',
            'endpoint': '/api/spotify/recommendations',
            'method': 'POST',
            'data': {'mood': 'calm', 'energy_level': 0.5}
        }
    ]
    
    successful_tests = 0
    total_tests = len(tests)
    
    for test in tests:
        try:
            print(f"\n🧪 Testing: {test['name']}")
            url = f"{base_url}{test['endpoint']}"
            
            if test['method'] == 'GET':
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, json=test.get('data', {}), timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {test['name']}: SUCCESS")
                
                # Show some data preview
                if 'tracks' in data:
                    tracks = data.get('tracks', {}).get('items', [])
                    if tracks:
                        print(f"   📀 Found {len(tracks)} tracks")
                        print(f"   🎵 Sample: {tracks[0].get('name', 'Unknown')} by {tracks[0].get('artists', [{}])[0].get('name', 'Unknown')}")
                elif 'playlists' in data:
                    playlists = data.get('playlists', {}).get('items', [])
                    if playlists:
                        print(f"   📝 Found {len(playlists)} playlists")
                        print(f"   🎵 Sample: {playlists[0].get('name', 'Unknown')}")
                elif 'categories' in data:
                    categories = data.get('categories', {})
                    print(f"   📂 Categories: {', '.join(categories.keys())}")
                elif 'access_token' in data:
                    print(f"   🔑 Token received (length: {len(data['access_token'])})")
                
                successful_tests += 1
            else:
                print(f"❌ {test['name']}: HTTP {response.status_code}")
                print(f"   Error: {response.text[:200]}...")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {test['name']}: CONNECTION ERROR")
            print(f"   Error: {str(e)}")
        except Exception as e:
            print(f"❌ {test['name']}: ERROR")
            print(f"   Error: {str(e)}")
    
    print(f"\n🏁 Test Results: {successful_tests}/{total_tests} passed")
    print("=" * 50)
    
    if successful_tests == total_tests:
        print("🎉 All tests passed! Your Spotify integration is working perfectly!")
    elif successful_tests > total_tests // 2:
        print("⚠️  Most tests passed. Some endpoints might need attention.")
    else:
        print("🚨 Multiple tests failed. Check your server and configurations.")
    
    return successful_tests == total_tests

if __name__ == "__main__":
    success = test_spotify_endpoints()
    sys.exit(0 if success else 1)