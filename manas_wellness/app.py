# 🧠 Manas: Youth Mental Wellness Platform
# Google GenAI Exchange Hackathon 2025
# Multi-modal AI-powered mental health support for Indian youth

from flask import Flask, render_template, request, jsonify, send_file, session
import sqlite3
import os
import json
import uuid
import tempfile
import base64
import wave
from datetime import datetime, timedelta
import logging
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import utility modules
from utils.gemini_api import gemini_text, gemini_multimodal, gemini_analyze_emotion
from utils.emotion_detector import EmotionDetector
from utils.therapy_generator import TherapyGenerator
from utils.crisis_detector import CrisisDetector
from utils.accessibility_engine import AccessibilityEngine
from utils.offline_manager import OfflineManager
from utils.multi_language_processor import MultiLanguageProcessor

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'manas_secret_key_2025')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'wav', 'mp3', 'mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize core components
emotion_detector = EmotionDetector()
therapy_generator = TherapyGenerator()
crisis_detector = CrisisDetector()
accessibility_engine = AccessibilityEngine()
offline_manager = OfflineManager()
multi_language_processor = MultiLanguageProcessor()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    """Get SQLite database connection"""
    conn = sqlite3.connect('manas_wellness.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    
    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            name TEXT,
            age INTEGER,
            language TEXT DEFAULT 'english',
            accessibility_needs TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Emotional states table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS emotional_states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            emotion_data TEXT,
            modality TEXT,
            confidence REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Therapy sessions table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS therapy_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            therapy_type TEXT,
            content TEXT,
            effectiveness_rating INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Crisis alerts table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS crisis_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            risk_level REAL,
            alert_type TEXT,
            intervention_taken TEXT,
            resolved BOOLEAN DEFAULT FALSE,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Feedback table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            feedback_type TEXT,
            rating INTEGER,
            comments TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Journal entries table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            content TEXT NOT NULL,
            content_encrypted TEXT,
            mood TEXT,
            energy_level TEXT,
            sleep_quality TEXT,
            tags TEXT,
            sentiment_score REAL,
            emotion_detected TEXT,
            voice_file_path TEXT,
            voice_transcript TEXT,
            images TEXT,
            streak_count INTEGER DEFAULT 0,
            word_count INTEGER DEFAULT 0,
            ai_insights TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # User streak tracking table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            total_entries INTEGER DEFAULT 0,
            last_entry_date DATE,
            streak_milestones TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# ==================== ROUTES ====================

@app.route('/')
def home():
    """Landing page for Manas platform"""
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard for authenticated users"""
    user_id = session.get('user_id')
    if not user_id:
        return render_template('auth.html')
    
    # Get user's recent emotional states and therapy sessions
    conn = get_db_connection()
    
    recent_emotions = conn.execute('''
        SELECT * FROM emotional_states 
        WHERE user_id = ? 
        ORDER BY timestamp DESC 
        LIMIT 10
    ''', (user_id,)).fetchall()
    
    recent_sessions = conn.execute('''
        SELECT * FROM therapy_sessions 
        WHERE user_id = ? 
        ORDER BY timestamp DESC 
        LIMIT 5
    ''', (user_id,)).fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         recent_emotions=recent_emotions,
                         recent_sessions=recent_sessions)

@app.route('/api/auth/register', methods=['POST'])
def register_user():
    """Register new user"""
    data = request.json
    user_id = str(uuid.uuid4())
    
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO users (user_id, name, age, language, accessibility_needs)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, data.get('name'), data.get('age'), 
              data.get('language', 'english'), data.get('accessibility_needs', '')))
        conn.commit()
        
        session['user_id'] = user_id
        session['user_name'] = data.get('name')
        
        return jsonify({'success': True, 'user_id': user_id})
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    finally:
        conn.close()

@app.route('/api/emotion/analyze', methods=['POST'])
def analyze_emotion():
    """Multi-modal emotion analysis endpoint"""
    user_id = session.get('user_id', 'demo_user')  # Use demo_user if not authenticated
    
    session_id = request.json.get('session_id', str(uuid.uuid4())) if request.is_json else str(uuid.uuid4())
    
    try:
        # Handle different input modalities
        if 'image' in request.files:
            # Visual emotion detection
            image_file = request.files['image']
            if image_file and allowed_file(image_file.filename):
                # Generate unique filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_extension = image_file.filename.rsplit('.', 1)[1].lower()
                filename = f"emotion_capture_{user_id}_{timestamp}.{file_extension}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image_file.save(filepath)
                
                emotion_result = emotion_detector.analyze_facial_emotion(filepath)
                modality = 'visual'
                
                # Store filepath in emotion result for reference
                emotion_result['image_path'] = filename
        
        elif 'audio' in request.files:
            # Voice emotion detection
            audio_file = request.files['audio']
            if audio_file and allowed_file(audio_file.filename):
                # Generate unique filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_extension = audio_file.filename.rsplit('.', 1)[1].lower()
                filename = f"emotion_audio_{user_id}_{timestamp}.{file_extension}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                audio_file.save(filepath)
                
                emotion_result = emotion_detector.analyze_voice_emotion(filepath)
                modality = 'audio'
                
                # Store filepath in emotion result for reference
                emotion_result['audio_path'] = filename
        
        elif request.is_json and 'text' in request.json:
            # Text emotion analysis
            text = request.json['text']
            emotion_result = emotion_detector.analyze_text_emotion(text)
            modality = 'text'
        
        elif request.form.get('text'):
            # Text emotion analysis from form data
            text = request.form.get('text')
            emotion_result = emotion_detector.analyze_text_emotion(text)
            modality = 'text'
        
        else:
            return jsonify({'success': False, 'error': 'No valid input provided'})
        
        # Store emotion data
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO emotional_states (user_id, session_id, emotion_data, modality, confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, session_id, json.dumps(emotion_result), modality, emotion_result.get('confidence', 0.0)))
        conn.commit()
        conn.close()
        
        # Check for crisis indicators
        risk_assessment = crisis_detector.assess_risk(emotion_result, user_id)
        
        return jsonify({
            'success': True,
            'emotion_result': emotion_result,
            'risk_assessment': risk_assessment,
            'session_id': session_id
        })
        
    except Exception as e:
        logger.error(f"Emotion analysis error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/therapy/generate', methods=['POST'])
def generate_therapy():
    """Generate personalized therapy content"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'User not authenticated'})
    
    data = request.json
    emotion_state = data.get('emotion_state')
    session_id = data.get('session_id', str(uuid.uuid4()))
    
    try:
        # Get user profile for personalization
        conn = get_db_connection()
        user_profile = conn.execute('''
            SELECT * FROM users WHERE user_id = ?
        ''', (user_id,)).fetchone()
        
        # Generate personalized therapy
        therapy_content = therapy_generator.generate_personalized_therapy(
            emotion_state, dict(user_profile) if user_profile else {}
        )
        
        # Store therapy session
        conn.execute('''
            INSERT INTO therapy_sessions (user_id, session_id, therapy_type, content)
            VALUES (?, ?, ?, ?)
        ''', (user_id, session_id, therapy_content['type'], json.dumps(therapy_content)))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'therapy_content': therapy_content,
            'session_id': session_id
        })
        
    except Exception as e:
        logger.error(f"Therapy generation error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/therapy/recommendations', methods=['POST'])
def get_therapy_recommendations():
    """Get quick therapy recommendations based on current emotion"""
    data = request.json
    primary_emotion = data.get('primary_emotion', 'neutral')
    confidence = data.get('confidence', 0.5)
    request_type = data.get('request_type', 'recommendations_only')
    
    try:
        # Generate emotion-specific recommendations
        recommendations = []
        
        emotion_recommendations = {
            'happy': [
                {
                    'title': 'Maintain Your Positive Energy',
                    'description': 'Continue engaging in activities that bring you joy. Consider sharing your positive energy with others.',
                    'duration': '5-10 minutes'
                },
                {
                    'title': 'Gratitude Practice',
                    'description': 'Write down 3 things you\'re grateful for today to reinforce positive feelings.',
                    'duration': '3-5 minutes'
                }
            ],
            'sad': [
                {
                    'title': 'Gentle Self-Care',
                    'description': 'Try deep breathing exercises or listen to calming music. It\'s okay to feel this way.',
                    'duration': '10-15 minutes'
                },
                {
                    'title': 'Connect with Support',
                    'description': 'Reach out to a trusted friend or family member. Social support can be very healing.',
                    'duration': 'As needed'
                }
            ],
            'angry': [
                {
                    'title': 'Release Physical Tension',
                    'description': 'Try progressive muscle relaxation or take a brisk walk to release built-up energy.',
                    'duration': '10-20 minutes'
                },
                {
                    'title': 'Mindful Breathing',
                    'description': 'Practice the 4-7-8 breathing technique: inhale for 4, hold for 7, exhale for 8.',
                    'duration': '5-10 minutes'
                }
            ],
            'anxious': [
                {
                    'title': 'Grounding Exercise',
                    'description': 'Try the 5-4-3-2-1 technique: 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste.',
                    'duration': '5-10 minutes'
                },
                {
                    'title': 'Structured Problem-Solving',
                    'description': 'Write down your worries and break them into manageable steps with action plans.',
                    'duration': '15-20 minutes'
                }
            ],
            'stressed': [
                {
                    'title': 'Stress Relief Breathing',
                    'description': 'Practice diaphragmatic breathing while sitting comfortably. Focus only on your breath.',
                    'duration': '10-15 minutes'
                },
                {
                    'title': 'Quick Body Scan',
                    'description': 'Notice areas of tension in your body and consciously relax them one by one.',
                    'duration': '5-10 minutes'
                }
            ],
            'neutral': [
                {
                    'title': 'Mindfulness Moment',
                    'description': 'Take a few minutes to simply observe your thoughts and feelings without judgment.',
                    'duration': '5-10 minutes'
                },
                {
                    'title': 'Set Positive Intentions',
                    'description': 'Use this balanced state to set clear intentions for the rest of your day.',
                    'duration': '5 minutes'
                }
            ]
        }
        
        # Get recommendations for the primary emotion
        recommendations = emotion_recommendations.get(primary_emotion, emotion_recommendations['neutral'])
        
        # Add confidence-based recommendations
        if confidence < 0.6:
            recommendations.append({
                'title': 'Explore Your Feelings',
                'description': 'Your emotions seem mixed. Try journaling to gain clarity about what you\'re experiencing.',
                'duration': '10-15 minutes'
            })
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'emotion': primary_emotion,
            'confidence': confidence
        })
        
    except Exception as e:
        logger.error(f"Therapy recommendations error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/crisis/check', methods=['POST'])
def crisis_check():
    """Crisis detection and intervention"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'User not authenticated'})
    
    data = request.json
    user_data = data.get('user_data')
    
    try:
        risk_level = crisis_detector.analyze_risk_level(user_data)
        
        if risk_level >= 0.8:  # High risk
            intervention = crisis_detector.emergency_protocol(user_id)
            
            # Log crisis alert
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO crisis_alerts (user_id, risk_level, alert_type, intervention_taken)
                VALUES (?, ?, ?, ?)
            ''', (user_id, risk_level, 'emergency', json.dumps(intervention)))
            conn.commit()
            conn.close()
            
        elif risk_level >= 0.5:  # Moderate risk
            intervention = crisis_detector.support_resources(user_id)
        else:
            intervention = crisis_detector.preventative_guidance(user_id)
        
        return jsonify({
            'success': True,
            'risk_level': risk_level,
            'intervention': intervention
        })
        
    except Exception as e:
        logger.error(f"Crisis check error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/accessibility/navigate', methods=['POST'])
def accessibility_navigate():
    """Eye tracking and accessibility navigation"""
    data = request.json
    
    try:
        if 'eye_tracking_data' in data:
            navigation_result = accessibility_engine.process_eye_tracking(data['eye_tracking_data'])
        elif 'gesture_data' in data:
            navigation_result = accessibility_engine.process_gesture(data['gesture_data'])
        else:
            return jsonify({'success': False, 'error': 'No accessibility data provided'})
        
        return jsonify({
            'success': True,
            'navigation_result': navigation_result
        })
        
    except Exception as e:
        logger.error(f"Accessibility navigation error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/feedback/submit', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'User not authenticated'})
    
    data = request.json
    session_id = data.get('session_id')
    feedback_type = data.get('type')
    rating = data.get('rating')
    comments = data.get('comments', '')
    
    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO feedback (user_id, session_id, feedback_type, rating, comments)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, session_id, feedback_type, rating, comments))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Feedback submission error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/offline/sync', methods=['POST'])
def offline_sync():
    """Sync offline data when connection is available"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'User not authenticated'})
    
    data = request.json
    offline_data = data.get('offline_data', [])
    
    try:
        sync_result = offline_manager.sync_offline_data(user_id, offline_data)
        return jsonify({
            'success': True,
            'sync_result': sync_result
        })
        
    except Exception as e:
        logger.error(f"Offline sync error: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/language/translate', methods=['POST'])
def translate_content():
    """Multi-language content translation"""
    data = request.json
    text = data.get('text')
    target_language = data.get('target_language', 'english')
    
    try:
        translated_text = multi_language_processor.translate(text, target_language)
        return jsonify({
            'success': True,
            'translated_text': translated_text
        })
        
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return jsonify({'success': False, 'error': str(e)})

# ==================== TEMPLATE ROUTES ====================

@app.route('/emotion-analysis')
def emotion_analysis_page():
    """Emotion analysis interface"""
    return render_template('emotion_analysis.html')

@app.route('/therapy-session')
def therapy_session_page():
    """Therapy session interface"""
    # Get emotion from URL parameters if coming from emotion analysis
    emotion = request.args.get('emotion', '')
    source = request.args.get('source', '')
    return render_template('therapy_session.html', initial_emotion=emotion, source=source)

@app.route('/crisis-support')
def crisis_support_page():
    """Crisis support interface"""
    return render_template('crisis_support.html')

@app.route('/accessibility')
def accessibility_page():
    """Accessibility features interface"""
    return render_template('accessibility.html')

@app.route('/analytics')
def analytics_page():
    """User analytics and progress tracking"""
    user_id = session.get('user_id')
    if not user_id:
        return render_template('auth.html')
    
    return render_template('analytics.html')

@app.route('/journal', methods=['GET', 'POST'])
def journal_page():
    """Enhanced AI-powered journal interface with rich features"""
    if request.method == 'POST':
        try:
            # Get form data
            journal_entry = request.form.get('journal_entry', '').strip()
            text_content = request.form.get('text_content', journal_entry).strip()
            mood = request.form.get('mood', '')
            energy_level = request.form.get('energy_level', '')
            sleep_quality = request.form.get('sleep_quality', '')
            tags = request.form.get('tags', '')
            word_count = int(request.form.get('word_count', 0))
            
            if not text_content:
                return jsonify({'success': False, 'message': 'Journal entry is required'})
            
            # Generate user ID if not exists
            user_id = session.get('user_id')
            if not user_id:
                user_id = str(uuid.uuid4())
                session['user_id'] = user_id
            
            # Simple mood emoji mapping
            mood_emojis = {
                'very_happy': '😄',
                'happy': '😊',
                'neutral': '😐',
                'sad': '😔',
                'anxious': '😰'
            }
            
            mood_emoji = mood_emojis.get(mood, '😐')
            
            # Analyze journal entry with Google GenAI
            analysis_prompt = f"""
            Analyze this journal entry for comprehensive mental wellness insights:
            
            Entry: {text_content}
            Mood: {mood}
            Energy Level: {energy_level}
            Sleep Quality: {sleep_quality}
            Tags: {tags}
            
            Provide detailed analysis including:
            1. Emotional patterns and sentiment analysis
            2. Mental wellness recommendations
            3. Positive affirmations and encouragement
            4. Suggested mindfulness activities
            5. Sleep and energy optimization tips
            
            Keep response supportive, encouraging, and culturally sensitive.
            Limit response to 400 words.
            """
            
            # Get AI insights
            ai_insights = gemini_text(analysis_prompt)
            
            if not ai_insights:
                ai_insights = "Thank you for sharing your thoughts today. Your commitment to mental wellness through journaling is commendable. Regular self-reflection helps build emotional intelligence and resilience."
            
            # Simple sentiment analysis
            emotion_detected = "Neutral"
            sentiment_score = 0.5
            
            try:
                positive_words = ['happy', 'good', 'great', 'wonderful', 'amazing', 'love', 'joy', 'excited', 'grateful', 'blessed', 'peaceful', 'content']
                negative_words = ['sad', 'bad', 'terrible', 'awful', 'hate', 'angry', 'frustrated', 'stressed', 'anxious', 'worried', 'depressed', 'lonely']
                
                text_lower = text_content.lower()
                positive_count = sum(1 for word in positive_words if word in text_lower)
                negative_count = sum(1 for word in negative_words if word in text_lower)
                
                if positive_count > negative_count:
                    sentiment_score = 0.7 + min(positive_count * 0.05, 0.3)
                    emotion_detected = "Positive"
                elif negative_count > positive_count:
                    sentiment_score = max(0.3 - negative_count * 0.05, 0.0)
                    emotion_detected = "Negative"
                else:
                    sentiment_score = 0.5
                    emotion_detected = "Neutral"
                    
            except Exception as e:
                logger.error(f"Sentiment analysis error: {e}")
            
            # Save to database
            conn = get_db_connection()
            
            # Ensure enhanced journal_entries table exists
            conn.execute('''
                CREATE TABLE IF NOT EXISTS journal_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    mood TEXT,
                    mood_emoji TEXT,
                    energy_level TEXT,
                    sleep_quality TEXT,
                    ai_insights TEXT,
                    content_encrypted BOOLEAN DEFAULT FALSE,
                    tags TEXT,
                    sentiment_score REAL,
                    emotion_detected TEXT,
                    voice_file_path TEXT,
                    voice_transcript TEXT,
                    images TEXT,
                    streak_count INTEGER DEFAULT 0,
                    word_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Calculate current streak
            current_streak = get_current_streak(user_id, conn)
            
            # Insert enhanced journal entry
            conn.execute('''
                INSERT INTO journal_entries (
                    user_id, content, mood, mood_emoji, energy_level, sleep_quality, ai_insights,
                    content_encrypted, tags, sentiment_score, emotion_detected,
                    voice_file_path, voice_transcript, images, streak_count, word_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, journal_entry, mood, mood_emoji, energy_level, sleep_quality, ai_insights,
                False, tags, sentiment_score, emotion_detected,
                None, None, None, current_streak, word_count
            ))
            
            # Update streak data
            update_user_streak(user_id, conn)
            
            conn.commit()
            conn.close()
            
            # Parse AI insights for frontend
            insights = {
                'mood_analysis': f"Your emotional state shows {emotion_detected.lower()} sentiment with a score of {sentiment_score:.2f}. " + (ai_insights[:150] if ai_insights else ''),
                'recommendations': ai_insights[150:] if len(ai_insights) > 150 else 'Continue your excellent mental wellness journey with regular journaling and mindfulness practices.'
            }
            
            return jsonify({
                'success': True,
                'message': 'Enhanced journal entry saved successfully!',
                'insights': insights,
                'sentiment_score': sentiment_score,
                'emotion_detected': emotion_detected,
                'current_streak': current_streak
            })
            
        except Exception as e:
            logger.error(f"Enhanced journal error: {e}")
            return jsonify({'success': False, 'message': 'Error processing journal entry. Please try again.'})
    
    # GET request - show enhanced journal page with previous entries
    try:
        user_id = session.get('user_id')
        journal_entries = []
        streak_data = {'current_streak': 0, 'longest_streak': 0, 'total_entries': 0}
        
        if user_id:
            conn = get_db_connection()
            
            # Ensure table exists
            conn.execute('''
                CREATE TABLE IF NOT EXISTS journal_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    mood TEXT,
                    mood_emoji TEXT,
                    energy_level TEXT,
                    sleep_quality TEXT,
                    ai_insights TEXT,
                    content_encrypted BOOLEAN DEFAULT FALSE,
                    tags TEXT,
                    sentiment_score REAL,
                    emotion_detected TEXT,
                    voice_file_path TEXT,
                    voice_transcript TEXT,
                    images TEXT,
                    streak_count INTEGER DEFAULT 0,
                    word_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Get recent journal entries
            entries = conn.execute('''
                SELECT * FROM journal_entries 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT 20
            ''', (user_id,)).fetchall()
            
            # Convert to list of dicts
            journal_entries = []
            for entry in entries:
                entry_dict = dict(entry)
                try:
                    entry_dict['created_at'] = datetime.fromisoformat(entry['created_at'])
                except:
                    entry_dict['created_at'] = datetime.now()
                journal_entries.append(entry_dict)
            
            # Get streak data
            streak_data = get_user_streak_data(user_id, conn)
            
            conn.close()
    
        return render_template('journal_enhanced.html', 
                             journal_entries=journal_entries,
                             streak_data=streak_data)
        
    except Exception as e:
        logger.error(f"Journal page error: {e}")
        return render_template('journal_enhanced.html', 
                             journal_entries=[],
                             streak_data={'current_streak': 0, 'longest_streak': 0, 'total_entries': 0})

def get_current_streak(user_id, conn):
    """Calculate current journaling streak for user"""
    try:
        # Count consecutive days with journal entries
        entries = conn.execute('''
            SELECT DATE(created_at) as entry_date 
            FROM journal_entries 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        ''', (user_id,)).fetchall()
        
        if not entries:
            return 0
        
        today = datetime.now().date()
        current_streak = 0
        
        # Check if there's an entry today or yesterday (to account for late night entries)
        for i, entry in enumerate(entries):
            entry_date = datetime.fromisoformat(entry['entry_date']).date()
            days_diff = (today - entry_date).days
            
            if i == 0 and days_diff <= 1:  # First entry should be today or yesterday
                current_streak = 1
            elif days_diff == current_streak:  # Consecutive day
                current_streak += 1
            else:
                break
        
        return current_streak
        
    except Exception as e:
        logger.error(f"Streak calculation error: {e}")
        return 0

def update_user_streak(user_id, conn):
    """Update user streak data in database"""
    try:
        # Create user_streaks table if not exists
        conn.execute('''
            CREATE TABLE IF NOT EXISTS user_streaks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                total_entries INTEGER DEFAULT 0,
                last_entry_date DATE,
                streak_milestones TEXT,  -- JSON array of achieved milestones
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Get current values
        current_streak = get_current_streak(user_id, conn)
        
        # Get total entries
        total_entries = conn.execute('''
            SELECT COUNT(*) as count 
            FROM journal_entries 
            WHERE user_id = ?
        ''', (user_id,)).fetchone()['count']
        
        # Get or create user streak record
        existing = conn.execute('''
            SELECT * FROM user_streaks WHERE user_id = ?
        ''', (user_id,)).fetchone()
        
        if existing:
            longest_streak = max(existing['longest_streak'], current_streak)
            conn.execute('''
                UPDATE user_streaks 
                SET current_streak = ?, longest_streak = ?, total_entries = ?, 
                    last_entry_date = DATE('now'), updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (current_streak, longest_streak, total_entries, user_id))
        else:
            conn.execute('''
                INSERT INTO user_streaks (user_id, current_streak, longest_streak, total_entries, last_entry_date)
                VALUES (?, ?, ?, ?, DATE('now'))
            ''', (user_id, current_streak, current_streak, total_entries))
        
    except Exception as e:
        logger.error(f"Streak update error: {e}")

def get_user_streak_data(user_id, conn):
    """Get comprehensive streak data for user"""
    try:
        streak_record = conn.execute('''
            SELECT * FROM user_streaks WHERE user_id = ?
        ''', (user_id,)).fetchone()
        
        if streak_record:
            return {
                'current_streak': streak_record['current_streak'],
                'longest_streak': streak_record['longest_streak'],
                'total_entries': streak_record['total_entries']
            }
        else:
            return {'current_streak': 0, 'longest_streak': 0, 'total_entries': 0}
            
    except Exception as e:
        logger.error(f"Streak data error: {e}")
        return {'current_streak': 0, 'longest_streak': 0, 'total_entries': 0}

# ==================== VOICE AI CHAT ROUTES ====================

@app.route('/voice-ai-chat')
def voice_ai_chat_page():
    """Voice AI Chat interface with STT/TTS capabilities"""
    return render_template('voice_ai_chat.html')

@app.route('/api/voice-chat/analyze', methods=['POST'])
def analyze_voice_chat():
    """Analyze user speech and generate AI response"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        if not user_message:
            return jsonify({
                'success': False,
                'message': 'No message provided'
            })
        
        # Generate user ID if not exists
        user_id = session.get('user_id')
        if not user_id:
            user_id = str(uuid.uuid4())
            session['user_id'] = user_id
        
        # Enhanced analysis using Google GenAI with better error handling
        try:
            # Configure GenAI with provided API key
            import google.generativeai as genai
            api_key = "AIzaSyBEGmWmBVurFFQxMjVSue8Zreu_nMSX_WU"
            genai.configure(api_key=api_key)
            
            # Create model instance
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Enhanced analysis prompt
            analysis_prompt = f"""
            As an AI mental wellness mentor for students, analyze this message and provide insights:
            
            Student says: "{user_message}"
            
            Analyze and respond with:
            1. Sentiment (positive/negative/neutral)
            2. Emotional state (happy, sad, anxious, stressed, excited, calm, worried, confident, etc.)
            3. Key emotional keywords found
            4. Supportive response (2-3 encouraging sentences)
            
            Respond in this exact JSON format:
            {{
                "sentiment": "positive/negative/neutral",
                "confidence": 0.8,
                "emotion": "emotional_state",
                "keywords": ["keyword1", "keyword2"],
                "response": "Your supportive response here"
            }}
            
            Keep responses warm, understanding, and professionally supportive for students.
            """
            
            # Generate AI response
            ai_response = model.generate_content(analysis_prompt)
            
            # Parse JSON response
            response_text = ai_response.text.strip()
            
            # Extract JSON from response
            import re
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response_text, re.DOTALL)
            
            if json_match:
                try:
                    analysis_data = json.loads(json_match.group())
                    # Validate required fields
                    if not all(key in analysis_data for key in ['sentiment', 'emotion', 'response']):
                        raise ValueError("Missing required fields")
                except (json.JSONDecodeError, ValueError) as e:
                    logger.error(f"JSON parsing error: {e}")
                    analysis_data = perform_fallback_analysis(user_message)
            else:
                logger.warning("No JSON found in AI response, using fallback")
                analysis_data = perform_fallback_analysis(user_message)
                
        except Exception as e:
            logger.error(f"Google GenAI error: {e}")
            # Use enhanced fallback analysis
            analysis_data = perform_fallback_analysis(user_message)
        
        # Use AI response from analysis or generate enhanced response
        ai_response_text = analysis_data.get('response', '')
        
        # If no response in analysis, generate one
        if not ai_response_text or len(ai_response_text.strip()) < 10:
            try:
                response_prompt = f"""
                As a supportive AI mental wellness mentor for students, respond to: "{user_message}"
                
                Detected sentiment: {analysis_data.get('sentiment', 'neutral')}
                Emotional state: {analysis_data.get('emotion', 'neutral')}
                
                Provide a warm, empathetic response (2-3 sentences) that:
                - Acknowledges their feelings
                - Offers encouragement or practical advice
                - Is supportive and age-appropriate for students
                
                Response:
                """
                
                # Generate response using configured GenAI
                response_result = model.generate_content(response_prompt)
                ai_response_text = response_result.text.strip()
                
                # Clean up response (remove quotes, extra formatting)
                ai_response_text = re.sub(r'^["\']|["\']$', '', ai_response_text)
                ai_response_text = ai_response_text.replace('Response:', '').strip()
                
            except Exception as e:
                logger.error(f"Response generation error: {e}")
                ai_response_text = generate_fallback_response(user_message, analysis_data.get('sentiment', 'neutral'))
        
        # Ensure we have a valid response
        if not ai_response_text or len(ai_response_text.strip()) < 5:
            ai_response_text = generate_fallback_response(user_message, analysis_data.get('sentiment', 'neutral'))
        
        # Save conversation to database
        save_voice_conversation(user_id, user_message, ai_response_text, analysis_data)
        
        # Prepare response
        return jsonify({
            'success': True,
            'analysis': {
                'sentiment': analysis_data.get('sentiment', 'neutral'),
                'confidence': analysis_data.get('confidence', 0.7),
                'emotion': analysis_data.get('emotion', 'Neutral'),
                'keywords': analysis_data.get('keywords', []),
                'sentiment_score': sentiment_to_score(analysis_data.get('sentiment', 'neutral'))
            },
            'response': ai_response_text
        })
        
    except Exception as e:
        logger.error(f"Voice chat analysis error: {e}")
        return jsonify({
            'success': False,
            'message': 'Error analyzing speech. Please try again.',
            'analysis': {
                'sentiment': 'neutral',
                'confidence': 0.5,
                'emotion': 'Neutral',
                'keywords': [],
                'sentiment_score': 0.5
            },
            'response': 'I apologize, but I encountered an error. Please try speaking again, and I\'ll do my best to help you.'
        })

def perform_fallback_analysis(message):
    """Enhanced fallback analysis when AI is unavailable"""
    message_lower = message.lower()
    
    # Expanded emotional vocabulary
    positive_words = [
        'happy', 'good', 'great', 'wonderful', 'amazing', 'love', 'joy', 'excited', 
        'grateful', 'blessed', 'peaceful', 'content', 'confident', 'motivated', 'proud',
        'optimistic', 'hopeful', 'cheerful', 'delighted', 'thrilled', 'satisfied', 'calm',
        'relaxed', 'comfortable', 'successful', 'accomplished', 'energetic', 'positive'
    ]
    
    negative_words = [
        'sad', 'bad', 'terrible', 'awful', 'hate', 'angry', 'frustrated', 'stressed', 
        'anxious', 'worried', 'depressed', 'lonely', 'confused', 'overwhelmed', 'tired',
        'upset', 'disappointed', 'scared', 'nervous', 'concerned', 'troubled', 'hurt',
        'irritated', 'exhausted', 'hopeless', 'discouraged', 'insecure', 'uncertain'
    ]
    
    # Academic/study related words
    study_words = ['exam', 'test', 'study', 'homework', 'assignment', 'grade', 'class', 'school', 'college', 'university', 'learning']
    stress_words = ['pressure', 'deadline', 'busy', 'overloaded', 'difficult', 'hard', 'struggling', 'challenge']
    
    positive_count = sum(1 for word in positive_words if word in message_lower)
    negative_count = sum(1 for word in negative_words if word in message_lower)
    study_count = sum(1 for word in study_words if word in message_lower)
    stress_count = sum(1 for word in stress_words if word in message_lower)
    
    # Determine sentiment and emotion
    if positive_count > negative_count:
        sentiment = "positive"
        confidence = min(0.7 + positive_count * 0.05, 0.95)
        if 'excited' in message_lower or 'thrilled' in message_lower:
            emotion = "Excited"
        elif 'calm' in message_lower or 'peaceful' in message_lower:
            emotion = "Calm"
        elif 'confident' in message_lower or 'proud' in message_lower:
            emotion = "Confident"
        else:
            emotion = "Happy"
    elif negative_count > positive_count or stress_count > 0:
        sentiment = "negative"
        confidence = min(0.7 + negative_count * 0.05, 0.95)
        if 'anxious' in message_lower or 'nervous' in message_lower:
            emotion = "Anxious"
        elif 'stressed' in message_lower or stress_count > 0:
            emotion = "Stressed"
        elif 'sad' in message_lower or 'depressed' in message_lower:
            emotion = "Sad"
        elif 'overwhelmed' in message_lower:
            emotion = "Overwhelmed"
        else:
            emotion = "Concerned"
    else:
        sentiment = "neutral"
        confidence = 0.75
        if study_count > 0:
            emotion = "Focused"
        else:
            emotion = "Thoughtful"
    
    # Extract relevant keywords
    keywords = []
    all_emotional_words = positive_words + negative_words + study_words + stress_words
    for word in all_emotional_words:
        if word in message_lower:
            keywords.append(word.capitalize())
    
    # Generate contextual response
    response = generate_contextual_response(message_lower, sentiment, emotion, study_count > 0, stress_count > 0)
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "emotion": emotion,
        "keywords": keywords[:5],  # Limit to 5 keywords
        "wellness_assessment": f"Student expressed {sentiment} sentiment with {emotion.lower()} emotional state.",
        "response": response
    }

def generate_contextual_response(message_lower, sentiment, emotion, is_study_related, is_stress_related):
    """Generate contextual response based on message analysis"""
    
    if sentiment == "positive":
        responses = [
            "I'm so glad to hear you're feeling positive! That energy is wonderful and I encourage you to keep nurturing it.",
            "Your positive attitude really shines through. Remember to celebrate these good moments and share that positivity with others.",
            "It's beautiful to hear such optimism from you. Keep building on these positive feelings through self-care and mindfulness."
        ]
    elif sentiment == "negative":
        if is_study_related or is_stress_related:
            responses = [
                "I understand that academic pressures can feel overwhelming. Remember that it's okay to take breaks and ask for help when you need it.",
                "Study stress is very common, and you're not alone in feeling this way. Consider breaking tasks into smaller steps and practicing some relaxation techniques.",
                "Academic challenges can be tough, but they're temporary. Try some deep breathing exercises and remember that your worth isn't defined by grades alone."
            ]
        elif emotion == "Anxious":
            responses = [
                "I hear that you're feeling anxious, and that's completely valid. Try focusing on your breathing - breathe in for 4 counts, hold for 4, and breathe out for 6.",
                "Anxiety can feel overwhelming, but remember that these feelings will pass. Consider grounding yourself by naming 5 things you can see around you right now.",
                "Thank you for sharing your anxious feelings with me. Remember that you're stronger than you think, and it's okay to reach out for support."
            ]
        else:
            responses = [
                "I hear that you're going through a difficult time right now. These feelings are valid, and it's important to be gentle with yourself.",
                "Thank you for trusting me with your feelings. Remember that tough times don't last, but resilient people like you do.",
                "It takes courage to express difficult emotions. Consider talking to a trusted friend or counselor about what you're experiencing."
            ]
    else:  # neutral
        if is_study_related:
            responses = [
                "It sounds like you're focused on your studies. Remember to balance your academic work with self-care and rest.",
                "I appreciate you sharing your thoughts about your academic journey. How can I best support your learning and well-being today?",
                "Your dedication to your studies is admirable. Don't forget to take breaks and check in with how you're feeling along the way."
            ]
        else:
            responses = [
                "Thank you for sharing your thoughts with me. I'm here to listen and support you in whatever way would be most helpful.",
                "I appreciate you taking the time to communicate with me. What would you like to focus on for your well-being today?",
                "Your willingness to engage shows great self-awareness. How can I best support your mental wellness journey right now?"
            ]
    
    import random
    return random.choice(responses)

def generate_fallback_response(message, sentiment):
    """Generate supportive response when AI is unavailable"""
    responses = {
        'positive': [
            "I'm glad to hear you're feeling positive! Keep nurturing those good feelings through self-care and mindfulness.",
            "Your positive energy is wonderful to hear. Remember to celebrate these moments and share them with others.",
            "It's great that you're in a good space. Consider keeping a gratitude journal to maintain this positive mindset."
        ],
        'negative': [
            "I hear that you're going through a difficult time. Remember that it's okay to feel this way, and these feelings will pass.",
            "Thank you for trusting me with your feelings. Consider talking to a counselor or trusted friend about what you're experiencing.",
            "Your feelings are valid and important. Try some deep breathing exercises or gentle movement to help process these emotions."
        ],
        'neutral': [
            "Thank you for sharing your thoughts with me. I'm here to listen and support you in your mental wellness journey.",
            "I appreciate you taking the time to communicate. How would you like to focus on your well-being today?",
            "Your willingness to engage in conversation shows your commitment to self-care. What would be most helpful for you right now?"
        ]
    }
    
    import random
    return random.choice(responses.get(sentiment, responses['neutral']))

def sentiment_to_score(sentiment):
    """Convert sentiment string to numerical score"""
    scores = {
        'positive': 0.8,
        'negative': 0.2,
        'neutral': 0.5
    }
    return scores.get(sentiment, 0.5)

def save_voice_conversation(user_id, user_message, ai_response, analysis_data):
    """Save voice conversation to database"""
    try:
        conn = get_db_connection()
        
        # Create voice_conversations table if not exists
        conn.execute('''
            CREATE TABLE IF NOT EXISTS voice_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                sentiment TEXT,
                confidence REAL,
                emotion TEXT,
                keywords TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert conversation
        conn.execute('''
            INSERT INTO voice_conversations (
                user_id, user_message, ai_response, sentiment, confidence, emotion, keywords
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            user_message,
            ai_response,
            analysis_data.get('sentiment', 'neutral'),
            analysis_data.get('confidence', 0.7),
            analysis_data.get('emotion', 'Neutral'),
            json.dumps(analysis_data.get('keywords', []))
        ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error saving voice conversation: {e}")

# ==================== FAVICON ROUTE ====================

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No Content

# ==================== SVG ICONS ROUTE ====================

@app.route('/svgicons/<filename>')
def serve_svg(filename):
    """Serve SVG icon files"""
    try:
        svg_path = os.path.join('svgicons', filename)
        if os.path.exists(svg_path) and filename.endswith('.svg'):
            return send_file(svg_path, mimetype='image/svg+xml')
        else:
            return '', 404
    except Exception as e:
        logger.error(f"Error serving SVG {filename}: {e}")
        return '', 404

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('utils', exist_ok=True)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)