"""
Real Spotify Music Therapy Integration
Replaces dummy music recommendations with actual Spotify API
"""

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import session
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SpotifyMusicTherapy:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if self.client_id and self.client_secret:
            try:
                client_credentials_manager = SpotifyClientCredentials(
                    client_id=self.client_id, 
                    client_secret=self.client_secret
                )
                self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
                self.is_connected = True
                logging.info("Spotify API connected successfully")
            except Exception as e:
                logging.error(f"Spotify connection failed: {e}")
                self.sp = None
                self.is_connected = False
        else:
            logging.warning(f"Spotify credentials not found: ID={self.client_id}, Secret={'***' if self.client_secret else None}")
            self.sp = None
            self.is_connected = False
    
    def get_mood_based_playlist(self, mood, intensity=0.5):
        """Generate playlist based on user's current mood"""
        if not self.is_connected:
            return self._get_fallback_playlist(mood)
        
        try:
            # Map moods to Spotify audio features and search terms
            mood_mapping = {
                'anxious': {'valence': 0.3, 'energy': 0.2, 'search_terms': ['anxiety relief', 'calming music', 'meditation']},
                'depressed': {'valence': 0.4, 'energy': 0.3, 'search_terms': ['healing music', 'uplifting gentle', 'emotional support']},
                'stressed': {'valence': 0.5, 'energy': 0.4, 'search_terms': ['stress relief', 'relaxation', 'peaceful']},
                'angry': {'valence': 0.2, 'energy': 0.8, 'search_terms': ['anger management', 'cooling down', 'peaceful']},
                'happy': {'valence': 0.8, 'energy': 0.7, 'search_terms': ['happy music', 'uplifting', 'positive vibes']},
                'calm': {'valence': 0.6, 'energy': 0.3, 'search_terms': ['calm music', 'peaceful', 'meditation']},
                'energetic': {'valence': 0.8, 'energy': 0.9, 'search_terms': ['energetic', 'upbeat', 'motivational']},
                'sad': {'valence': 0.2, 'energy': 0.2, 'search_terms': ['sad music', 'melancholy', 'emotional']},
                'focused': {'valence': 0.5, 'energy': 0.4, 'search_terms': ['focus music', 'concentration', 'study']},
                'motivated': {'valence': 0.8, 'energy': 0.8, 'search_terms': ['motivational', 'workout', 'energizing']}
            }
            
            mood_params = mood_mapping.get(mood.lower(), mood_mapping['calm'])
            
            # Use search instead of recommendations to avoid API issues
            playlist = []
            search_terms = mood_params['search_terms']
            
            for search_term in search_terms:
                try:
                    results = self.sp.search(q=f"{search_term} instrumental", type='track', limit=7, market='US')
                    
                    for track in results['tracks']['items'][:5]:  # Limit per search
                        if len(playlist) < 15:  # Total limit
                            # Handle missing album images with fallback
                            image_url = None
                            if track['album']['images']:
                                image_url = track['album']['images'][0]['url']
                            else:
                                image_url = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjMURCOTU0Ii8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTUwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZmlsbD0iI0ZGRkZGRiIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE2cHgiPk11c2ljPC90ZXh0Pjwvc3ZnPgo='
                            
                            playlist.append({
                                'id': track['id'],
                                'name': track['name'],
                                'artist': track['artists'][0]['name'],
                                'duration_ms': track['duration_ms'],
                                'preview_url': track['preview_url'],
                                'external_url': track['external_urls']['spotify'],
                                'image_url': image_url,
                                'therapy_benefit': self._get_therapy_benefit(mood, track)
                            })
                except Exception as e:
                    logging.error(f"Search error for {search_term}: {e}")
                    continue
            
            # Fallback if no tracks found
            if not playlist:
                return self._get_fallback_playlist(mood)
            
            return {
                'mood': mood,
                'tracks': playlist,
                'total_duration': sum(t['duration_ms'] for t in playlist),
                'therapy_focus': self._get_therapy_focus(mood),
                'source': 'spotify'
            }
            
        except Exception as e:
            logging.error(f"Spotify API error: {e}")
            return self._get_fallback_playlist(mood)
    
    def search_therapeutic_music(self, query, mood_context=None):
        """Search for therapeutic music tracks based on query"""
        if not self.is_connected:
            return self._get_fallback_search_results(query)
        
        try:
            results = self.sp.search(q=query, type='track', limit=20)
            
            tracks = []
            for track in results['tracks']['items']:
                # Handle missing album images with fallback using base64 SVG
                images = track['album']['images'] if track['album']['images'] else [
                    {'url': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjMURCOTU0Ii8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTUwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZmlsbD0iI0ZGRkZGRiIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE2cHgiPlRyYWNrPC90ZXh0Pjwvc3ZnPgo='}
                ]
                
                track_data = {
                    'id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'url': track['external_urls']['spotify'],
                    'preview_url': track['preview_url'],
                    'duration_ms': track['duration_ms'],
                    'popularity': track['popularity'],
                    'images': images,
                    'external_urls': track['external_urls']
                }
                
                if mood_context:
                    track_data['therapy_benefit'] = self._get_therapy_benefit(mood_context, track)
                
                tracks.append(track_data)
            
            return {
                'results': tracks,
                'source': 'spotify_api',
                'query': query
            }
        
        except Exception as e:
            logging.error(f"Spotify search error: {e}")
            return self._get_fallback_search_results(query)
    
    def search_playlists(self, query, limit=10):
        """Search for therapeutic playlists based on query"""
        if not self.is_connected:
            return self._get_fallback_playlist_search(query)
        
        try:
            results = self.sp.search(q=query, type='playlist', limit=limit)
            
            playlists = []
            if results and 'playlists' in results and results['playlists']['items']:
                for playlist in results['playlists']['items']:
                    if not playlist:  # Skip None playlists
                        continue
                        
                    # Handle missing images with fallback using base64 SVG
                    images = playlist.get('images', [])
                    if not images:
                        images = [{'url': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjMURCOTU0Ii8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTUwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZmlsbD0iI0ZGRkZGRiIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE0cHgiPlBsYXlsaXN0PC90ZXh0Pjwvc3ZnPgo='}]
                    
                    # Handle missing description
                    description = playlist.get('description', f"Curated playlist: {playlist.get('name', 'Untitled')}")
                    
                    # Handle missing owner display name
                    owner_info = playlist.get('owner', {})
                    owner_name = owner_info.get('display_name') or owner_info.get('id', 'Unknown')
                    
                    playlist_data = {
                        'id': playlist.get('id', ''),
                        'name': playlist.get('name', 'Untitled Playlist'),
                        'description': description,
                        'url': playlist.get('external_urls', {}).get('spotify', ''),
                        'images': images,
                        'tracks_total': playlist.get('tracks', {}).get('total', 0),
                        'owner': owner_name,
                        'external_urls': playlist.get('external_urls', {})
                    }
                    
                    playlists.append(playlist_data)
            
            return {
                'results': playlists,
                'source': 'spotify_api',
                'query': query
            }
        
        except Exception as e:
            logging.error(f"Spotify playlist search error: {e}")
            return self._get_fallback_playlist_search(query)
    
    def _get_fallback_playlist_search(self, query):
        """Fallback playlists when API is not available"""
        fallback_playlists = [
            {
                'id': '37i9dQZF1DX4sWSpwAYIy1',
                'name': 'Peaceful Piano',
                'description': 'Soothing piano melodies for relaxation',
                'url': 'https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwAYIy1',
                'images': [{'url': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjMURCOTU0Ii8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTUwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZmlsbD0iI0ZGRkZGRiIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE0cHgiPvCflosgUGlhbm88L3RleHQ+PC9zdmc+Cg=='}],
                'tracks_total': 100,
                'owner': 'Spotify'
            },
            {
                'id': '37i9dQZF1DWZeKCadgRdKQ', 
                'name': 'Deep Focus',
                'description': 'Keep calm and focus with ambient music',
                'url': 'https://open.spotify.com/playlist/37i9dQZF1DWZeKCadgRdKQ',
                'images': [{'url': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjMURCOTU0Ii8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTUwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZmlsbD0iI0ZGRkZGRiIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE0cHgiPvCfjK8gRm9jdXM8L3RleHQ+PC9zdmc+Cg=='}],
                'tracks_total': 150,
                'owner': 'Spotify'
            },
            {
                'id': 'fallback_meditation',
                'name': 'Meditation & Mindfulness',
                'description': 'Calming meditation music for inner peace',
                'url': 'https://open.spotify.com',
                'images': [{'url': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjMURCOTU0Ii8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTUwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZmlsbD0iI0ZGRkZGRiIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjEycHgiPvCfp5og4oCuTWVkaXRhdGU8L3RleHQ+PC9zdmc+Cg=='}],
                'tracks_total': 80,
                'owner': 'Spotify'
            },
            {
                'id': 'fallback_nature',
                'name': 'Nature Sounds',
                'description': 'Relaxing nature sounds for stress relief',
                'url': 'https://open.spotify.com',
                'images': [{'url': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjMwMCIgdmlld0JveD0iMCAwIDMwMCAzMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMzAwIiBmaWxsPSIjMURCOTU0Ii8+Cjx0ZXh0IHg9IjE1MCIgeT0iMTUwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZmlsbD0iI0ZGRkZGRiIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE0cHgiPvCfj7ggTmF0dXJlPC90ZXh0Pjwvc3ZnPgo='}],
                'tracks_total': 120,
                'owner': 'Spotify'
            }
        ]
        
        return {
            'results': fallback_playlists,
            'source': 'fallback',
            'query': query
        }
    
    def _get_therapy_benefit(self, mood, track):
        """Determine therapeutic benefit of track for specific mood"""
        benefits = {
            'anxious': 'Promotes relaxation and reduces anxiety',
            'depressed': 'Uplifts mood and provides emotional support',
            'stressed': 'Helps with stress relief and mindfulness',
            'angry': 'Channels emotions constructively',
            'calm': 'Maintains peaceful state of mind',
            'sad': 'Provides comfort and emotional processing'
        }
        return benefits.get(mood.lower(), 'Supports overall mental wellness')
    
    def _get_therapy_focus(self, mood):
        """Get therapy focus description"""
        focus = {
            'anxious': 'Anxiety reduction through calming melodies',
            'depressed': 'Mood elevation through uplifting rhythms',
            'stressed': 'Stress relief through mindful listening',
            'angry': 'Emotional regulation through music therapy',
            'calm': 'Mindfulness enhancement through ambient sounds',
            'sad': 'Emotional processing through therapeutic music'
        }
        return focus.get(mood.lower(), 'General wellness support')
    
    def _calculate_therapeutic_score(self, track):
        """Calculate how therapeutically beneficial a track might be"""
        # Simple scoring based on track characteristics
        # In a real implementation, this could be more sophisticated
        score = 7.5  # Base score
        
        # Adjust based on track name keywords
        therapeutic_keywords = ['calm', 'peace', 'relax', 'meditation', 'healing', 'gentle']
        track_name_lower = track['name'].lower()
        
        for keyword in therapeutic_keywords:
            if keyword in track_name_lower:
                score += 0.5
        
        return min(score, 10.0)
    
    def _get_fallback_playlist(self, mood):
        """Fallback playlist when Spotify is not available"""
        fallback_tracks = {
            'anxious': [
                {'name': 'Calm Mind', 'artist': 'Nature Sounds', 'therapy_benefit': 'Reduces anxiety'},
                {'name': 'Peaceful Breathing', 'artist': 'Meditation Music', 'therapy_benefit': 'Promotes relaxation'},
                {'name': 'Gentle Waves', 'artist': 'Ocean Therapy', 'therapy_benefit': 'Soothes nervous system'}
            ],
            'happy': [
                {'name': 'Uplifting Melody', 'artist': 'Positive Vibes', 'therapy_benefit': 'Maintains positive mood'},
                {'name': 'Joyful Rhythms', 'artist': 'Happiness Music', 'therapy_benefit': 'Enhances well-being'},
                {'name': 'Bright Day', 'artist': 'Sunshine Sounds', 'therapy_benefit': 'Boosts energy'}
            ]
        }
        
        tracks = fallback_tracks.get(mood.lower(), fallback_tracks['anxious'])
        
        return {
            'mood': mood,
            'tracks': tracks,
            'total_duration': 180000,  # 3 minutes fallback
            'therapy_focus': self._get_therapy_focus(mood),
            'source': 'fallback'
        }
    
    def _get_fallback_search_results(self, query):
        """Fallback search results"""
        return {
            'query': query,
            'results': [
                {'name': f'Therapeutic {query}', 'artist': 'Wellness Music', 'therapeutic_score': 8.0}
            ],
            'source': 'fallback'
        }

    def get_crisis_intervention_playlist(self, crisis_level='high', duration_minutes=15):
        """Emergency calming music for crisis situations"""
        if not self.is_connected:
            return self._get_crisis_fallback_playlist(crisis_level)
        
        try:
            # Crisis-specific music parameters
            crisis_params = {
                'high': {
                    'valence': 0.1, 'energy': 0.1, 'tempo': '60-70',
                    'genres': ['ambient', 'new-age', 'classical'],
                    'keywords': ['healing', 'calm', 'peace', 'meditation']
                },
                'medium': {
                    'valence': 0.3, 'energy': 0.2, 'tempo': '70-80',
                    'genres': ['instrumental', 'acoustic', 'folk'],
                    'keywords': ['comfort', 'gentle', 'soothing']
                },
                'low': {
                    'valence': 0.5, 'energy': 0.3, 'tempo': '80-90',
                    'genres': ['indie', 'alternative', 'pop'],
                    'keywords': ['hope', 'support', 'understanding']
                }
            }
            
            params = crisis_params.get(crisis_level, crisis_params['high'])
            tracks = []
            
            # Search for crisis intervention music
            for keyword in params['keywords']:
                results = self.sp.search(
                    q=f"{keyword} instrumental peaceful",
                    type='track',
                    limit=5,
                    market='US'
                )
                tracks.extend(results['tracks']['items'])
            
            # Filter and sort by audio features for crisis intervention
            analyzed_tracks = []
            for track in tracks[:20]:  # Analyze top 20
                try:
                    features = self.sp.audio_features(track['id'])
                    if features and features[0]:
                        feature = features[0]
                        # Crisis score based on calming attributes
                        crisis_score = (
                            (1 - feature['energy']) * 0.3 +
                            (1 - feature['valence']) * 0.2 +
                            (feature['acousticness']) * 0.3 +
                            (feature['instrumentalness']) * 0.2
                        )
                        analyzed_tracks.append({
                            'track': track,
                            'crisis_score': crisis_score,
                            'features': feature
                        })
                except:
                    continue
            
            # Sort by crisis intervention effectiveness
            analyzed_tracks.sort(key=lambda x: x['crisis_score'], reverse=True)
            
            selected_tracks = []
            total_duration = 0
            target_duration = duration_minutes * 60 * 1000
            
            for item in analyzed_tracks:
                if total_duration < target_duration:
                    track = item['track']
                    selected_tracks.append({
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'duration_ms': track['duration_ms'],
                        'crisis_score': item['crisis_score'],
                        'spotify_url': track['external_urls']['spotify'],
                        'preview_url': track['preview_url'],
                        'therapy_benefit': 'Crisis intervention and immediate calming'
                    })
                    total_duration += track['duration_ms']
            
            return {
                'crisis_level': crisis_level,
                'tracks': selected_tracks,
                'total_duration': total_duration,
                'therapy_focus': 'Crisis intervention and emotional stabilization',
                'usage_instructions': 'Use immediately during crisis. Focus on breathing while listening.',
                'source': 'spotify_crisis'
            }
            
        except Exception as e:
            logging.error(f"Crisis playlist error: {e}")
            return self._get_crisis_fallback_playlist(crisis_level)
    
    def get_sleep_therapy_sequence(self, sleep_goal='deep_sleep', sequence_length=90):
        """Generate therapeutic sleep sequence with gradual progression"""
        if not self.is_connected:
            return self._get_sleep_fallback_sequence(sleep_goal)
        
        try:
            sleep_phases = {
                'relaxation': {  # 0-30 minutes
                    'valence': 0.3, 'energy': 0.2, 'tempo': '60-80',
                    'genres': ['ambient', 'classical', 'new-age']
                },
                'transition': {  # 30-60 minutes
                    'valence': 0.2, 'energy': 0.1, 'tempo': '50-70',
                    'genres': ['ambient', 'drone', 'minimalist']
                },
                'deep_sleep': {  # 60-90 minutes
                    'valence': 0.1, 'energy': 0.05, 'tempo': '40-60',
                    'genres': ['ambient', 'sound-healing', 'nature-sounds']
                }
            }
            
            sequence_tracks = []
            phase_duration = sequence_length // 3  # Divide into 3 phases
            
            for phase_name, phase_params in sleep_phases.items():
                phase_tracks = []
                
                # Search for phase-specific music
                search_queries = [
                    f"sleep {phase_name} ambient",
                    f"meditation {phase_name}",
                    f"healing {phase_name} instrumental"
                ]
                
                for query in search_queries:
                    results = self.sp.search(q=query, type='track', limit=10)
                    phase_tracks.extend(results['tracks']['items'])
                
                # Analyze and select best tracks for this phase
                analyzed_phase_tracks = []
                for track in phase_tracks[:15]:
                    try:
                        features = self.sp.audio_features(track['id'])
                        if features and features[0]:
                            feature = features[0]
                            sleep_score = self._calculate_sleep_score(feature, phase_params)
                            analyzed_phase_tracks.append({
                                'track': track,
                                'sleep_score': sleep_score,
                                'phase': phase_name
                            })
                    except:
                        continue
                
                analyzed_phase_tracks.sort(key=lambda x: x['sleep_score'], reverse=True)
                
                # Select tracks for this phase
                phase_total_duration = 0
                phase_target = phase_duration * 60 * 1000
                
                for item in analyzed_phase_tracks:
                    if phase_total_duration < phase_target:
                        track = item['track']
                        sequence_tracks.append({
                            'name': track['name'],
                            'artist': track['artists'][0]['name'],
                            'duration_ms': track['duration_ms'],
                            'phase': phase_name,
                            'sleep_score': item['sleep_score'],
                            'spotify_url': track['external_urls']['spotify'],
                            'therapy_benefit': f'Sleep {phase_name} enhancement'
                        })
                        phase_total_duration += track['duration_ms']
            
            return {
                'sleep_goal': sleep_goal,
                'sequence_length_minutes': sequence_length,
                'tracks': sequence_tracks,
                'phases': list(sleep_phases.keys()),
                'therapy_focus': 'Progressive sleep induction and deep rest',
                'usage_instructions': 'Start 30 minutes before sleep. Use low volume.',
                'source': 'spotify_sleep_therapy'
            }
            
        except Exception as e:
            logging.error(f"Sleep therapy error: {e}")
            return self._get_sleep_fallback_sequence(sleep_goal)
    
    def get_focus_study_playlist(self, study_type='concentration', duration_minutes=60):
        """Academic stress relief and focus enhancement music"""
        if not self.is_connected:
            return self._get_study_fallback_playlist(study_type)
        
        try:
            study_mapping = {
                'concentration': {
                    'valence': 0.5, 'energy': 0.4, 'tempo': '70-90',
                    'genres': ['lo-fi', 'instrumental', 'classical'],
                    'keywords': ['focus', 'concentration', 'study', 'productivity']
                },
                'creative': {
                    'valence': 0.6, 'energy': 0.5, 'tempo': '80-100',
                    'genres': ['ambient', 'electronic', 'indie-folk'],
                    'keywords': ['creative', 'inspiration', 'flow', 'innovation']
                },
                'memory': {
                    'valence': 0.4, 'energy': 0.3, 'tempo': '60-80',
                    'genres': ['classical', 'baroque', 'minimalist'],
                    'keywords': ['memory', 'learning', 'retention', 'classical']
                },
                'exam_prep': {
                    'valence': 0.4, 'energy': 0.3, 'tempo': '50-70',
                    'genres': ['ambient', 'classical', 'meditation'],
                    'keywords': ['calm', 'confidence', 'clarity', 'focus']
                }
            }
            
            params = study_mapping.get(study_type, study_mapping['concentration'])
            tracks = []
            
            # Search for study music
            for keyword in params['keywords']:
                results = self.sp.search(
                    q=f"{keyword} instrumental study",
                    type='track',
                    limit=8,
                    market='US'
                )
                tracks.extend(results['tracks']['items'])
            
            # Analyze tracks for study effectiveness
            analyzed_tracks = []
            for track in tracks[:25]:
                try:
                    features = self.sp.audio_features(track['id'])
                    if features and features[0]:
                        feature = features[0]
                        study_score = self._calculate_study_score(feature, params)
                        analyzed_tracks.append({
                            'track': track,
                            'study_score': study_score,
                            'features': feature
                        })
                except:
                    continue
            
            analyzed_tracks.sort(key=lambda x: x['study_score'], reverse=True)
            
            selected_tracks = []
            total_duration = 0
            target_duration = duration_minutes * 60 * 1000
            
            for item in analyzed_tracks:
                if total_duration < target_duration:
                    track = item['track']
                    selected_tracks.append({
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'duration_ms': track['duration_ms'],
                        'study_score': item['study_score'],
                        'study_type': study_type,
                        'spotify_url': track['external_urls']['spotify'],
                        'preview_url': track['preview_url'],
                        'therapy_benefit': f'{study_type.title()} enhancement and stress reduction'
                    })
                    total_duration += track['duration_ms']
            
            return {
                'study_type': study_type,
                'tracks': selected_tracks,
                'total_duration': total_duration,
                'therapy_focus': f'Academic stress relief and {study_type} enhancement',
                'usage_instructions': f'Optimal for {study_type} sessions. Use consistent volume.',
                'source': 'spotify_study'
            }
            
        except Exception as e:
            logging.error(f"Study playlist error: {e}")
            return self._get_study_fallback_playlist(study_type)
    
    def get_cultural_healing_music(self, culture, healing_type='traditional', language='english'):
        """Cultural and regional healing music therapy"""
        if not self.is_connected:
            return self._get_cultural_fallback_playlist(culture, healing_type)
        
        try:
            cultural_mapping = {
                'indian': {
                    'instruments': ['sitar', 'tabla', 'flute', 'tanpura'],
                    'genres': ['classical', 'raga', 'devotional', 'meditation'],
                    'keywords': ['raga', 'healing', 'meditation', 'spiritual']
                },
                'chinese': {
                    'instruments': ['guzheng', 'erhu', 'dizi', 'pipa'],
                    'genres': ['traditional', 'meditation', 'healing'],
                    'keywords': ['traditional chinese', 'healing', 'meditation', 'zen']
                },
                'japanese': {
                    'instruments': ['koto', 'shamisen', 'shakuhachi'],
                    'genres': ['traditional', 'zen', 'meditation'],
                    'keywords': ['zen', 'meditation', 'traditional japanese', 'healing']
                },
                'western': {
                    'instruments': ['piano', 'violin', 'cello', 'harp'],
                    'genres': ['classical', 'new-age', 'acoustic'],
                    'keywords': ['classical', 'healing', 'therapeutic', 'peaceful']
                },
                'african': {
                    'instruments': ['djembe', 'kora', 'mbira', 'kalimba'],
                    'genres': ['traditional', 'world', 'healing'],
                    'keywords': ['african traditional', 'healing', 'rhythmic', 'spiritual']
                }
            }
            
            params = cultural_mapping.get(culture.lower(), cultural_mapping['western'])
            tracks = []
            
            # Search for cultural healing music
            search_terms = params['keywords'] + params['instruments'][:2]  # Limit instruments
            
            for term in search_terms:
                results = self.sp.search(
                    q=f"{term} healing therapeutic",
                    type='track',
                    limit=6,
                    market='US'
                )
                tracks.extend(results['tracks']['items'])
            
            # Analyze for cultural healing effectiveness
            cultural_tracks = []
            for track in tracks[:20]:
                try:
                    features = self.sp.audio_features(track['id'])
                    if features and features[0]:
                        cultural_score = self._calculate_cultural_healing_score(
                            features[0], culture, healing_type
                        )
                        cultural_tracks.append({
                            'track': track,
                            'cultural_score': cultural_score,
                            'culture': culture
                        })
                except:
                    continue
            
            cultural_tracks.sort(key=lambda x: x['cultural_score'], reverse=True)
            
            selected_tracks = []
            for item in cultural_tracks[:12]:  # Select top 12 tracks
                track = item['track']
                selected_tracks.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'duration_ms': track['duration_ms'],
                    'culture': culture,
                    'healing_type': healing_type,
                    'cultural_score': item['cultural_score'],
                    'spotify_url': track['external_urls']['spotify'],
                    'therapy_benefit': f'{culture.title()} cultural healing and spiritual wellness'
                })
            
            return {
                'culture': culture,
                'healing_type': healing_type,
                'language': language,
                'tracks': selected_tracks,
                'therapy_focus': f'{culture.title()} traditional healing and cultural connection',
                'usage_instructions': 'Use for cultural healing and spiritual connection',
                'source': 'spotify_cultural'
            }
            
        except Exception as e:
            logging.error(f"Cultural healing music error: {e}")
            return self._get_cultural_fallback_playlist(culture, healing_type)
    
    def analyze_track_therapeutic_value(self, track_id):
        """Detailed therapeutic analysis of a specific track"""
        if not self.is_connected:
            return {'error': 'Spotify not connected'}
        
        try:
            # Get track info and audio features
            track_info = self.sp.track(track_id)
            features = self.sp.audio_features(track_id)[0]
            
            if not features:
                return {'error': 'Audio features not available'}
            
            # Calculate therapeutic metrics
            therapeutic_analysis = {
                'track_name': track_info['name'],
                'artist': track_info['artists'][0]['name'],
                'duration_ms': track_info['duration_ms'],
                'relaxation_score': self._calculate_relaxation_score(features),
                'energy_level': features['energy'],
                'mood_valence': features['valence'],
                'therapeutic_bpm': features['tempo'],
                'acoustic_quality': features['acousticness'],
                'instrumental_ratio': features['instrumentalness'],
                'recommended_for': self._get_therapeutic_recommendations(features),
                'best_time_to_use': self._get_optimal_usage_time(features),
                'therapy_applications': self._get_therapy_applications(features)
            }
            
            return therapeutic_analysis
            
        except Exception as e:
            logging.error(f"Track analysis error: {e}")
            return {'error': f'Analysis failed: {str(e)}'}
    
    def _calculate_sleep_score(self, features, phase_params):
        """Calculate how suitable a track is for sleep therapy"""
        return (
            (1 - features['energy']) * 0.4 +
            (1 - features['valence']) * 0.2 +
            features['acousticness'] * 0.2 +
            features['instrumentalness'] * 0.2
        )
    
    def _calculate_study_score(self, features, study_params):
        """Calculate study effectiveness score"""
        return (
            (0.5 - abs(features['energy'] - 0.4)) * 0.3 +
            (0.5 - abs(features['valence'] - 0.5)) * 0.3 +
            features['instrumentalness'] * 0.2 +
            (1 - features['speechiness']) * 0.2
        )
    
    def _calculate_cultural_healing_score(self, features, culture, healing_type):
        """Calculate cultural healing effectiveness"""
        return (
            features['acousticness'] * 0.3 +
            features['instrumentalness'] * 0.3 +
            (1 - features['loudness'] / -60) * 0.2 +
            (0.6 - abs(features['valence'] - 0.5)) * 0.2
        )
    
    def _calculate_relaxation_score(self, features):
        """Calculate overall relaxation potential"""
        return (
            (1 - features['energy']) * 0.3 +
            features['acousticness'] * 0.3 +
            features['instrumentalness'] * 0.2 +
            (1 - features['loudness'] / -60) * 0.2
        )
    
    def _get_therapeutic_recommendations(self, features):
        """Get therapeutic use recommendations based on audio features"""
        recommendations = []
        
        if features['energy'] < 0.3:
            recommendations.append('Sleep therapy')
        if features['valence'] > 0.7:
            recommendations.append('Mood enhancement')
        if features['instrumentalness'] > 0.7:
            recommendations.append('Focus and concentration')
        if features['acousticness'] > 0.6:
            recommendations.append('Stress relief')
        
        return recommendations
    
    def _get_optimal_usage_time(self, features):
        """Suggest optimal time for using this track"""
        if features['energy'] < 0.3:
            return 'Evening/Night'
        elif features['energy'] > 0.7:
            return 'Morning/Afternoon'
        else:
            return 'Anytime'
    
    def _get_therapy_applications(self, features):
        """Get specific therapy applications"""
        applications = []
        
        if features['tempo'] < 80:
            applications.append('Anxiety reduction')
        if features['valence'] < 0.3:
            applications.append('Depression support')
        if features['energy'] > 0.6:
            applications.append('Energy boost')
        if features['instrumentalness'] > 0.5:
            applications.append('Meditation')
        
        return applications
    
    def _get_crisis_fallback_playlist(self, crisis_level):
        """Fallback crisis intervention playlist"""
        return {
            'crisis_level': crisis_level,
            'tracks': [
                {'name': 'Emergency Calm', 'artist': 'Crisis Support', 'therapy_benefit': 'Immediate calming'},
                {'name': 'Breathe Easy', 'artist': 'Wellness Support', 'therapy_benefit': 'Breathing support'},
                {'name': 'Safe Space', 'artist': 'Crisis Care', 'therapy_benefit': 'Safety and comfort'}
            ],
            'therapy_focus': 'Crisis intervention',
            'source': 'fallback_crisis'
        }
    
    def _get_sleep_fallback_sequence(self, sleep_goal):
        """Fallback sleep therapy sequence"""
        return {
            'sleep_goal': sleep_goal,
            'tracks': [
                {'name': 'Sleep Preparation', 'artist': 'Sleep Therapy', 'phase': 'relaxation'},
                {'name': 'Deep Rest', 'artist': 'Sleep Therapy', 'phase': 'deep_sleep'}
            ],
            'source': 'fallback_sleep'
        }
    
    def _get_study_fallback_playlist(self, study_type):
        """Fallback study playlist"""
        return {
            'study_type': study_type,
            'tracks': [
                {'name': f'{study_type.title()} Focus', 'artist': 'Study Music', 'therapy_benefit': 'Focus enhancement'}
            ],
            'source': 'fallback_study'
        }
    
    def _get_cultural_fallback_playlist(self, culture, healing_type):
        """Fallback cultural healing playlist"""
        return {
            'culture': culture,
            'healing_type': healing_type,
            'tracks': [
                {'name': f'{culture.title()} Healing', 'artist': 'Cultural Therapy', 'therapy_benefit': 'Cultural healing'}
            ],
            'source': 'fallback_cultural'
        }

# Global instance
spotify_therapy = SpotifyMusicTherapy()
