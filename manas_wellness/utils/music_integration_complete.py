# Multiple Music Integration Options for Art & Music Therapy

"""
🎵 MUSIC INTEGRATION OPTIONS FOR MOOD-BASED THERAPY

1. SPOTIFY WEB API (Best Option)
2. YouTube Music API 
3. Apple Music API
4. Free Music APIs
5. Embedded Players
6. Local Audio Files

Each option has different benefits and requirements.
"""

# =============================================================================
# 1. SPOTIFY INTEGRATION (Recommended)
# =============================================================================

# Requirements:
# pip install spotipy
# Get credentials from: https://developer.spotify.com/dashboard/

import os
import json
import requests
from typing import List, Dict

class MusicTherapyIntegration:
    
    def __init__(self):
        self.setup_all_integrations()
    
    def setup_all_integrations(self):
        """Setup all available music integrations"""
        self.spotify_setup()
        self.youtube_setup()
        self.freemium_setup()
    
    # =============================================================================
    # SPOTIFY INTEGRATION
    # =============================================================================
    
    def spotify_setup(self):
        """Setup Spotify integration"""
        try:
            import spotipy
            from spotipy.oauth2 import SpotifyClientCredentials
            
            client_id = os.getenv('SPOTIFY_CLIENT_ID')
            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
            
            if client_id and client_secret:
                self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
                    client_id=client_id, client_secret=client_secret
                ))
                self.spotify_available = True
            else:
                self.spotify_available = False
                print("Spotify credentials not found. Using fallback playlists.")
                
        except ImportError:
            self.spotify_available = False
            print("Spotipy not installed. Using fallback playlists.")
    
    def get_spotify_playlists(self, mood: str) -> List[Dict]:
        """Get real Spotify playlists based on mood"""
        if not self.spotify_available:
            return []
        
        mood_searches = {
            'happy': ['happy', 'upbeat', 'feel good', 'positive vibes'],
            'sad': ['sad', 'melancholy', 'emotional', 'healing'],
            'anxious': ['calm', 'relaxing', 'peaceful', 'anxiety relief'],
            'calm': ['peaceful', 'meditation', 'ambient', 'zen'],
            'focused': ['focus', 'concentration', 'study', 'productive'],
            'motivated': ['workout', 'energy', 'pump up', 'motivational']
        }
        
        try:
            search_terms = mood_searches.get(mood, ['relaxing'])
            playlists = []
            
            for term in search_terms[:2]:  # Search top 2 terms per mood
                results = self.spotify.search(q=f'{term} playlist', type='playlist', limit=3)
                
                for playlist in results['playlists']['items']:
                    playlists.append({
                        'name': playlist['name'],
                        'description': playlist['description'] or f'Great {mood} music',
                        'url': playlist['external_urls']['spotify'],
                        'embed_url': f"https://open.spotify.com/embed/playlist/{playlist['id']}?utm_source=generator&theme=0",
                        'image': playlist['images'][0]['url'] if playlist['images'] else None,
                        'tracks': playlist['tracks']['total'],
                        'source': 'spotify'
                    })
            
            return playlists[:6]  # Return top 6
            
        except Exception as e:
            print(f"Spotify API error: {e}")
            return []
    
    # =============================================================================
    # YOUTUBE MUSIC INTEGRATION
    # =============================================================================
    
    def youtube_setup(self):
        """Setup YouTube Music integration"""
        self.youtube_api_key = os.getenv('YOUTUBE_API_KEY')
        self.youtube_available = bool(self.youtube_api_key)
    
    def get_youtube_playlists(self, mood: str) -> List[Dict]:
        """Get YouTube playlists based on mood"""
        if not self.youtube_available:
            return self.get_youtube_fallback_playlists(mood)
        
        # YouTube API v3 integration
        mood_queries = {
            'happy': 'happy upbeat music playlist',
            'sad': 'sad emotional music playlist',
            'anxious': 'calming relaxing music playlist',
            'calm': 'peaceful meditation music playlist',
            'focused': 'focus study music playlist',
            'motivated': 'workout motivation music playlist'
        }
        
        try:
            query = mood_queries.get(mood, 'relaxing music playlist')
            url = f"https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'playlist',
                'key': self.youtube_api_key,
                'maxResults': 6
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            playlists = []
            for item in data.get('items', []):
                playlists.append({
                    'name': item['snippet']['title'],
                    'description': item['snippet']['description'][:100] + '...',
                    'url': f"https://www.youtube.com/playlist?list={item['id']['playlistId']}",
                    'embed_url': f"https://www.youtube.com/embed/videoseries?list={item['id']['playlistId']}",
                    'image': item['snippet']['thumbnails']['medium']['url'],
                    'source': 'youtube'
                })
            
            return playlists
            
        except Exception as e:
            print(f"YouTube API error: {e}")
            return self.get_youtube_fallback_playlists(mood)
    
    def get_youtube_fallback_playlists(self, mood: str) -> List[Dict]:
        """Fallback YouTube playlists"""
        fallback_playlists = {
            'happy': [
                {'name': 'Happy Pop Hits 2024', 'url': 'https://www.youtube.com/playlist?list=PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI'},
                {'name': 'Feel Good Music', 'url': 'https://www.youtube.com/playlist?list=PLw-VjHDlEOgs658kAHR_LAaILBXb-s6Q5'},
                {'name': 'Upbeat Workout Songs', 'url': 'https://www.youtube.com/playlist?list=PLFgquLnL59akA2PflkTWDqVdpCBxiWXps'}
            ],
            'sad': [
                {'name': 'Sad Songs That Make You Cry', 'url': 'https://www.youtube.com/playlist?list=PLFgquLnL59amWJRsL7aqeMRF7rlPxiCR7'},
                {'name': 'Emotional Piano Music', 'url': 'https://www.youtube.com/playlist?list=PLYnoQPmXU84SBNJFl23DCNzk0KE2UOmPF'},
                {'name': 'Healing Music for the Soul', 'url': 'https://www.youtube.com/playlist?list=PLFgquLnL59alx4OzqCKqBggCGkXPxJNdD'}
            ],
            'anxious': [
                {'name': 'Calming Music for Anxiety', 'url': 'https://www.youtube.com/playlist?list=PLU0YLAlgR0Vgu3TF1OwQj2WVqIgOXd6b1'},
                {'name': 'Peaceful Nature Sounds', 'url': 'https://www.youtube.com/playlist?list=PLAmEaWwM7xpgbvAOEBDOIoJ06t6h5W_CJ'},
                {'name': 'Deep Breathing Meditation', 'url': 'https://www.youtube.com/playlist?list=PLv-LK3dxq0vXLkLW2sDjTMIq8VJr0Bj6b'}
            ],
            'calm': [
                {'name': 'Peaceful Piano Music', 'url': 'https://www.youtube.com/playlist?list=PLu7SwobRFGE2b3xhLaJC2TQPXz_2v5cFr'},
                {'name': 'Ambient Relaxation Music', 'url': 'https://www.youtube.com/playlist?list=PLrpb8VJd2g3dYZDOQ8_L6c0mOHdO6O1w1'},
                {'name': 'Ocean Waves and Rain', 'url': 'https://www.youtube.com/playlist?list=PLAmEaWwM7xpgbvAOEBDOIoJ06t6h5W_CJ'}
            ],
            'focused': [
                {'name': 'Lo-Fi Hip Hop Study Music', 'url': 'https://www.youtube.com/playlist?list=PLt47jlGKRIGFqNsePeOp8KSQj3_2c4j9v'},
                {'name': 'Deep Focus Instrumental', 'url': 'https://www.youtube.com/playlist?list=PLAmEaWwM7xpgbvAOEBDOIoJ06t6h5W_CJ'},
                {'name': 'Classical Music for Studying', 'url': 'https://www.youtube.com/playlist?list=PLTQaq0BaNIbyFd_jkYJ5Pm1I2qO3-NrfG'}
            ],
            'motivated': [
                {'name': 'Epic Workout Music', 'url': 'https://www.youtube.com/playlist?list=PLFgquLnL59akVg_GxxjcuNKw4XJkAqzFo'},
                {'name': 'Pump Up Songs 2024', 'url': 'https://www.youtube.com/playlist?list=PLnI6NKPOzNy4hggCl9jmxnp6b5gRwVoJF'},
                {'name': 'Motivational Music Mix', 'url': 'https://www.youtube.com/playlist?list=PLFgquLnL59amWJRsL7aqeMRF7rlPxiCR7'}
            ]
        }
        
        return fallback_playlists.get(mood, fallback_playlists['calm'])
    
    # =============================================================================
    # FREE MUSIC APIs (No Authentication Required)
    # =============================================================================
    
    def freemium_setup(self):
        """Setup free music APIs"""
        self.freemium_available = True
    
    def get_freemium_music(self, mood: str) -> List[Dict]:
        """Get music from free APIs and services"""
        
        # Free Music Archive playlists
        fma_playlists = {
            'happy': [
                {'name': 'FMA Happy Vibes', 'url': 'https://freemusicarchive.org/search?adv=1&music-filter-tag=happy', 'description': 'Uplifting tracks from FMA'},
                {'name': 'Upbeat Electronic', 'url': 'https://freemusicarchive.org/search?adv=1&music-filter-genre=Electronic', 'description': 'Electronic music for good vibes'}
            ],
            'calm': [
                {'name': 'FMA Ambient Collection', 'url': 'https://freemusicarchive.org/search?adv=1&music-filter-genre=Ambient', 'description': 'Peaceful ambient music'},
                {'name': 'Classical Guitar', 'url': 'https://freemusicarchive.org/search?adv=1&music-filter-genre=Classical', 'description': 'Soothing guitar pieces'}
            ]
        }
        
        # Internet Radio stations by mood
        radio_stations = {
            'happy': [
                {'name': 'SomaFM Groove Salad', 'url': 'https://somafm.com/groovesalad/', 'description': 'Downtempo and ambient grooves'},
                {'name': 'Radio Swiss Jazz', 'url': 'https://www.radioswissjazz.ch/', 'description': 'Feel-good jazz music'}
            ],
            'calm': [
                {'name': 'Hearts of Space', 'url': 'https://hos.com/', 'description': 'Ambient and space music'},
                {'name': 'Calm Radio Nature', 'url': 'https://calmradio.com/', 'description': 'Nature sounds and ambient music'}
            ],
            'focused': [
                {'name': 'Brain.fm', 'url': 'https://brain.fm/', 'description': 'Scientifically designed focus music'},
                {'name': 'Noisli', 'url': 'https://www.noisli.com/', 'description': 'Background noise for concentration'}
            ]
        }
        
        return fma_playlists.get(mood, []) + radio_stations.get(mood, [])
    
    # =============================================================================
    # EMBEDDED PLAYERS (iframe integration)
    # =============================================================================
    
    def get_embedded_players(self, mood: str) -> List[Dict]:
        """Get embeddable music players for direct integration"""
        
        embedded_options = {
            'happy': [
                {
                    'name': 'Happy Hits Spotify',
                    'embed_code': '<iframe src="https://open.spotify.com/embed/playlist/37i9dQZF1DXdPec7aLTmlC" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>',
                    'description': 'Spotify happy hits playlist'
                },
                {
                    'name': 'Upbeat YouTube Mix',
                    'embed_code': '<iframe width="300" height="200" src="https://www.youtube.com/embed/videoseries?list=PLrpb8VJd2g3dYZDOQ8_L6c0mOHdO6O1w1" frameborder="0" allowfullscreen></iframe>',
                    'description': 'YouTube upbeat music mix'
                }
            ],
            'calm': [
                {
                    'name': 'Peaceful Piano Spotify',
                    'embed_code': '<iframe src="https://open.spotify.com/embed/playlist/37i9dQZF1DX4sWSpwAYIy1" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>',
                    'description': 'Spotify peaceful piano playlist'
                },
                {
                    'name': 'Nature Sounds YouTube',
                    'embed_code': '<iframe width="300" height="200" src="https://www.youtube.com/embed/UNXLbbUyWrQ" frameborder="0" allowfullscreen></iframe>',
                    'description': 'Calming nature sounds'
                }
            ]
        }
        
        return embedded_options.get(mood, embedded_options['calm'])
    
    # =============================================================================
    # MAIN INTEGRATION METHOD
    # =============================================================================
    
    def get_mood_music(self, mood: str, source_preference: str = 'all') -> Dict:
        """
        Get music recommendations for a specific mood
        
        Args:
            mood: 'happy', 'sad', 'anxious', 'calm', 'focused', 'motivated'
            source_preference: 'spotify', 'youtube', 'freemium', 'all'
        
        Returns:
            Dictionary with playlists from various sources
        """
        
        results = {
            'mood': mood,
            'spotify_playlists': [],
            'youtube_playlists': [],
            'freemium_options': [],
            'embedded_players': []
        }
        
        if source_preference in ['spotify', 'all']:
            results['spotify_playlists'] = self.get_spotify_playlists(mood)
        
        if source_preference in ['youtube', 'all']:
            results['youtube_playlists'] = self.get_youtube_playlists(mood)
        
        if source_preference in ['freemium', 'all']:
            results['freemium_options'] = self.get_freemium_music(mood)
        
        if source_preference in ['embedded', 'all']:
            results['embedded_players'] = self.get_embedded_players(mood)
        
        return results

# Usage example
if __name__ == "__main__":
    music_therapy = MusicTherapyIntegration()
    
    # Get all music options for 'happy' mood
    happy_music = music_therapy.get_mood_music('happy', 'all')
    print(json.dumps(happy_music, indent=2))