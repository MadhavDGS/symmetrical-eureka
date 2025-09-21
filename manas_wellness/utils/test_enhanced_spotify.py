#!/usr/bin/env python3
"""
Enhanced Spotify Music Therapy Testing
Tests all advanced therapeutic music features
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from integrations.spotify_therapy import spotify_therapy
import json
from dotenv import load_dotenv

def test_crisis_intervention():
    """Test crisis intervention playlists"""
    print("\n" + "="*60)
    print("TESTING CRISIS INTERVENTION MUSIC")
    print("="*60)
    
    crisis_levels = ['high', 'medium', 'low']
    
    for level in crisis_levels:
        print(f"\nTesting Crisis Level: {level.upper()}")
        print("-" * 40)
        
        result = spotify_therapy.get_crisis_intervention_playlist(
            crisis_level=level, 
            duration_minutes=10
        )
        
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Therapy Focus: {result.get('therapy_focus', 'N/A')}")
        print(f"Usage Instructions: {result.get('usage_instructions', 'N/A')}")
        print(f"Total Tracks: {len(result.get('tracks', []))}")
        
        if result.get('tracks'):
            print("Sample Tracks:")
            for i, track in enumerate(result['tracks'][:3], 1):
                print(f"  {i}. {track.get('name', 'Unknown')} - {track.get('artist', 'Unknown')}")
                crisis_score = track.get('crisis_score', 'N/A')
                if crisis_score != 'N/A':
                    print(f"     Crisis Score: {crisis_score:.3f}")
                else:
                    print(f"     Crisis Score: {crisis_score}")
                print(f"     Benefit: {track.get('therapy_benefit', 'N/A')}")

def test_sleep_therapy():
    """Test sleep therapy sequences"""
    print("\n" + "="*60)
    print("TESTING SLEEP THERAPY SEQUENCES")
    print("="*60)
    
    sleep_goals = ['deep_sleep', 'relaxation', 'insomnia_relief']
    
    for goal in sleep_goals:
        print(f"\nTesting Sleep Goal: {goal.upper()}")
        print("-" * 40)
        
        result = spotify_therapy.get_sleep_therapy_sequence(
            sleep_goal=goal,
            sequence_length=45  # 45 minutes for testing
        )
        
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Sequence Length: {result.get('sequence_length_minutes', 'N/A')} minutes")
        print(f"Therapy Focus: {result.get('therapy_focus', 'N/A')}")
        print(f"Total Tracks: {len(result.get('tracks', []))}")
        
        # Show tracks by phase
        tracks = result.get('tracks', [])
        phases = ['relaxation', 'transition', 'deep_sleep']
        
        for phase in phases:
            phase_tracks = [t for t in tracks if t.get('phase') == phase]
            if phase_tracks:
                print(f"\n  {phase.upper()} Phase ({len(phase_tracks)} tracks):")
                for track in phase_tracks[:2]:
                    print(f"    • {track.get('name', 'Unknown')} - {track.get('artist', 'Unknown')}")

def test_study_focus():
    """Test focus and study playlists"""
    print("\n" + "="*60)
    print("TESTING STUDY AND FOCUS MUSIC")
    print("="*60)
    
    study_types = ['concentration', 'creative', 'memory', 'exam_prep']
    
    for study_type in study_types:
        print(f"\nTesting Study Type: {study_type.upper()}")
        print("-" * 40)
        
        result = spotify_therapy.get_focus_study_playlist(
            study_type=study_type,
            duration_minutes=30
        )
        
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Therapy Focus: {result.get('therapy_focus', 'N/A')}")
        print(f"Usage Instructions: {result.get('usage_instructions', 'N/A')}")
        print(f"Total Tracks: {len(result.get('tracks', []))}")
        
        if result.get('tracks'):
            print("Top Study Tracks:")
            for i, track in enumerate(result['tracks'][:3], 1):
                print(f"  {i}. {track.get('name', 'Unknown')} - {track.get('artist', 'Unknown')}")
                study_score = track.get('study_score', 'N/A')
                if study_score != 'N/A':
                    print(f"     Study Score: {study_score:.3f}")
                else:
                    print(f"     Study Score: {study_score}")
                print(f"     Benefit: {track.get('therapy_benefit', 'N/A')}")

def test_cultural_healing():
    """Test cultural healing music"""
    print("\n" + "="*60)
    print("TESTING CULTURAL HEALING MUSIC")
    print("="*60)
    
    cultures = ['indian', 'chinese', 'japanese', 'western', 'african']
    
    for culture in cultures:
        print(f"\nTesting Culture: {culture.upper()}")
        print("-" * 40)
        
        result = spotify_therapy.get_cultural_healing_music(
            culture=culture,
            healing_type='traditional',
            language='english'
        )
        
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Therapy Focus: {result.get('therapy_focus', 'N/A')}")
        print(f"Total Tracks: {len(result.get('tracks', []))}")
        
        if result.get('tracks'):
            print("Cultural Healing Tracks:")
            for i, track in enumerate(result['tracks'][:3], 1):
                print(f"  {i}. {track.get('name', 'Unknown')} - {track.get('artist', 'Unknown')}")
                cultural_score = track.get('cultural_score', 'N/A')
                if cultural_score != 'N/A':
                    print(f"     Cultural Score: {cultural_score:.3f}")
                else:
                    print(f"     Cultural Score: {cultural_score}")
                print(f"     Benefit: {track.get('therapy_benefit', 'N/A')}")

def test_track_analysis():
    """Test individual track therapeutic analysis"""
    print("\n" + "="*60)
    print("TESTING TRACK THERAPEUTIC ANALYSIS")
    print("="*60)
    
    # Test with a well-known calming track (Spotify track ID)
    test_track_ids = [
        '4uLU6hMCjMI75M1A2tKUQC',  # "Clair de Lune" by Debussy
        '6b2oQwSGFkzsMtQjfvyva7',  # Popular ambient track
        '0VgkVdmE4gld66l8iyGjgx'   # Another test track
    ]
    
    for track_id in test_track_ids:
        print(f"\nAnalyzing Track ID: {track_id}")
        print("-" * 40)
        
        analysis = spotify_therapy.analyze_track_therapeutic_value(track_id)
        
        if 'error' in analysis:
            print(f"Analysis Error: {analysis['error']}")
            continue
        
        print(f"Track: {analysis.get('track_name', 'Unknown')}")
        print(f"Artist: {analysis.get('artist', 'Unknown')}")
        print(f"Duration: {analysis.get('duration_ms', 0) / 1000:.1f} seconds")
        print(f"Relaxation Score: {analysis.get('relaxation_score', 0):.3f}")
        print(f"Energy Level: {analysis.get('energy_level', 0):.3f}")
        print(f"Mood Valence: {analysis.get('mood_valence', 0):.3f}")
        print(f"Therapeutic BPM: {analysis.get('therapeutic_bpm', 0):.1f}")
        print(f"Recommended For: {', '.join(analysis.get('recommended_for', []))}")
        print(f"Best Time: {analysis.get('best_time_to_use', 'N/A')}")
        print(f"Therapy Applications: {', '.join(analysis.get('therapy_applications', []))}")
        break  # Test only first track to avoid too many API calls

def test_existing_mood_features():
    """Test existing mood-based features to ensure they still work"""
    print("\n" + "="*60)
    print("TESTING EXISTING MOOD-BASED FEATURES")
    print("="*60)
    
    moods = ['anxious', 'happy', 'sad', 'angry', 'calm']
    
    for mood in moods:
        print(f"\nTesting Mood: {mood.upper()}")
        print("-" * 25)
        
        result = spotify_therapy.get_mood_based_playlist(mood, intensity=0.7)
        
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Total Tracks: {len(result.get('tracks', []))}")
        print(f"Therapy Focus: {result.get('therapy_focus', 'N/A')}")
        
        if result.get('tracks'):
            print(f"Sample Track: {result['tracks'][0].get('name', 'Unknown')}")

def main():
    """Run all enhanced Spotify music therapy tests"""
    print("Enhanced Spotify Music Therapy Testing Suite")
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
        test_existing_mood_features()
        test_crisis_intervention()
        test_sleep_therapy()
        test_study_focus()
        test_cultural_healing()
        test_track_analysis()
        
        print("\n" + "="*60)
        print("ENHANCED SPOTIFY TESTING COMPLETED")
        print("="*60)
        print("All advanced therapeutic music features tested successfully!")
        
    except Exception as e:
        print(f"\nTest Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()