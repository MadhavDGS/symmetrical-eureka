# Spotify Integration for Art & Music Therapy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

class SpotifyMusicTherapy:
    def __init__(self):
        # Set up Spotify credentials
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if self.client_id and self.client_secret:
            self.spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            ))
        else:
            self.spotify = None
    
    def get_mood_playlists(self, mood):
        """Get Spotify playlists based on mood"""
        if not self.spotify:
            return self.get_fallback_playlists(mood)
        
        try:
            # Mood-based search queries
            mood_queries = {
                'happy': ['happy hits', 'feel good', 'upbeat', 'energetic music'],
                'sad': ['sad songs', 'melancholy', 'emotional ballads', 'healing music'],
                'anxious': ['calming music', 'anxiety relief', 'peaceful sounds', 'relaxation'],
                'calm': ['peaceful piano', 'meditation music', 'ambient sounds', 'nature sounds'],
                'focused': ['focus music', 'study beats', 'concentration', 'lo-fi hip hop'],
                'motivated': ['workout music', 'motivational songs', 'pump up', 'energy boost']
            }
            
            playlists = []
            for query in mood_queries.get(mood, ['relaxing music']):
                results = self.spotify.search(q=query, type='playlist', limit=5)
                for playlist in results['playlists']['items']:
                    playlists.append({
                        'name': playlist['name'],
                        'description': playlist['description'],
                        'url': playlist['external_urls']['spotify'],
                        'embed_url': f"https://open.spotify.com/embed/playlist/{playlist['id']}",
                        'image': playlist['images'][0]['url'] if playlist['images'] else None,
                        'tracks_total': playlist['tracks']['total']
                    })
            
            return playlists[:6]  # Return top 6 playlists
            
        except Exception as e:
            print(f"Spotify API error: {e}")
            return self.get_fallback_playlists(mood)
    
    def get_fallback_playlists(self, mood):
        """Fallback curated playlists when Spotify API is unavailable"""
        fallback_playlists = {
            'happy': [
                {'name': 'Feel Good Friday', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC', 'description': 'Uplifting pop hits'},
                {'name': 'Happy Hits!', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd', 'description': 'Songs to make you smile'},
                {'name': 'Good Vibes', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX9XIFQuFvzM4', 'description': 'Positive energy music'}
            ],
            'sad': [
                {'name': 'Life Sucks', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX3YSRoSdA634', 'description': 'For when you need to cry it out'},
                {'name': 'Sad Songs', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1', 'description': 'Emotional healing through music'},
                {'name': 'Melancholy', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX3Ogo9pFvBkY', 'description': 'Beautiful sad songs'}
            ],
            'anxious': [
                {'name': 'Peaceful Piano', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwAYIy1', 'description': 'Calming piano melodies'},
                {'name': 'Deep Sleep', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DWZeKCadgRdKQ', 'description': 'Relaxing sounds for anxiety'},
                {'name': 'Calm Vibes', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX1s9knjP51Oa', 'description': 'Stress-relieving music'}
            ],
            'calm': [
                {'name': 'Peaceful Guitar', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DWVFeEut75IAL', 'description': 'Gentle acoustic guitar'},
                {'name': 'Nature Sounds', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX6VdMW310YC7', 'description': 'Sounds of nature for peace'},
                {'name': 'Meditation Music', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DWZqd5JICZI0u', 'description': 'Music for mindfulness'}
            ],
            'focused': [
                {'name': 'Deep Focus', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DWZeKCadgRdKQ', 'description': 'Instrumental focus music'},
                {'name': 'Brain Food', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DWWQRwui0ExPn', 'description': 'Lo-fi beats for studying'},
                {'name': 'Concentration', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX8Uebhn9wzrS', 'description': 'Music to enhance focus'}
            ],
            'motivated': [
                {'name': 'Power Workout', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX76Wlfdnj7AP', 'description': 'High-energy workout music'},
                {'name': 'Beast Mode', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX32NsLKyzScr', 'description': 'Motivational pump-up songs'},
                {'name': 'Confidence Boost', 'url': 'https://open.spotify.com/playlist/37i9dQZF1DX9oh43oAzkyx', 'description': 'Music to boost confidence'}
            ]
        }
        
        return fallback_playlists.get(mood, fallback_playlists['calm'])

# Usage example
def get_spotify_credentials():
    """
    To use Spotify API:
    1. Go to https://developer.spotify.com/dashboard/
    2. Create a new app
    3. Get Client ID and Client Secret
    4. Set environment variables:
       SPOTIFY_CLIENT_ID=your_client_id
       SPOTIFY_CLIENT_SECRET=your_client_secret
    """
    pass