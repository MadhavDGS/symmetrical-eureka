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