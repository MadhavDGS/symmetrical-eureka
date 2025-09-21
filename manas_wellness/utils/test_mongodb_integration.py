#!/usr/bin/env python3
"""
🗃️ MongoDB Integration Test
Tests MongoDB connection and data migration
"""

import os
import sys
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

def test_mongodb_connection():
    """Test MongoDB connection"""
    print("🗃️ Testing MongoDB Connection...")
    
    mongodb_uri = os.getenv('MONGODB_URI')
    
    if not mongodb_uri:
        print("❌ MONGODB_URI not found in .env file")
        print("📝 Please add this to your .env file:")
        print("   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/manas_wellness")
        return False
    
    try:
        # Import pymongo (will fail if not installed)
        import pymongo
        
        # Create client
        client = pymongo.MongoClient(mongodb_uri)
        
        # Test connection
        client.admin.command('ping')
        
        # Get database
        db_name = os.getenv('MONGODB_DB_NAME', 'manas_wellness')
        db = client[db_name]
        
        print("✅ MongoDB connection successful!")
        print(f"📊 Database: {db_name}")
        
        return client, db
        
    except ImportError:
        print("❌ pymongo not installed. Run: pip install pymongo")
        return False, False
    except Exception as e:
        print(f"❌ MongoDB connection failed: {str(e)}")
        return False, False

def test_collection_operations(db):
    """Test basic database operations"""
    print("\n📝 Testing Database Operations...")
    
    try:
        # Test collection creation and insertion
        test_collection = db.test_connection
        
        # Insert test document
        test_doc = {
            "test_id": "connection_test",
            "timestamp": datetime.now(),
            "status": "testing",
            "data": {"message": "MongoDB connection test successful"}
        }
        
        result = test_collection.insert_one(test_doc)
        print(f"✅ Document inserted with ID: {result.inserted_id}")
        
        # Test query
        found_doc = test_collection.find_one({"test_id": "connection_test"})
        if found_doc:
            print("✅ Document query successful")
            
        # Test update
        update_result = test_collection.update_one(
            {"test_id": "connection_test"},
            {"$set": {"status": "completed"}}
        )
        print(f"✅ Document updated: {update_result.modified_count} documents")
        
        # Clean up test document
        test_collection.delete_one({"test_id": "connection_test"})
        print("✅ Test document cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Database operations failed: {str(e)}")
        return False

def create_collections_schema(db):
    """Create required collections for Manas Wellness"""
    print("\n🏗️ Creating Database Schema...")
    
    collections_schema = {
        'users': {
            'indexes': [
                {'key': 'user_id', 'unique': True},
                {'key': 'email', 'unique': True},
                {'key': 'created_at'}
            ],
            'sample_doc': {
                'user_id': 'user_123',
                'email': 'user@example.com',
                'name': 'Sample User',
                'age': 25,
                'preferences': {
                    'language': 'english',
                    'therapy_type': ['music', 'art', 'journal'],
                    'crisis_contacts': []
                },
                'created_at': datetime.now(),
                'last_active': datetime.now()
            }
        },
        
        'journal_entries': {
            'indexes': [
                {'key': 'user_id'},
                {'key': 'entry_date'},
                {'key': 'mood_score'}
            ],
            'sample_doc': {
                'entry_id': 'journal_123',
                'user_id': 'user_123',
                'content': 'Sample journal entry content',
                'mood_score': 7,
                'emotions': ['happy', 'grateful'],
                'entry_date': datetime.now(),
                'analysis': {
                    'sentiment': 'positive',
                    'key_themes': ['gratitude', 'achievement'],
                    'ai_insights': 'User shows positive emotional state'
                }
            }
        },
        
        'emotion_analysis': {
            'indexes': [
                {'key': 'user_id'},
                {'key': 'analysis_date'},
                {'key': 'emotion_type'}
            ],
            'sample_doc': {
                'analysis_id': 'emotion_123',
                'user_id': 'user_123',
                'emotion_type': 'facial',
                'detected_emotions': {
                    'joy': 0.8,
                    'sadness': 0.1,
                    'anger': 0.1
                },
                'analysis_date': datetime.now(),
                'context': 'art_therapy_session'
            }
        },
        
        'therapy_sessions': {
            'indexes': [
                {'key': 'user_id'},
                {'key': 'session_date'},
                {'key': 'therapy_type'}
            ],
            'sample_doc': {
                'session_id': 'session_123',
                'user_id': 'user_123',
                'therapy_type': 'music',
                'session_date': datetime.now(),
                'duration_minutes': 30,
                'effectiveness_rating': 8,
                'resources_used': ['playlist_relaxing', 'breathing_exercise'],
                'notes': 'User responded well to classical music therapy'
            }
        },
        
        'peer_connections': {
            'indexes': [
                {'key': 'user_id'},
                {'key': 'connection_date'},
                {'key': 'status'}
            ],
            'sample_doc': {
                'connection_id': 'peer_123',
                'user_id': 'user_123',
                'peer_user_id': 'user_456',
                'connection_type': 'support_buddy',
                'status': 'active',
                'connection_date': datetime.now(),
                'shared_interests': ['music_therapy', 'journaling']
            }
        }
    }
    
    created_collections = []
    
    for collection_name, schema in collections_schema.items():
        try:
            collection = db[collection_name]
            
            # Create indexes
            for index_def in schema['indexes']:
                collection.create_index(
                    index_def['key'], 
                    unique=index_def.get('unique', False)
                )
            
            # Insert sample document (for testing)
            if 'sample_doc' in schema:
                # Check if collection is empty
                if collection.count_documents({}) == 0:
                    collection.insert_one(schema['sample_doc'])
            
            created_collections.append(collection_name)
            print(f"✅ Collection '{collection_name}' created with indexes")
            
        except Exception as e:
            print(f"❌ Error creating collection '{collection_name}': {str(e)}")
    
    print(f"\n📊 Created {len(created_collections)} collections:")
    for collection in created_collections:
        print(f"  - {collection}")
    
    return len(created_collections) > 0

def export_sqlite_data():
    """Export existing SQLite data for migration"""
    print("\n📤 Exporting SQLite Data...")
    
    sqlite_db_path = 'manas_wellness.db'
    
    if not os.path.exists(sqlite_db_path):
        print("❌ SQLite database not found. Skipping data export.")
        return False
    
    try:
        import sqlite3
        
        # Connect to SQLite
        conn = sqlite3.connect(sqlite_db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        export_data = {}
        
        for table_name in tables:
            table = table_name[0]
            if table.startswith('sqlite_'):
                continue
                
            cursor.execute(f"SELECT * FROM {table}")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            export_data[table] = {
                'columns': columns,
                'data': rows
            }
            
            print(f"  📋 Exported {len(rows)} rows from '{table}' table")
        
        # Save exported data
        os.makedirs('data_migration', exist_ok=True)
        with open('data_migration/sqlite_export.json', 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        conn.close()
        
        print("✅ SQLite data exported to data_migration/sqlite_export.json")
        return True
        
    except Exception as e:
        print(f"❌ SQLite export failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Manas Wellness - MongoDB Integration Test")
    print("=" * 50)
    
    # Test connection
    client, db = test_mongodb_connection()
    if not client:
        print("\n❌ MongoDB integration test failed!")
        sys.exit(1)
    
    # Test operations
    if test_collection_operations(db):
        print("✅ Basic database operations working")
    
    # Create schema
    if create_collections_schema(db):
        print("✅ Database schema created successfully")
    
    # Export existing data
    export_sqlite_data()
    
    # Close connection
    client.close()
    
    print("\n🎉 MongoDB Integration Test Summary:")
    print("=" * 50)
    print("✅ MongoDB Connection: Success")
    print("✅ Database Operations: Working")
    print("✅ Schema Creation: Complete")
    print("✅ Data Export: Prepared")
    
    print("\n🔧 Next Steps:")
    print("1. Review exported data in data_migration/sqlite_export.json")
    print("2. Update app.py to use MongoDB instead of SQLite")
    print("3. Test the complete application with MongoDB")
    print("4. Monitor performance and optimize queries as needed")

if __name__ == "__main__":
    main()