# 🧠 Manas: Offline Capability Manager
# Offline-first mental wellness support with sync capabilities

import json
import sqlite3
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import hashlib
import gzip
import base64

# Configure logging
logger = logging.getLogger(__name__)

class OfflineManager:
    """Offline capability manager for mental wellness platform"""
    
    def __init__(self, offline_db_path: str = "manas_offline.db"):
        """Initialize offline manager"""
        self.offline_db_path = offline_db_path
        self.sync_queue = []
        self.offline_content_cache = {}
        
        # Initialize offline database
        self._init_offline_db()
        
        # Offline therapy content templates
        self.offline_therapy_templates = {
            'breathing': {
                'title': 'Simple Breathing Exercise',
                'description': 'A calming breathing technique you can do anywhere',
                'instructions': [
                    'Sit comfortably with your back straight',
                    'Close your eyes or soften your gaze',
                    'Breathe in slowly through your nose for 4 counts',
                    'Hold your breath gently for 4 counts',
                    'Breathe out slowly through your mouth for 6 counts',
                    'Repeat this cycle 5-10 times'
                ],
                'duration': '5-10 minutes',
                'difficulty': 'easy'
            },
            'grounding': {
                'title': '5-4-3-2-1 Grounding Technique',
                'description': 'A grounding exercise to help you feel present and calm',
                'instructions': [
                    'Look around and name 5 things you can see',
                    'Listen and identify 4 things you can hear',
                    'Touch and notice 3 things you can feel',
                    'Identify 2 things you can smell',
                    'Think of 1 thing you can taste',
                    'Take a few deep breaths and notice how you feel'
                ],
                'duration': '5-10 minutes',
                'difficulty': 'easy'
            },
            'progressive_relaxation': {
                'title': 'Progressive Muscle Relaxation',
                'description': 'Systematically relax your entire body',
                'instructions': [
                    'Lie down or sit comfortably',
                    'Start with your toes - tense for 5 seconds, then relax',
                    'Move to your calves - tense and relax',
                    'Continue with thighs, abdomen, hands, arms, shoulders',
                    'Tense your face muscles, then relax',
                    'Notice the difference between tension and relaxation',
                    'Breathe deeply and enjoy the relaxed feeling'
                ],
                'duration': '15-20 minutes',
                'difficulty': 'medium'
            },
            'mindfulness': {
                'title': 'Mindful Awareness',
                'description': 'Practice being present in the moment',
                'instructions': [
                    'Sit quietly and focus on your breathing',
                    'Notice thoughts as they come and go',
                    'Don\'t judge or try to change anything',
                    'When your mind wanders, gently return to your breath',
                    'Observe sensations in your body',
                    'Practice acceptance of whatever you\'re experiencing'
                ],
                'duration': '10-20 minutes',
                'difficulty': 'medium'
            },
            'journaling': {
                'title': 'Emotional Check-in Journal',
                'description': 'Reflect on your thoughts and feelings',
                'instructions': [
                    'Find a quiet space with pen and paper',
                    'Write about how you\'re feeling right now',
                    'Don\'t worry about grammar or structure',
                    'Explore what might be causing these feelings',
                    'Write about what you\'re grateful for today',
                    'End with one positive affirmation about yourself'
                ],
                'duration': '10-15 minutes',
                'difficulty': 'easy'
            }
        }
        
        # Crisis support content for offline use
        self.offline_crisis_support = {
            'emergency_contacts': [
                {'name': 'AASRA', 'number': '91-22-27546669', 'hours': '24/7'},
                {'name': 'Sneha', 'number': '044-24640050', 'hours': '24/7'},
                {'name': 'Vandrevala Foundation', 'number': '1860-2662-345', 'hours': '24/7'},
                {'name': 'Emergency Services', 'number': '112', 'type': 'emergency'}
            ],
            'immediate_coping_strategies': [
                'Take slow, deep breaths',
                'Find a safe, comfortable space',
                'Call a trusted friend or family member',
                'Use grounding techniques (5-4-3-2-1)',
                'Write down your feelings',
                'Listen to calming music',
                'Take a warm shower or bath'
            ],
            'safety_planning': {
                'warning_signs': [
                    'Feeling hopeless or trapped',
                    'Thinking about death or suicide',
                    'Feeling like a burden to others',
                    'Increased substance use',
                    'Withdrawing from friends and family'
                ],
                'coping_strategies': [
                    'Call crisis helpline',
                    'Reach out to support person',
                    'Remove harmful objects',
                    'Go to safe location',
                    'Use distraction techniques'
                ],
                'support_contacts': 'List of trusted people to contact'
            }
        }
        
        logger.info("OfflineManager initialized successfully")
    
    def _init_offline_db(self):
        """Initialize offline SQLite database"""
        try:
            conn = sqlite3.connect(self.offline_db_path)
            
            # Offline sessions table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS offline_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    session_type TEXT,
                    content TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    synced BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Offline emotions table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS offline_emotions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    emotion_data TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    synced BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Offline feedback table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS offline_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    feedback_data TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    synced BOOLEAN DEFAULT FALSE
                )
            ''')
            
            # Cached content table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cached_content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_type TEXT NOT NULL,
                    content_key TEXT NOT NULL,
                    content_data TEXT,
                    expiry_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Offline database initialization error: {e}")
    
    def store_offline_session(self, user_id: str, session_data: Dict[str, Any]) -> bool:
        """
        Store therapy session data for offline use
        
        Args:
            user_id: User identifier
            session_data: Session data to store
        
        Returns:
            Success status
        """
        try:
            conn = sqlite3.connect(self.offline_db_path)
            
            conn.execute('''
                INSERT INTO offline_sessions (user_id, session_id, session_type, content)
                VALUES (?, ?, ?, ?)
            ''', (
                user_id,
                session_data.get('session_id'),
                session_data.get('type'),
                json.dumps(session_data)
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Stored offline session for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Offline session storage error: {e}")
            return False
    
    def store_offline_emotion(self, user_id: str, emotion_data: Dict[str, Any]) -> bool:
        """
        Store emotion analysis data for offline use
        
        Args:
            user_id: User identifier
            emotion_data: Emotion analysis data
        
        Returns:
            Success status
        """
        try:
            conn = sqlite3.connect(self.offline_db_path)
            
            conn.execute('''
                INSERT INTO offline_emotions (user_id, session_id, emotion_data)
                VALUES (?, ?, ?)
            ''', (
                user_id,
                emotion_data.get('session_id'),
                json.dumps(emotion_data)
            ))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Offline emotion storage error: {e}")
            return False
    
    def get_offline_therapy_content(self, emotion_state: Dict[str, Any], user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get appropriate therapy content for offline use
        
        Args:
            emotion_state: Current emotional state
            user_preferences: User preferences and accessibility needs
        
        Returns:
            Offline therapy content
        """
        try:
            primary_emotion = emotion_state.get('primary_emotion', 'neutral')
            emotion_intensity = emotion_state.get('emotion_intensity', 5)
            
            # Select appropriate therapy based on emotion
            if primary_emotion in ['anxious', 'stressed', 'overwhelmed']:
                if emotion_intensity >= 7:
                    therapy_type = 'breathing'
                else:
                    therapy_type = 'grounding'
            elif primary_emotion in ['sad', 'depressed', 'lonely']:
                therapy_type = 'journaling'
            elif primary_emotion in ['angry', 'frustrated']:
                therapy_type = 'progressive_relaxation'
            else:
                therapy_type = 'mindfulness'
            
            # Get base therapy content
            therapy_content = self.offline_therapy_templates.get(therapy_type, self.offline_therapy_templates['breathing']).copy()
            
            # Add offline-specific adaptations
            therapy_content.update({
                'offline_mode': True,
                'sync_when_online': True,
                'therapy_type': therapy_type,
                'selected_for_emotion': primary_emotion,
                'accessibility_adaptations': self._get_offline_accessibility_adaptations(user_preferences),
                'cultural_notes': self._get_cultural_adaptations(user_preferences),
                'follow_up_offline': [
                    'Rate how you feel after this exercise (1-10)',
                    'Note any thoughts or insights',
                    'Plan when to practice this again',
                    'Data will sync when you\'re back online'
                ]
            })
            
            return therapy_content
            
        except Exception as e:
            logger.error(f"Offline therapy content error: {e}")
            return self.offline_therapy_templates['breathing']
    
    def get_offline_crisis_support(self) -> Dict[str, Any]:
        """
        Get crisis support content for offline use
        
        Returns:
            Offline crisis support content
        """
        try:
            crisis_content = self.offline_crisis_support.copy()
            
            # Add offline-specific instructions
            crisis_content.update({
                'offline_mode': True,
                'immediate_actions': [
                    'If in immediate danger, call emergency services: 112',
                    'Use offline coping strategies below',
                    'Try to reach someone by phone if possible',
                    'Your safety data will sync when back online'
                ],
                'offline_coping': [
                    'Practice deep breathing (4-4-6 pattern)',
                    'Use 5-4-3-2-1 grounding technique',
                    'Write down your feelings if you have paper',
                    'Find a safe, comfortable space',
                    'Try progressive muscle relaxation'
                ],
                'when_online_again': [
                    'Contact crisis helpline for follow-up',
                    'Sync your data with the platform',
                    'Consider professional support',
                    'Update your safety plan'
                ]
            })
            
            return crisis_content
            
        except Exception as e:
            logger.error(f"Offline crisis support error: {e}")
            return {
                'emergency_contacts': [{'name': 'Emergency', 'number': '112'}],
                'immediate_actions': ['Call emergency services if in danger']
            }
    
    def sync_offline_data(self, user_id: str, offline_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Sync offline data when connection is available
        
        Args:
            user_id: User identifier
            offline_data: List of offline data to sync
        
        Returns:
            Sync result summary
        """
        try:
            sync_results = {
                'sessions_synced': 0,
                'emotions_synced': 0,
                'feedback_synced': 0,
                'errors': [],
                'total_items': len(offline_data)
            }
            
            conn = sqlite3.connect(self.offline_db_path)
            
            for data_item in offline_data:
                try:
                    data_type = data_item.get('type')
                    
                    if data_type == 'session':
                        # Sync session data
                        self._sync_session_data(conn, user_id, data_item)
                        sync_results['sessions_synced'] += 1
                        
                    elif data_type == 'emotion':
                        # Sync emotion data
                        self._sync_emotion_data(conn, user_id, data_item)
                        sync_results['emotions_synced'] += 1
                        
                    elif data_type == 'feedback':
                        # Sync feedback data
                        self._sync_feedback_data(conn, user_id, data_item)
                        sync_results['feedback_synced'] += 1
                        
                except Exception as item_error:
                    sync_results['errors'].append(f"Item sync error: {str(item_error)}")
            
            conn.close()
            
            # Clean up synced data
            self._cleanup_synced_data()
            
            logger.info(f"Sync completed for user {user_id}: {sync_results}")
            return sync_results
            
        except Exception as e:
            logger.error(f"Offline data sync error: {e}")
            return {
                'sessions_synced': 0,
                'emotions_synced': 0,
                'feedback_synced': 0,
                'errors': [str(e)],
                'total_items': 0
            }
    
    def cache_content_for_offline(self, content_type: str, content_key: str, content_data: Any, expiry_hours: int = 24) -> bool:
        """
        Cache content for offline use
        
        Args:
            content_type: Type of content (therapy, crisis, etc.)
            content_key: Unique key for content
            content_data: Content to cache
            expiry_hours: Hours until content expires
        
        Returns:
            Success status
        """
        try:
            conn = sqlite3.connect(self.offline_db_path)
            
            # Compress content data
            compressed_data = self._compress_content(content_data)
            
            # Calculate expiry date
            expiry_date = datetime.now() + timedelta(hours=expiry_hours)
            
            # Store or update cached content
            conn.execute('''
                INSERT OR REPLACE INTO cached_content 
                (content_type, content_key, content_data, expiry_date)
                VALUES (?, ?, ?, ?)
            ''', (content_type, content_key, compressed_data, expiry_date))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            logger.error(f"Content caching error: {e}")
            return False
    
    def get_cached_content(self, content_type: str, content_key: str) -> Optional[Any]:
        """
        Retrieve cached content for offline use
        
        Args:
            content_type: Type of content
            content_key: Content key
        
        Returns:
            Cached content or None if not found/expired
        """
        try:
            conn = sqlite3.connect(self.offline_db_path)
            
            cursor = conn.execute('''
                SELECT content_data, expiry_date FROM cached_content
                WHERE content_type = ? AND content_key = ?
            ''', (content_type, content_key))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return None
            
            content_data, expiry_date = result
            
            # Check if content has expired
            if datetime.now() > datetime.fromisoformat(expiry_date):
                self._remove_expired_content(content_type, content_key)
                return None
            
            # Decompress and return content
            return self._decompress_content(content_data)
            
        except Exception as e:
            logger.error(f"Cached content retrieval error: {e}")
            return None
    
    def prepare_offline_resources(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare personalized offline resources for user
        
        Args:
            user_profile: User profile information
        
        Returns:
            Offline resources package
        """
        try:
            offline_package = {
                'therapy_content': {},
                'crisis_support': self.get_offline_crisis_support(),
                'user_preferences': user_profile,
                'accessibility_features': self._get_offline_accessibility_adaptations(user_profile),
                'cultural_adaptations': self._get_cultural_adaptations(user_profile),
                'sync_instructions': {
                    'auto_sync_when_online': True,
                    'manual_sync_available': True,
                    'data_retention_days': 30
                }
            }
            
            # Prepare therapy content for common emotions
            common_emotions = ['anxious', 'sad', 'stressed', 'angry', 'neutral']
            for emotion in common_emotions:
                emotion_state = {'primary_emotion': emotion, 'emotion_intensity': 5}
                therapy_content = self.get_offline_therapy_content(emotion_state, user_profile)
                offline_package['therapy_content'][emotion] = therapy_content
            
            # Cache the offline package
            package_key = f"offline_package_{user_profile.get('user_id', 'default')}"
            self.cache_content_for_offline('offline_package', package_key, offline_package, 168)  # 1 week
            
            return offline_package
            
        except Exception as e:
            logger.error(f"Offline resources preparation error: {e}")
            return {
                'therapy_content': self.offline_therapy_templates,
                'crisis_support': self.offline_crisis_support,
                'error': str(e)
            }
    
    def _get_offline_accessibility_adaptations(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Get accessibility adaptations for offline use"""
        adaptations = {}
        
        if user_preferences.get('visual_impairment'):
            adaptations.update({
                'text_to_speech_instructions': True,
                'high_contrast_mode': True,
                'large_text': True,
                'audio_cues': True
            })
        
        if user_preferences.get('hearing_impairment'):
            adaptations.update({
                'visual_instructions_only': True,
                'vibration_alerts': True,
                'text_based_feedback': True
            })
        
        if user_preferences.get('motor_impairment'):
            adaptations.update({
                'voice_control_available': True,
                'simplified_interactions': True,
                'extended_timeouts': True
            })
        
        return adaptations
    
    def _get_cultural_adaptations(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Get cultural adaptations for offline content"""
        language = user_preferences.get('language', 'english')
        
        adaptations = {
            'language': language,
            'cultural_context': 'indian',
            'family_considerations': True,
            'spiritual_elements': user_preferences.get('include_spiritual', False)
        }
        
        if language != 'english':
            adaptations.update({
                'native_language_support': True,
                'cultural_metaphors': True,
                'regional_practices': True
            })
        
        return adaptations
    
    def _sync_session_data(self, conn: sqlite3.Connection, user_id: str, session_data: Dict[str, Any]):
        """Sync session data to main database"""
        # In production, this would sync to the main online database
        # For now, just mark as synced
        conn.execute('''
            UPDATE offline_sessions SET synced = TRUE 
            WHERE user_id = ? AND session_id = ?
        ''', (user_id, session_data.get('session_id')))
        conn.commit()
    
    def _sync_emotion_data(self, conn: sqlite3.Connection, user_id: str, emotion_data: Dict[str, Any]):
        """Sync emotion data to main database"""
        conn.execute('''
            UPDATE offline_emotions SET synced = TRUE 
            WHERE user_id = ? AND session_id = ?
        ''', (user_id, emotion_data.get('session_id')))
        conn.commit()
    
    def _sync_feedback_data(self, conn: sqlite3.Connection, user_id: str, feedback_data: Dict[str, Any]):
        """Sync feedback data to main database"""
        conn.execute('''
            UPDATE offline_feedback SET synced = TRUE 
            WHERE user_id = ? AND session_id = ?
        ''', (user_id, feedback_data.get('session_id')))
        conn.commit()
    
    def _cleanup_synced_data(self):
        """Clean up synced offline data"""
        try:
            conn = sqlite3.connect(self.offline_db_path)
            
            # Remove synced data older than 7 days
            cutoff_date = datetime.now() - timedelta(days=7)
            
            conn.execute('''
                DELETE FROM offline_sessions 
                WHERE synced = TRUE AND timestamp < ?
            ''', (cutoff_date,))
            
            conn.execute('''
                DELETE FROM offline_emotions 
                WHERE synced = TRUE AND timestamp < ?
            ''', (cutoff_date,))
            
            conn.execute('''
                DELETE FROM offline_feedback 
                WHERE synced = TRUE AND timestamp < ?
            ''', (cutoff_date,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Synced data cleanup error: {e}")
    
    def _remove_expired_content(self, content_type: str, content_key: str):
        """Remove expired cached content"""
        try:
            conn = sqlite3.connect(self.offline_db_path)
            conn.execute('''
                DELETE FROM cached_content 
                WHERE content_type = ? AND content_key = ?
            ''', (content_type, content_key))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Expired content removal error: {e}")
    
    def _compress_content(self, content: Any) -> str:
        """Compress content for storage"""
        try:
            json_str = json.dumps(content)
            compressed = gzip.compress(json_str.encode('utf-8'))
            return base64.b64encode(compressed).decode('utf-8')
        except Exception as e:
            logger.error(f"Content compression error: {e}")
            return json.dumps(content)  # Fallback to uncompressed
    
    def _decompress_content(self, compressed_content: str) -> Any:
        """Decompress stored content"""
        try:
            compressed_bytes = base64.b64decode(compressed_content.encode('utf-8'))
            decompressed = gzip.decompress(compressed_bytes)
            return json.loads(decompressed.decode('utf-8'))
        except Exception as e:
            logger.error(f"Content decompression error: {e}")
            return json.loads(compressed_content)  # Fallback assuming uncompressed