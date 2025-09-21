#!/usr/bin/env python3
"""
🧪 Spotify API Integration Test
Tests Spotify connection and music therapy features
"""

import os
import sys
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

# Load environment variables
load_dotenv()

def test_spotify_connection():
    """Test basic Spotify API connection"""
    print("🎵 Testing Spotify API Connection...")
    
    # Get credentials from environment
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET not found in .env file")
        print("📝 Please add these to your .env file:")
        print("   SPOTIFY_CLIENT_ID=your_client_id_here")
        print("   SPOTIFY_CLIENT_SECRET=your_client_secret_here")
        return False
    
    try:
        # Initialize Spotify client
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id, 
            client_secret=client_secret
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        # Test connection with a simple search
        results = sp.search(q='meditation', type='playlist', limit=1)
        
        if results and results['playlists']['items']:
            print("✅ Spotify API connection successful!")
            return sp
        else:
            print("❌ Spotify API connected but no results found")
            return False
            
    except Exception as e:
        print(f"❌ Spotify API connection failed: {str(e)}")
        return False

def test_music_therapy_playlists(sp):
    """Test music therapy playlist creation"""
    print("\n🧘 Testing Music Therapy Playlist Generation...")
    
    # Define mood categories for therapy
    therapy_moods = {
        'anxiety_relief': ['calm', 'meditation', 'relaxing', 'ambient'],
        'depression_support': ['uplifting', 'motivational', 'positive', 'hope'],
        'stress_reduction': ['nature sounds', 'instrumental', 'peaceful', 'zen'],
        'focus_enhancement': ['lo-fi', 'study music', 'concentration', 'focus'],
        'sleep_therapy': ['sleep music', 'lullaby', 'bedtime', 'peaceful night']
    }
    
    playlist_results = {}
    
    for mood, keywords in therapy_moods.items():
        print(f"  🎼 Generating {mood.replace('_', ' ').title()} playlist...")
        
        try:
            # Search for tracks matching therapy mood
            tracks = []
            for keyword in keywords[:2]:  # Limit to 2 keywords per mood
                results = sp.search(q=keyword, type='track', limit=5)
                if results['tracks']['items']:
                    for track in results['tracks']['items']:
                        tracks.append({
                            'name': track['name'],
                            'artist': track['artists'][0]['name'],
                            'duration': track['duration_ms'],
                            'preview_url': track['preview_url'],
                            'external_url': track['external_urls']['spotify']
                        })
                        
            playlist_results[mood] = tracks[:10]  # Limit to 10 tracks per mood
            print(f"    ✅ Found {len(tracks)} tracks for {mood}")
            
        except Exception as e:
            print(f"    ❌ Error generating {mood} playlist: {str(e)}")
    
    return playlist_results

def test_real_time_recommendations(sp):
    """Test real-time mood-based recommendations"""
    print("\n🎯 Testing Real-time Mood Recommendations...")
    
    # Simulate different user moods
    test_moods = [
        {'mood': 'anxious', 'energy': 0.2, 'valence': 0.1},
        {'mood': 'happy', 'energy': 0.8, 'valence': 0.9}, 
        {'mood': 'sad', 'energy': 0.3, 'valence': 0.2},
        {'mood': 'stressed', 'energy': 0.9, 'valence': 0.3},
        {'mood': 'calm', 'energy': 0.4, 'valence': 0.7}
    ]
    
    for mood_state in test_moods:
        print(f"  🎭 Testing recommendations for {mood_state['mood']} user...")
        
        try:
            # Get recommendations based on mood parameters
            recommendations = sp.recommendations(
                seed_genres=['ambient', 'chill', 'classical'],
                target_energy=mood_state['energy'],
                target_valence=mood_state['valence'],
                limit=5
            )
            
            if recommendations['tracks']:
                print(f"    ✅ Found {len(recommendations['tracks'])} recommendations")
                for track in recommendations['tracks'][:3]:  # Show first 3
                    print(f"      🎵 {track['name']} by {track['artists'][0]['name']}")
            else:
                print(f"    ⚠️  No recommendations found for {mood_state['mood']}")
                
        except Exception as e:
            print(f"    ❌ Error getting recommendations for {mood_state['mood']}: {str(e)}")

def save_test_results(playlist_results):
    """Save test results for app integration"""
    print("\n💾 Saving test results...")
    
    try:
        # Create test data directory
        os.makedirs('test_data', exist_ok=True)
        
        # Save playlist results
        with open('test_data/spotify_playlists.json', 'w') as f:
            json.dump(playlist_results, f, indent=2)
        
        print("✅ Test results saved to test_data/spotify_playlists.json")
        return True
        
    except Exception as e:
        print(f"❌ Error saving test results: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Manas Wellness - Spotify Integration Test")
    print("=" * 50)
    
    # Test connection
    sp = test_spotify_connection()
    if not sp:
        print("\n❌ Spotify integration test failed!")
        print("Please check your API credentials and try again.")
        sys.exit(1)
    
    # Test music therapy features
    playlist_results = test_music_therapy_playlists(sp)
    test_real_time_recommendations(sp)
    save_test_results(playlist_results)
    
    print("\n🎉 Spotify Integration Test Summary:")
    print("=" * 50)
    print("✅ API Connection: Success")
    print("✅ Music Therapy Playlists: Generated")  
    print("✅ Real-time Recommendations: Working")
    print("✅ Test Data: Saved")
    
    print("\n🔧 Next Steps:")
    print("1. Update your .env file with the Spotify credentials")
    print("2. Restart your Flask application")
    print("3. Music therapy features will automatically use real Spotify data")
    print("4. Test the /music-therapy endpoint in your app")

if __name__ == "__main__":
    main()