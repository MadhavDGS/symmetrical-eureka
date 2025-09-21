"""
Database Integration Layer - MongoDB and Supabase
Handles both relational and document-based data with real-time features
"""

import os
import logging
from datetime import datetime
from typing import Optional, Dict, List, Any

# MongoDB Integration
try:
    import pymongo
    from pymongo import MongoClient
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False
    logging.warning("pymongo not installed - MongoDB features disabled")

# Supabase Integration  
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    logging.warning("supabase not installed - Real-time features disabled")

class DatabaseManager:
    def __init__(self):
        self.mongodb_client = None
        self.mongodb_db = None
        self.supabase_client = None
        
        # Initialize MongoDB
        if MONGODB_AVAILABLE:
            self._init_mongodb()
        
        # Initialize Supabase
        if SUPABASE_AVAILABLE:
            self._init_supabase()
    
    def _init_mongodb(self):
        """Initialize MongoDB connection"""
        mongodb_uri = os.getenv('MONGODB_URI')
        if mongodb_uri:
            try:
                self.mongodb_client = MongoClient(mongodb_uri)
                db_name = os.getenv('MONGODB_DB_NAME', 'manas_wellness')
                self.mongodb_db = self.mongodb_client[db_name]
                
                # Test connection
                self.mongodb_client.admin.command('ping')
                logging.info("MongoDB connected successfully")
                
            except Exception as e:
                logging.error(f"MongoDB connection failed: {e}")
                self.mongodb_client = None
    
    def _init_supabase(self):
        """Initialize Supabase connection"""
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_ANON_KEY')
        
        if supabase_url and supabase_key:
            try:
                self.supabase_client = create_client(supabase_url, supabase_key)
                logging.info("Supabase connected successfully")
                
            except Exception as e:
                logging.error(f"Supabase connection failed: {e}")
                self.supabase_client = None
    
    # User Management
    def create_user(self, user_data: Dict[str, Any]) -> Optional[str]:
        """Create new user in the database"""
        if self.mongodb_db is not None:
            try:
                user_data['created_at'] = datetime.now()
                user_data['last_active'] = datetime.now()
                
                result = self.mongodb_db.users.insert_one(user_data)
                logging.info(f"User created with ID: {result.inserted_id}")
                return str(result.inserted_id)
                
            except Exception as e:
                logging.error(f"Error creating user: {e}")
                return None
        else:
            # Fallback to SQLite or in-memory storage
            return self._fallback_create_user(user_data)
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        if self.mongodb_db is not None:
            try:
                user = self.mongodb_db.users.find_one({"user_id": user_id})
                return user
            except Exception as e:
                logging.error(f"Error getting user: {e}")
                return None
        else:
            return self._fallback_get_user(user_id)
    
    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        """Update user information"""
        if self.mongodb_db is not None:
            try:
                update_data['last_modified'] = datetime.now()
                result = self.mongodb_db.users.update_one(
                    {"user_id": user_id},
                    {"$set": update_data}
                )
                return result.modified_count > 0
            except Exception as e:
                logging.error(f"Error updating user: {e}")
                return False
        else:
            return self._fallback_update_user(user_id, update_data)
    
    # Journal Management
    def save_journal_entry(self, user_id: str, entry_data: Dict[str, Any]) -> Optional[str]:
        """Save journal entry"""
        if self.mongodb_db is not None:
            try:
                entry_data.update({
                    'user_id': user_id,
                    'created_at': datetime.now(),
                    'entry_id': f"journal_{user_id}_{datetime.now().timestamp()}"
                })
                
                result = self.mongodb_db.journal_entries.insert_one(entry_data)
                return str(result.inserted_id)
                
            except Exception as e:
                logging.error(f"Error saving journal entry: {e}")
                return None
        else:
            return self._fallback_save_journal(user_id, entry_data)
    
    def get_journal_entries(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's journal entries"""
        if self.mongodb_db is not None:
            try:
                entries = list(self.mongodb_db.journal_entries.find(
                    {"user_id": user_id}
                ).sort("created_at", -1).limit(limit))
                return entries
            except Exception as e:
                logging.error(f"Error getting journal entries: {e}")
                return []
        else:
            return self._fallback_get_journal_entries(user_id, limit)
    
    # Emotion Analysis Storage
    def save_emotion_analysis(self, user_id: str, analysis_data: Dict[str, Any]) -> Optional[str]:
        """Save emotion analysis results"""
        if self.mongodb_db is not None:
            try:
                analysis_data.update({
                    'user_id': user_id,
                    'analysis_date': datetime.now(),
                    'analysis_id': f"emotion_{user_id}_{datetime.now().timestamp()}"
                })
                
                result = self.mongodb_db.emotion_analysis.insert_one(analysis_data)
                return str(result.inserted_id)
                
            except Exception as e:
                logging.error(f"Error saving emotion analysis: {e}")
                return None
        else:
            return self._fallback_save_emotion_analysis(user_id, analysis_data)
    
    # Real-time Features (Supabase)
    def send_realtime_message(self, channel: str, message: Dict[str, Any]) -> bool:
        """Send real-time message via Supabase"""
        if self.supabase_client is not None:
            try:
                # Insert message into Supabase table for real-time sync
                result = self.supabase_client.table('realtime_messages').insert({
                    'channel': channel,
                    'message': message,
                    'timestamp': datetime.now().isoformat()
                }).execute()
                
                return len(result.data) > 0
                
            except Exception as e:
                logging.error(f"Error sending realtime message: {e}")
                return False
        else:
            return self._fallback_realtime_message(channel, message)
    
    def get_peer_connections(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's peer support connections"""
        if self.mongodb_db is not None:
            try:
                connections = list(self.mongodb_db.peer_connections.find(
                    {"$or": [{"user_id": user_id}, {"peer_user_id": user_id}]}
                ))
                return connections
            except Exception as e:
                logging.error(f"Error getting peer connections: {e}")
                return []
        else:
            return self._fallback_get_peer_connections(user_id)
    
    # Fallback methods for when databases are not available
    def _fallback_create_user(self, user_data: Dict[str, Any]) -> str:
        logging.warning("Using fallback user creation - data not persisted")
        return f"fallback_user_{datetime.now().timestamp()}"
    
    def _fallback_get_user(self, user_id: str) -> Dict[str, Any]:
        logging.warning("Using fallback user retrieval")
        return {"user_id": user_id, "name": "Demo User", "source": "fallback"}
    
    def _fallback_update_user(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        logging.warning("Using fallback user update - changes not persisted")
        return True
    
    def _fallback_save_journal(self, user_id: str, entry_data: Dict[str, Any]) -> str:
        logging.warning("Using fallback journal save - entry not persisted")
        return f"fallback_journal_{datetime.now().timestamp()}"
    
    def _fallback_get_journal_entries(self, user_id: str, limit: int) -> List[Dict[str, Any]]:
        logging.warning("Using fallback journal retrieval")
        return [{"content": "Demo journal entry", "mood": "neutral", "source": "fallback"}]
    
    def _fallback_save_emotion_analysis(self, user_id: str, analysis_data: Dict[str, Any]) -> str:
        logging.warning("Using fallback emotion analysis save")
        return f"fallback_emotion_{datetime.now().timestamp()}"
    
    def _fallback_realtime_message(self, channel: str, message: Dict[str, Any]) -> bool:
        logging.warning("Using fallback realtime messaging - message not sent")
        return False
    
    def _fallback_get_peer_connections(self, user_id: str) -> List[Dict[str, Any]]:
        logging.warning("Using fallback peer connections")
        return [{"peer_id": "demo_peer", "status": "demo", "source": "fallback"}]

# Global instance
db_manager = DatabaseManager()
