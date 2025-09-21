# 🚀 API Integration Guide - Manas Wellness Platform

## Overview
This guide provides step-by-step instructions for integrating real APIs into the Manas Wellness Platform for the GenAI hackathon. Currently using dummy data and placeholder functions - this will make everything functional with real services.

## 🔧 Step 1: Environment Setup

### Copy Environment File
```bash
cp .env.example .env
```

### Update .gitignore
Ensure your `.env` file is protected:
```bash
echo ".env" >> .gitignore
```

## 🗝️ Step 2: API Keys Required

### Priority 1: MongoDB (CRITICAL)
**Purpose**: Replace SQLite for scalable data storage
```bash
# Sign up at mongodb.com/atlas
# Create free cluster
# Get connection string like:
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/manas_wellness
```

### Priority 2: Spotify API (HIGH)
**Purpose**: Real music therapy with mood-based playlists
```bash
# Visit developer.spotify.com
# Create app in dashboard
# Get credentials:
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

### Priority 3: Google Cloud (HIGH)
**Purpose**: Advanced AI features beyond Gemini
```bash
# Visit console.cloud.google.com
# Create new project or use existing
# Enable APIs: Speech-to-Text, Text-to-Speech, Translation, Vision
# Download service account JSON:
GOOGLE_CLOUD_PROJECT_ID=your_project_id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
```

### Priority 4: Supabase (MEDIUM)
**Purpose**: Real-time peer support and chat
```bash
# Visit supabase.com
# Create new project
# Get keys from settings:
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_key
```

## 📦 Step 3: Install Additional Packages

### Update Requirements
The following packages will be automatically installed:
```txt
# Database
pymongo==4.6.0
supabase==2.3.0

# Music/Audio
spotipy==2.22.1

# Google Cloud Services
google-cloud-speech==2.21.0
google-cloud-texttospeech==2.16.3
google-cloud-translate==3.12.1
google-cloud-vision==3.4.4

# Real-time Features
python-socketio==5.10.0
redis==5.0.1

# SMS/Communication (Optional)
twilio==8.10.0
```

### Install Command
```bash
pip install -r requirements.txt
```

## 🔄 Step 4: Database Migration (MongoDB)

### 1. Export Current SQLite Data
```python
# Run this script to export existing data:
python utils/export_sqlite_data.py
```

### 2. Import to MongoDB
```python
# Run this script to import data:
python utils/import_to_mongodb.py
```

### 3. Update App Configuration
The app will automatically detect MongoDB URI and switch from SQLite.

## 🎵 Step 5: Spotify Integration

### Current Dummy Implementation
```python
# In app.py - line ~800
@app.route('/api/music-therapy')
def music_therapy():
    return jsonify({"tracks": ["dummy_track_1", "dummy_track_2"]})
```

### Real Implementation (Already Prepared)
Once you add Spotify keys, the app will automatically:
- Authenticate with Spotify
- Create mood-based playlists
- Recommend therapeutic music
- Play tracks directly in the app

## 🗣️ Step 6: Google Cloud Services

### Speech-to-Text (Voice Journaling)
- Converts voice entries to text
- Supports multiple Indian languages
- Real-time transcription

### Text-to-Speech (Accessibility)  
- Reads therapy content aloud
- Voice-guided meditation
- Audio feedback for visually impaired

### Translation (Multi-language)
- Automatic Hindi/English translation
- Regional language support
- Cultural context preservation

### Vision API (Emotion Detection)
- Real-time facial emotion analysis
- Photo-based mood tracking
- Visual therapy assessment

## 💬 Step 7: Supabase Real-time Features

### Peer Support Chat
- Instant messaging between users
- Anonymous support groups
- Crisis intervention alerts

### Live Therapy Sessions
- Real-time video/audio calls
- Screen sharing for art therapy
- Group meditation sessions

## 🚨 Step 8: Crisis Detection Enhancement

### Current System
- Uses Gemini AI for text analysis
- Basic keyword detection
- Static response system

### Enhanced System (With APIs)
- Multi-modal crisis detection (text + voice + image)
- Automatic SMS/call alerts via Twilio
- Real-time counselor notifications
- Emergency contact integration

## 🎨 Step 9: Remove Dummy Data & Emojis

### Automated Cleanup Script
```python
python utils/cleanup_dummy_data.py
```

This will:
- Remove 90% of emojis from templates
- Replace dummy data with real API calls
- Clean up placeholder content
- Optimize for production

## 🧪 Step 10: Testing Real APIs

### Test Spotify Connection
```bash
python test_spotify_integration.py
```

### Test Google Cloud Services  
```bash
python test_google_cloud.py
```

### Test Database Connection
```bash
python test_mongodb_connection.py
```

### Test Complete System
```bash
python test_complete_system.py
```

## 🚀 Step 11: Production Deployment

### Update Environment
```bash
# In .env file:
FLASK_ENV=production
FLASK_DEBUG=False
```

### Run Production Server
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

## 📊 Expected Impact

### Before (Current State)
- ❌ Dummy music recommendations
- ❌ Static emotion analysis
- ❌ No real-time features
- ❌ SQLite limitations
- ❌ Excessive emojis/placeholder content

### After (With Real APIs)
- ✅ Personalized Spotify playlists
- ✅ Multi-modal emotion detection
- ✅ Real-time peer support
- ✅ Scalable MongoDB storage
- ✅ Production-ready interface
- ✅ Advanced Google AI features

## 🏆 GenAI Hackathon Benefits

1. **Technical Excellence**: Real API integrations vs dummy implementations
2. **Scalability**: MongoDB + Supabase vs SQLite limitations  
3. **User Experience**: Functional music therapy, real-time chat, voice features
4. **Innovation**: Multi-modal AI analysis using Google Cloud suite
5. **Production Ready**: Clean codebase, proper error handling, security

## ❓ Support & Troubleshooting

### Common Issues
1. **API Key Errors**: Double-check .env file syntax
2. **Database Connection**: Verify MongoDB URI format
3. **Spotify Auth**: Ensure redirect URI matches exactly
4. **Google Cloud**: Check service account permissions

### Next Steps
Once you provide the API keys, I'll help you:
1. Test each integration individually
2. Fix any configuration issues
3. Optimize performance
4. Prepare final hackathon presentation

**Ready to transform dummy data into a fully functional mental wellness platform! 🚀**