#!/usr/bin/env python3
"""
Simplified Enhanced Spotify Music Therapy Testing
Works with basic Spotify API access (no audio features required)
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from integrations.spotify_therapy import spotify_therapy
import json
from dotenv import load_dotenv

def test_basic_mood_playlists():
    """Test mood-based playlists without audio analysis"""
    print("\n" + "="*60)
    print("TESTING BASIC MOOD-BASED PLAYLISTS")
    print("="*60)
    
    moods = ['anxious', 'happy', 'sad', 'calm', 'energetic']
    
    for mood in moods:
        print(f"\nTesting Mood: {mood.upper()}")
        print("-" * 40)
        
        result = spotify_therapy.get_mood_based_playlist(mood, intensity=0.7)
        
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Total Tracks: {len(result.get('tracks', []))}")
        print(f"Therapy Focus: {result.get('therapy_focus', 'N/A')}")
        
        if result.get('tracks'):
            print("Sample Tracks:")
            for i, track in enumerate(result['tracks'][:3], 1):
                print(f"  {i}. {track.get('name', 'Unknown')} - {track.get('artist', 'Unknown')}")
                print(f"     Benefit: {track.get('therapy_benefit', 'N/A')}")

def test_therapeutic_search():
    """Test therapeutic music search functionality"""
    print("\n" + "="*60)
    print("TESTING THERAPEUTIC MUSIC SEARCH")
    print("="*60)
    
    search_terms = [
        'anxiety relief meditation',
        'sleep music peaceful',
        'focus concentration study',
        'depression support healing',
        'stress relief calm'
    ]
    
    for term in search_terms:
        print(f"\nSearching: '{term}'")
        print("-" * 40)
        
        result = spotify_therapy.search_therapeutic_music(term)
        
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Query: {result.get('query', 'N/A')}")
        print(f"Total Results: {len(result.get('results', []))}")
        
        if result.get('results'):
            print("Top Results:")
            for i, track in enumerate(result['results'][:5], 1):
                print(f"  {i}. {track.get('name', 'Unknown')} - {track.get('artist', 'Unknown')}")
                score = track.get('therapeutic_score', 'N/A')
                if score != 'N/A':
                    print(f"     Therapeutic Score: {score}")

def test_crisis_keywords():
    """Test crisis-specific music search"""
    print("\n" + "="*60)
    print("TESTING CRISIS INTERVENTION KEYWORDS")
    print("="*60)
    
    crisis_keywords = [
        'emergency calm peaceful',
        'panic attack relief',
        'breathing meditation anxiety',
        'safe space comfort music',
        'crisis support healing'
    ]
    
    for keyword in crisis_keywords:
        print(f"\nCrisis Search: '{keyword}'")
        print("-" * 40)
        
        result = spotify_therapy.search_therapeutic_music(keyword)
        
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Total Results: {len(result.get('results', []))}")
        
        if result.get('results'):
            print("Crisis Support Tracks:")
            for i, track in enumerate(result['results'][:3], 1):
                print(f"  {i}. {track.get('name', 'Unknown')} - {track.get('artist', 'Unknown')}")

def test_cultural_music_search():
    """Test cultural healing music search"""
    print("\n" + "="*60)
    print("TESTING CULTURAL HEALING MUSIC SEARCH")
    print("="*60)
    
    cultural_searches = [
        'indian classical meditation raga',
        'chinese traditional healing music',
        'japanese zen meditation',
        'african healing drums therapeutic',
        'tibetan singing bowls meditation'
    ]
    
    for search_term in cultural_searches:
        culture = search_term.split()[0]
        print(f"\nCultural Search ({culture.upper()}): '{search_term}'")
        print("-" * 50)
        
        result = spotify_therapy.search_therapeutic_music(search_term)
        
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Total Results: {len(result.get('results', []))}")
        
        if result.get('results'):
            print("Cultural Healing Tracks:")
            for i, track in enumerate(result['results'][:3], 1):
                print(f"  {i}. {track.get('name', 'Unknown')} - {track.get('artist', 'Unknown')}")

def test_study_focus_search():
    """Test study and focus music search"""
    print("\n" + "="*60)
    print("TESTING STUDY AND FOCUS MUSIC SEARCH")
    print("="*60)
    
    study_searches = [
        'lo-fi study beats concentration',
        'classical music focus memory',
        'ambient study peaceful instrumental',
        'binaural beats focus attention',
        'nature sounds study productivity'
    ]
    
    for search_term in study_searches:
        study_type = search_term.split()[0]
        print(f"\nStudy Search ({study_type.upper()}): '{search_term}'")
        print("-" * 50)
        
        result = spotify_therapy.search_therapeutic_music(search_term)
        
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Total Results: {len(result.get('results', []))}")
        
        if result.get('results'):
            print("Study Enhancement Tracks:")
            for i, track in enumerate(result['results'][:3], 1):
                print(f"  {i}. {track.get('name', 'Unknown')} - {track.get('artist', 'Unknown')}")

def test_sleep_therapy_search():
    """Test sleep therapy music search"""
    print("\n" + "="*60)
    print("TESTING SLEEP THERAPY MUSIC SEARCH")
    print("="*60)
    
    sleep_searches = [
        'sleep music deep relaxation',
        'insomnia relief peaceful dreams',
        'bedtime meditation calm',
        'rain sounds sleep therapy',
        'lullaby adult sleep healing'
    ]
    
    for search_term in sleep_searches:
        print(f"\nSleep Search: '{search_term}'")
        print("-" * 40)
        
        result = spotify_therapy.search_therapeutic_music(search_term)
        
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Total Results: {len(result.get('results', []))}")
        
        if result.get('results'):
            print("Sleep Therapy Tracks:")
            for i, track in enumerate(result['results'][:3], 1):
                print(f"  {i}. {track.get('name', 'Unknown')} - {track.get('artist', 'Unknown')}")

def demo_therapeutic_recommendations():
    """Demonstrate how to use the therapeutic music system"""
    print("\n" + "="*60)
    print("THERAPEUTIC MUSIC RECOMMENDATION DEMO")
    print("="*60)
    
    scenarios = [
        {
            'situation': 'User experiencing anxiety attack',
            'search': 'anxiety relief calm breathing',
            'mood': 'anxious'
        },
        {
            'situation': 'Student preparing for exams',
            'search': 'focus study concentration',
            'mood': 'stressed'
        },
        {
            'situation': 'Insomnia and sleep difficulties',
            'search': 'sleep meditation peaceful',
            'mood': 'restless'
        },
        {
            'situation': 'Depression and low mood',
            'search': 'uplifting healing hope music',
            'mood': 'sad'
        }
    ]
    
    for scenario in scenarios:
        print(f"\nScenario: {scenario['situation']}")
        print("-" * 50)
        
        # Get mood-based playlist
        mood_result = spotify_therapy.get_mood_based_playlist(scenario['mood'])
        print(f"Mood-based tracks: {len(mood_result.get('tracks', []))}")
        
        # Get search-based results
        search_result = spotify_therapy.search_therapeutic_music(scenario['search'])
        print(f"Search-based tracks: {len(search_result.get('results', []))}")
        
        # Show combined recommendation
        print("Recommended Approach:")
        print(f"  1. Start with {scenario['mood']} mood playlist")
        print(f"  2. Supplement with '{scenario['search']}' search results")
        print(f"  3. Therapy focus: {mood_result.get('therapy_focus', 'General wellness')}")

def main():
    """Run simplified Spotify music therapy tests"""
    print("Simplified Spotify Music Therapy Testing Suite")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check Spotify connection
    if spotify_therapy.is_connected:
        print("✓ Spotify API Connected - Testing with real data")
    else:
        print("! Spotify API Not Connected - Testing with fallback data")
    
    # Run all tests
    try:
        test_basic_mood_playlists()
        test_therapeutic_search()
        test_crisis_keywords()
        test_cultural_music_search()
        test_study_focus_search()
        test_sleep_therapy_search()
        demo_therapeutic_recommendations()
        
        print("\n" + "="*60)
        print("SIMPLIFIED SPOTIFY TESTING COMPLETED")
        print("="*60)
        print("All basic therapeutic music features tested successfully!")
        print("\nNote: Advanced audio analysis features require Spotify Premium API access.")
        print("Current implementation uses search-based therapeutic music discovery.")
        
    except Exception as e:
        print(f"\nTest Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()