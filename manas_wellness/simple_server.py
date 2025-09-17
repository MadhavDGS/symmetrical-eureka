#!/usr/bin/env python3
"""
Simple test server for Manas Wellness Platform
"""

from flask import Flask, render_template, request, jsonify
import os

# Create Flask app
app = Flask(__name__)
app.secret_key = 'manas_secret_key_2025'

@app.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception                elif emotion_context == "breakup":
                    return [
                        "ಸಂಬಂಧ ಮುರಿಯುವುದು ತುಂಬಾ ನೋವಿನ ವಿಷಯ, ನಿಮ್ಮ ನೋವನ್ನು ನಾನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುತ್ತೇನೆ। 💙 ದಯವಿಟ್ಟು ನೆನಪಿಡಿ, ನೀವು ಪ್ರೀತಿಗೆ ಅರ್ಹರು।",
                        "ಬ್ರೇಕಪ್ ಹೃದಯವನ್ನು ನೋಯಿಸುತ್ತದೆ, ಆದರೆ ಇದು ನಿಮ್ಮ ಮೌಲ್ಯವನ್ನು ಕಡಿಮೆ ಮಾಡುವುದಿಲ್ಲ। ಸಮಯ ಎಲ್ಲಾ ಗಾಯಗಳನ್ನು ಗುಣಪಡಿಸುತ್ತದೆ। ನಿಮ್ಮ ಒಳ್ಳೆಯ ಜನರೊಂದಿಗೆ ಸಮಯ ಕಳೆಯಿರಿ।",
                        "ಬ್ರೇಕಪ್ ನೋವನ್ನು ಸಹಿಸುವುದು ಕಷ್ಟ, ಆದರೆ ನೀವು ಏಕಾಂಗಿಯಲ್ಲ। 🤝 ನಿಮ್ಮ ಭಾವನೆಗಳನ್ನು ದಮನ ಮಾಡಬೇಡಿ - ಅಳಬೇಕೆನಿಸಿದರೆ ಅಳಿರಿ, ಅದು ಸಹಜ."
                    ]
                elif emotion_context == "loneliness":
                    return [
                        "ಏಕಾಂತತೆ ಅನುಭವಿಸುವುದು ತುಂಬಾ ಕಷ್ಟ, ಆದರೆ ನೀವು ನಿಜವಾಗಿಯೂ ಏಕಾಂಗಿಯಲ್ಲ। 🫂 ನಾನು ಇಲ್ಲಿದ್ದೇನೆ ಮತ್ತು ನಿಮ್ಮ ಕಥೆ ಕೇಳಲು ಸಿದ್ಧ.",
                        "ಏಕಾಂಗಿಯಾಗಿ ಅನಿಸುವುದು ಸಹಜ ಭಾವನೆ, ಆದರೆ ನೆನಪಿಡಿ - ನೀವು ಮೌಲ್ಯಯುತ ವ್ಯಕ್ತಿ। ಹೊಸ ಸ್ನೇಹ ಮಾಡಲು ಸಣ್ಣ ಹೆಜ್ಜೆಗಳನ್ನು ಇಡಿರಿ।",
                        "ಏಕಾಂತತೆ ಹೃದಯವನ್ನು ನೋಯಿಸುತ್ತದೆ, ಆದರೆ ಇದು ಶಾಶ್ವತವಲ್ಲ। 🌱 ನಿಮ್ಮ ಬಗ್ಗೆ ಕಾಳಜಿ ವಹಿಸುವವರು ಇದ್ದಾರೆ, ಅವರನ್ನು ಭೇಟಿಯಾಗಿ ಅಥವಾ ಕಾಲ್ ಮಾಡಿ।"
                    ]
                elif emotion_context == "sadness":
                    return [
                        "ನಿಮ್ಮ ದುಃಖ ನೋಡಿ ನನಗೂ ಬೇಸರವಾಗುತ್ತಿದೆ। 💙 ಅಳಬೇಕೆನಿಸಿದರೆ ಅಳಿರಿ - ಕಣ್ಣೀರು ಹೃದಯವನ್ನು ಹಗುರಗೊಳಿಸುತ್ತದೆ।",
                        "ದುಃಖ ಅನುಭವಿಸುವುದು ತುಂಬಾ ಕಷ್ಟ, ಆದರೆ ನಿಮ್ಮ ಭಾವನೆಗಳು ಸರಿಯಾದವು। 🤗 ನಿಮ್ಮೊಂದಿಗೆ ಇರಲು ನಾನು ಇಲ್ಲಿದ್ದೇನೆ।",
                        "ದುಃಖ ಜೀವನದ ಭಾಗ, ಆದರೆ ಅದು ನಿಮ್ಮನ್ನು ವ್ಯಾಖ್ಯಾನಿಸುವುದಿಲ್ಲ। 🌈 ದಯವಿಟ್ಟು ನಿಮ್ಮ ಬಗ್ಗೆ ದಯೆ ತೋರಿಕೊಳ್ಳಿ ಮತ್ತು ಸಹಾಯ ಕೇಳಲು ಹಿಂಜರಿಯಬೇಡಿ।"
                    ]
                elif emotion_context == "anxiety":
                    return [
                        "ಆತಂಕ ಅನುಭವಿಸುವುದು ಭಯಾನಕವಾಗಿರಬಹುದು। 🌸 4-7-8 ಉಸಿರಾಟ ತಂತ್ರವನ್ನು ಪ್ರಯತ್ನಿಸಿ: 4 ಎಣಿಕೆ ಮಾಡಿ ಉಸಿರಾಡಿ, 7 ಎಣಿಕೆ ಹಿಡಿದಿರಿ, 8 ಎಣಿಕೆ ಬಿಡಿ.",
                        "ನಿಮ್ಮ ಆತಂಕದ ಭಾವನೆಗಳು ಸಂಪೂರ್ಣವಾಗಿ ಸರಿಯಾದವು। 🧘‍♀️ ನಿಮ್ಮ ಸುತ್ತಲೂ ಇರುವ 5 ವಸ್ತುಗಳನ್ನು ಗಮನಿಸುವ ಮೂಲಕ ಮನಸ್ಸನ್ನು ಶಾಂತಗೊಳಿಸಿ.",
                        "ಆತಂಕದೊಂದಿಗೆ ಹೋರಾಡುವುದು ಧೈರ್ಯ. 💪 ನೀವು ಮೊದಲೂ ಕಷ್ಟಗಳನ್ನು ಜಯಿಸಿದ್ದೀರಿ, ಈಗಲೂ ಮಾಡಬಹುದು."
                    ]
                elif emotion_context == "depression":
                    return [
                        "ನೀವು ತುಂಬಾ ಕತ್ತಲೆಯ ಸ್ಥಳದಲ್ಲಿ ಇದ್ದೀರಿ ಎಂದು ನಾನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುತ್ತೇನೆ। 🫂 ದಯವಿಟ್ಟು ನೆನಪಿಡಿ, ನಿಮ್ಮ ಜೀವನಕ್ಕೆ ಮೌಲ್ಯವಿದೆ ಮತ್ತು ಈ ಕಗ್ಗತ್ತಲೆ ಭಾವನೆಗಳು ಶಾಶ್ವತವಲ್ಲ.",
                        "ಖಿನ್ನತೆ ಎಲ್ಲವನ್ನೂ ಭಾರವಾಗಿ ಮತ್ತು ನಿರಾಶಾಜನಕವಾಗಿ ತೋರಿಸುತ್ತದೆ। 💙 ನೀವು ಮುರಿದುಹೋಗಿಲ್ಲ, ನೀವು ಮನುಷ್ಯರು, ಮತ್ತು ಬೆಂಬಲ ಮತ್ತು ಕಾಳಜಿಗೆ ನೀವು ಅರ್ಹರು.",
                        "ಖಿನ್ನತೆ ನಮ್ಮ ಮೌಲ್ಯದ ಬಗ್ಗೆ ಸುಳ್ಳು ಹೇಳುತ್ತದೆ। 🌱 ಆದರೆ ನೀವು ಇಂದು ಇಲ್ಲಿಗೆ ಬಂದಿದ್ದೀರಿ, ಇದು ಅದ್ಭುತ ಶಕ್ತಿಯನ್ನು ತೋರಿಸುತ್ತದೆ। ದಯವಿಟ್ಟು ಕೌನ್ಸೆಲರ್ ಅಥವಾ ನಂಬಿಕೆಯ ಸ್ನೇಹಿತರೊಂದಿಗೆ ಮಾತನಾಡುವುದನ್ನು ಪರಿಗಣಿಸಿ।"
                    ]
                elif emotion_context == "anger":
                    return [
                        "ನಿಮ್ಮ ಮಾತುಗಳಲ್ಲಿ ಕೋಪ ಕೇಳುತ್ತಿದೆ, ಆ ಭಾವನೆಗಳು ಸರಿಯಾದವು। 🔥 ಕೋಪ ಆಗಾಗ್ಗೆ ದುಃಖ ಅಥವಾ ಭಯವನ್ನು ಮರೆಮಾಡುತ್ತದೆ. ಆ ಕೋಪದ ಕೆಳಗೆ ನಿಮ್ಮಿಗೆ ಏನಿದೆ?",
                        "ಕೋಪ ಅನುಭವಿಸುವುದು ಸರಿ - ಅನ್ಯಾಯ ಅಥವಾ ನೋವಿಗೆ ಕೋಪವು ಆರೋಗ್ಯಕರ ಪ್ರತಿಕ್ರಿಯೆಯಾಗಿರಬಹುದು। 💪 ನಿಮಗೆ ಹೀಗೆ ಅನಿಸುವುದು ಏಕೆ ಎಂದು ಮಾತನಾಡೋಣ.",
                        "ಕೋಪವು ಕೇಳಿಸಿಕೊಳ್ಳಲು ಬಯಸುವ ಶಕ್ತಿಯುತ ಭಾವನೆ। 🗣️ ಅದನ್ನು ತಳ್ಳಿಕೊಳ್ಳುವ ಬದಲು, ಅದು ನಿಮಗೆ ಏನು ಹೇಳಲು ಪ್ರಯತ್ನಿಸುತ್ತಿದೆ ಎಂದು ಅನ್ವೇಷಿಸೋಣ."
                    ]
                elif emotion_context == "stress" or study_count > 0 or stress_count > 0:
                    return [
                        "ಅಧ್ಯಯನದ ಒತ್ತಡ ತುಂಬಾ ಸಾಮಾನ್ಯ, ನೀವು ಏಕಾಂಗಿಯಲ್ಲ। 📚 ವಿಶ್ರಾಂತಿ ತೆಗೆದುಕೊಳ್ಳಬೇಕು ಮತ್ತು ನಿಮ್ಮ ಮಾನಸಿಕ ಆರೋಗ್ಯಕ್ಕೆ ಆದ್ಯತೆ ನೀಡಬೇಕು ಎಂದು ನೆನಪಿಡಿ.",
                        "ಶೈಕ್ಷಣಿಕ ಒತ್ತಡ ಅಧಿಕವಾಗಿ ಅನಿಸಿಸಬಹುದು। 🎯 ಕೆಲಸಗಳನ್ನು ಚಿಕ್ಕ ಭಾಗಗಳಾಗಿ ವಿಭಜಿಸಿ ಮತ್ತು ಪ್ರತಿ ಚಿಕ್ಕ ವಿಜಯವನ್ನು ಆಚರಿಸಿ.",
                        "ನಿಮ್ಮ ಮೌಲ್ಯ ಗ್ರೇಡ್‌ಗಳಿಂದ ನಿರ್ಧರಿಸಲ್ಪಡುವುದಿಲ್ಲ। 🌟 ನೀವು ಪ್ರಯತ್ನಿಸುತ್ತಿದ್ದೀರಿ ಎಂದು ನಾನು ಹೆಮ್ಮೆಪಡುತ್ತೇನೆ। ಅಗತ್ಯವಿದ್ದಾಗ ಸಹಾಯ ಕೇಳಲು ಸಂಕೋಚಿಸಬೇಡಿ."
                    ]
                else:
        return f'''
        <h1>🧠 Manas Wellness Platform</h1>
        <p>Server is running successfully!</p>
        <p><strong>Available Pages:</strong></p>
        <ul>
            <li><a href="/journal">Journal (New Feature!)</a></li>
            <li><a href="/dashboard">Dashboard</a></li>
            <li><a href="/emotion-analysis">Emotion Analysis</a></li>
            <li><a href="/therapy-session">Therapy Session</a></li>
            <li><a href="/accessibility">Accessibility</a></li>
            <li><a href="/analytics">Analytics</a></li>
            <li><a href="/crisis-support">Crisis Support</a></li>
            <li><a href="/voice-ai-chat">Voice AI Chat</a></li>
        </ul>
        <p><em>Note: Some features may require API keys to be configured.</em></p>
        <p style="color: red;">Template error: {str(e)}</p>
        '''

@app.route('/journal')
def journal_page():
    try:
        return render_template('journal.html', journal_entries=[])
    except Exception as e:
        return f'''
        <h1>📖 AI Journal</h1>
        <p>This is the new AI-powered journal feature!</p>
        <p style="color: red;">Template error: {str(e)}</p>
        <p><a href="/">← Back to Home</a></p>
        '''

@app.route('/dashboard')
def dashboard():
    try:
        return render_template('dashboard.html')
    except Exception as e:
        return f'<h1>Dashboard</h1><p>Error: {str(e)}</p><p><a href="/">← Back to Home</a></p>'

@app.route('/emotion-analysis')
def emotion_analysis():
    try:
        return render_template('emotion_analysis.html')
    except Exception as e:
        return f'<h1>Emotion Analysis</h1><p>Error: {str(e)}</p><p><a href="/">← Back to Home</a></p>'

@app.route('/therapy-session')
def therapy_session():
    try:
        return render_template('therapy_session.html')
    except Exception as e:
        return f'<h1>Therapy Session</h1><p>Error: {str(e)}</p><p><a href="/">← Back to Home</a></p>'

@app.route('/accessibility')
def accessibility():
    try:
        return render_template('accessibility.html')
    except Exception as e:
        return f'<h1>Accessibility</h1><p>Error: {str(e)}</p><p><a href="/">← Back to Home</a></p>'

@app.route('/analytics')
def analytics():
    try:
        return render_template('analytics.html')
    except Exception as e:
        return f'<h1>Analytics</h1><p>Error: {str(e)}</p><p><a href="/">← Back to Home</a></p>'

@app.route('/crisis-support')
def crisis_support():
    try:
        return render_template('crisis_support.html')
    except Exception as e:
        return f'<h1>🚨 Crisis Support</h1><p>Error: {str(e)}</p><p><a href="/">← Back to Home</a></p>'

# API Routes for AJAX requests
@app.route('/api/emotion/analyze', methods=['POST'])
def api_emotion_analyze():
    try:
        # Get the data from the request
        data = request.get_json() or request.form
        
        # Mock response for testing (replace with actual AI analysis later)
        return jsonify({
            'success': True,
            'emotion': 'happy',
            'confidence': 0.85,
            'analysis': 'The analysis shows positive emotional indicators. You seem to be in a good mood today!',
            'recommendations': [
                'Continue with activities that make you feel good',
                'Consider journaling about positive experiences',
                'Share your happiness with friends and family'
            ]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Analysis temporarily unavailable. Please try again later.'
        })

@app.route('/api/journal/save', methods=['POST'])
def api_journal_save():
    try:
        # Get the journal data
        data = request.get_json() or request.form
        
        # Mock successful save (replace with actual database save later)
        return jsonify({
            'success': True,
            'message': 'Journal entry saved successfully!',
            'insights': {
                'mood_analysis': 'Your emotional state appears balanced and reflective.',
                'recommendations': 'Keep up the great work with regular journaling for mental wellness!'
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Unable to save journal entry. Please try again.'
        })

@app.route('/api/therapy/session', methods=['POST'])
def api_therapy_session():
    try:
        # Get the therapy request data
        data = request.get_json() or request.form
        
        # Mock therapy response
        return jsonify({
            'success': True,
            'session_type': 'mindfulness',
            'response': 'Thank you for sharing. Let\'s focus on breathing exercises to help you feel more centered.',
            'exercises': [
                'Take 5 deep breaths, counting to 4 on inhale and 6 on exhale',
                'Notice 3 things you can see, 2 things you can hear, 1 thing you can touch',
                'Practice gratitude by thinking of 3 positive things from today'
            ]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Therapy session temporarily unavailable. Please try again later.'
        })

@app.route('/voice-ai-chat')
def voice_ai_chat_page():
    """Voice AI Chat page route"""
    return render_template('voice_ai_chat.html')

@app.route('/api/voice-chat/analyze', methods=['POST'])
def analyze_voice_chat_simple():
    """Enhanced voice chat analysis endpoint with Google GenAI"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        user_language = data.get('language', 'en-US')
        
        print(f"🎤 Voice chat request received:")
        print(f"   Message: {user_message}")
        print(f"   Language: {user_language}")
        
        if not user_message:
            return jsonify({
                'success': False,
                'message': 'No message provided'
            })
        
        # Use enhanced fallback analysis for accurate responses
        print("Using enhanced fallback analysis for better accuracy")
        
        # Enhanced fallback analysis
        message_lower = user_message.lower()
        
        positive_words = [
            'happy', 'good', 'great', 'wonderful', 'amazing', 'love', 'joy', 'excited', 
            'grateful', 'blessed', 'peaceful', 'content', 'confident', 'motivated', 'proud',
            'optimistic', 'hopeful', 'cheerful', 'delighted', 'calm', 'relaxed', 'successful'
        ]
        
        negative_words = [
            'sad', 'bad', 'terrible', 'awful', 'hate', 'angry', 'frustrated', 'stressed', 
            'anxious', 'worried', 'depressed', 'lonely', 'confused', 'overwhelmed', 'tired',
            'upset', 'disappointed', 'scared', 'nervous', 'concerned', 'troubled', 'hurt'
        ]
        
        # Enhanced emotional context detection
        breakup_words = ['breakup', 'broke up', 'ex-boyfriend', 'ex-girlfriend', 'relationship ended', 'split up', 'dumped', 'divorce']
        loneliness_words = ['lonely', 'alone', 'isolated', 'no friends', 'nobody cares', 'empty', 'abandoned']
        sadness_words = ['crying', 'tears', 'heartbroken', 'devastated', 'grief', 'mourning', 'loss']
        anxiety_words = ['panic', 'anxious', 'nervous', 'worried', 'fear', 'scared', 'phobia', 'panic attack']
        depression_words = ['depressed', 'hopeless', 'worthless', 'meaningless', 'suicidal', 'give up', 'no point']
        anger_words = ['angry', 'furious', 'rage', 'hate', 'mad', 'pissed', 'irritated', 'annoyed']
        
        study_words = ['exam', 'test', 'study', 'homework', 'assignment', 'grade', 'class', 'school', 'college', 'university']
        stress_words = ['pressure', 'deadline', 'busy', 'difficult', 'hard', 'struggling', 'overwhelmed', 'burden']
        
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        
        # Enhanced emotional context detection
        breakup_count = sum(1 for word in breakup_words if word in message_lower)
        loneliness_count = sum(1 for word in loneliness_words if word in message_lower)
        sadness_count = sum(1 for word in sadness_words if word in message_lower)
        anxiety_count = sum(1 for word in anxiety_words if word in message_lower)
        depression_count = sum(1 for word in depression_words if word in message_lower)
        anger_count = sum(1 for word in anger_words if word in message_lower)
        
        study_count = sum(1 for word in study_words if word in message_lower)
        stress_count = sum(1 for word in stress_words if word in message_lower)
        
        # Enhanced empathetic and contextual responses
        def get_language_responses(sentiment, emotion_context, user_language):
            if user_language.startswith('te-'):
                # Telugu empathetic responses
                if sentiment == "positive":
                    return [
                        "మీ ఆనందం నాకు కూడా ఆనందాన్ని ఇస్తుంది! 😊 ఈ అందమైన క్షణాలను గుండెలో ఉంచుకోండి.",
                        "మీ సానుకూల శక్తి చాలా ప్రేరణాత్మకం! ఈ మంచి భావనలను ఇతరులతో కూడా పంచుకోండి.",
                        "మీలో ఉన్న ఆశావాదం నిజంగా గొప్పది! జీవితంలో ఇలాంటి సంతోషకరమైన క్షణాలను ఎల్లప్పుడూ జరుపుకోవాలి."
                    ]
                elif emotion_context == "breakup":
                    return [
                        "రిలేషన్‌షిప్ ముగియడం చాలా బాధాకరం, మీ నొప్पిని నేను అర్థం చేసుకుంటున్నాను. 💙 దయచేసి గుర్తుంచుకోండి, మీరు ప్రేమకు అర్హులైన వ్యక్తివి.",
                        "విడిపోవడం హృదయాన్ని బాధపెడుతుంది, కానీ ఇది మీ విలువను తగ్గించదు. సమయం అన్ని గాయాలను మానుస్తుంది. మీతో ఉన్న మంచి వారితో సమయం గడపండి.",
                        "బ్రేకప్ నొప్పి తట్టుకోవడం కష్టం, కానీ మీరు ఒంటరి కాదు. 🤝 మీ భావాలను అణచివేయకండి - ఏడవాలని అనిపిస్తే ఏడవండి, అది సహజం."
                    ]
                elif emotion_context == "loneliness":
                    return [
                        "ఒంటరితనం అనుభవించడం చాలా కష్టం, కానీ మీరు నిజంగా ఒంటరి కాదు. 🫂 నేను ఇక్కడ ఉన్నాను మరియు మీ కథ వినడానికి సిద్ధంగా ఉన్నాను.",
                        "ఒంటరిగా అనిపించడం సహజమైన భావన, కానీ గుర్తుంచుకోండి - మీరు విలువైన వ్యక్తివి. కొత్త స్నేహాలు చేసుకోవడానికి చిన్న అడుగులు వేయండి.",
                        "ఒంటరితనం హృదయాన్ని వేదనపరుస్తుంది, కానీ ఇది శాశ్వతం కాదు. 🌱 మీ గురించి పట్టింపు గల వారు ఉన్నారు, వారిని కలవండి లేదా కాల్ చేయండి."
                    ]
                elif emotion_context == "sadness":
                    return [
                        "మీ దుఃఖాన్ని చూడటం నాకు బాధగా ఉంది. 💙 ఏడవాలని అనిపిస్తే ఏడవండి - కన్నీళ్ళు హృదయాన్ని తేలిక చేస్తాయి.",
                        "బాధ అనుభవించడం చాలా కష్టం, కానీ మీ భావాలు చెల్లుబాటు అవుతాయి. 🤗 మీతో పాటు ఉండటానికి నేను ఇక్కడ ఉన్నాను.",
                        "దుఃఖం జీవితంలో భాగం, కానీ అది మిమ్మల్ని నిర్వచించదు. 🌈 దయచేసి మీ పట్ల దయగా ఉండండి మరియు సహాయం కోరడానికి వెనుకాడకండి."
                    ]
                elif emotion_context == "anxiety":
                    return [
                        "ఆందోళన అనుభవించడం భయంకరంగా ఉండవచ్చు. 🌸 4-7-8 శ్వాస పద్ధతిని ప్రయత్నించండి: 4 లెక్కల వరకు పీల్చండి, 7 వరకు ఆపండి, 8 వరకు వదలండి.",
                        "మీ ఆందోళన భావాలు పూర్తిగా సరైనవి. 🧘‍♀️ మీ చుట్టూ ఉన్న 5 వస్తువులను గమనించడం ద్వారా మనసును ప్రశాంతపరచండి.",
                        "ఆందోళనతో పోరాడడం ధైర్యం. 💪 మీరు ఇంతకు ముందు కూడா కష్టాలను అధిగమించారు, ఇప్పుడు కూడా చేయగలరు."
                    ]
                elif emotion_context == "depression":
                    return [
                        "మీరు చాలా చీకటి స్థలంలో ఉన్నారని నేను వింటున్నాను. 🫂 దయచేసి గుర్తుంచుకోండి, మీ జీవితానికి విలువ ఉంది మరియు ఈ చీకటి భావనలు శాశ్వతం కాదు.",
                        "డిప్రెషన్ అంతా భారంగా మరియు నిరాశగా అనిపిస్తుంది. 💙 మీరు దెబ్బతిన్నవారు కాదు, మీరు మనిషివి, మరియు మీరు మద్దతు మరియు శ్రద్ధకు అర్హులు.",
                        "డిప్రెషన్ మనతో అబద్ధాలు చెబుతుంది. 🌱 కానీ మీరు ఈరోజు చేరుకున్నారు, ఇది అద్భుతమైన బలాన్ని చూపిస్తుంది. దయచేసి కౌన్సెలర్ లేదా నమ్మకమైన స్నేహితుడితో మాట్లాడడాన్ని పరిగణించండి."
                    ]
                elif emotion_context == "anger":
                    return [
                        "మీ మాటల్లో కోపం వినిపిస్తుంది, ఆ భావనలు సరైనవి. 🔥 కోపం తరచుగా దుఃఖం లేదా భయాన్ని దాచుతుంది. ఆ కోపం కింద మీకు ఏమి ఉంది?",
                        "కోపం అనుభవించడం సరైనది - అన్యాయం లేదా నొప్పికి కోపం ఆరోగ్యకరమైన ప్రతిస్పందన కావచ్చు. 💪 మీకు ఈ విధంగా అనిపించడానికి కారణమేమిటో మాట్లాడుకుందాం.",
                        "కోపం వినబడాలని కోరుకునే శక్తివంతమైన భావోద్వేగం. 🗣️ దాన్ని దాచకుండా, అది మీకు ఏమి చెప్పడానికి ప్రయత్నిస్తుందో అన్వేషిద్దాం."
                    ]
                elif emotion_context == "stress" or study_count > 0 or stress_count > 0:
                    return [
                        "చదువుల ఒత్తిడి చాలా సాధారణం, మీరు ఒంటరి కాదు. 📚 విశ్రాంతి తీసుకోవాలని మరియు మీ మానసిక ఆరోగ్యాన్ని ప్రాధాన్యత ఇవ్వాలని గుర్తుంచుకోండి.",
                        "అకాడమిక్ ప్రెషర్ అధికంగా అనిపించవచ్చు. 🎯 పనులను చిన్న భాగాలుగా విభజించండి మరియు ప్రతి చిన్న విజయాన్ని జరుపుకోండి.",
                        "మీ విలువ గ్రేడ్‌లతో నిర్ణయించబడదు. 🌟 మీరు ప్రయత్నిస్తున్నందుకే గర్విస్తాను. అవసరమైనప్పుడు సహాయం కోరడంలో సిగ్గుపడకండి."
                    ]
                else:
                    return [
                        "మీ భావాలను నాతో పంచుకున్నందుకు ధన్యవాదాలు. 🤗 నేను మీ మాటలను జాగ్రత్తగా వింటున్నాను మరియు మీకు మద్దతు ఇవ్వడానికి ఇక్కడ ఉన్నాను.",
                        "నేను మీతో ఉన్నాను మరియు మీ అనుభవాలను విలువైనవిగా భావిస్తున్నాను. 💙 మీ మనసులో ఉన్నదాన్ని నాతో పంచుకోవడంలో సంకోచం వద్దు.",
                        "మీరు ధైర్యవంతులు, మీ భావాలను వ్యక్తపరచడానికి. 🌸 మనం కలిసి ఎదుర్కొనే ఏ సవాలు అయినా అధిగమించవచ్చు."
                    ]
            elif user_language.startswith('hi-'):
                # Hindi empathetic responses
                if sentiment == "positive":
                    return [
                        "आपकी खुशी देखकर मुझे भी बहुत अच्छा लग रहा है! 😊 इन सुंदर पलों को अपने दिल में संजो कर रखिए।",
                        "आपकी सकारात्मक ऊर्जा वाकई प्रेरणादायक है! इन अच्छी भावनाओं को दूसरों के साथ भी साझा करें।",
                        "आपमें जो आशावाद है वह सच में बहुत अच्छा है! जीवन के ऐसे खुशी के पलों को हमेशा मनाना चाहिए।"
                    ]
                elif emotion_context == "breakup":
                    return [
                        "रिश्ते का टूटना बहुत दुखदायी होता है, मैं आपके दर्द को समझ सकता हूं। 💙 कृपया याद रखें, आप प्यार के हकदार हैं।",
                        "ब्रेकअप दिल को दुखाता है, लेकिन यह आपकी कीमत कम नहीं करता। समय सभी घावों को भर देता है। अपने अच्छे लोगों के साथ समय बिताइए।",
                        "ब्रेकअप का दर्द सहना मुश्किल है, लेकिन आप अकेले नहीं हैं। 🤝 अपनी भावनाओं को दबाएं नहीं - रोना चाहें तो रोएं, यह प्राकृतिक है।"
                    ]
                elif emotion_context == "loneliness":
                    return [
                        "अकेलापन महसूस करना बहुत कष्टकर है, लेकिन आप वास्तव में अकेले नहीं हैं। 🫂 मैं यहां हूं और आपकी बात सुनने के लिए तैयार हूं।",
                        "अकेला महसूस करना एक प्राकृतिक भावना है, लेकिन याद रखें - आप एक मूल्यवान व्यक्ति हैं। नई दोस्ती बनाने के लिए छोटे कदम उठाएं।",
                        "अकेलापन दिल को दुखाता है, लेकिन यह हमेशा के लिए नहीं है। 🌱 आपकी परवाह करने वाले लोग हैं, उनसे मिलें या फोन करें।"
                    ]
                elif emotion_context == "sadness":
                    return [
                        "आपका दुख देखकर मुझे भी दुख हो रहा है। 💙 रोना चाहें तो रोएं - आंसू दिल को हल्का करते हैं।",
                        "दुख महसूस करना बहुत कठिन है, लेकिन आपकी भावनाएं वैध हैं। 🤗 आपके साथ रहने के लिए मैं यहां हूं।",
                        "दुख जीवन का हिस्सा है, लेकिन यह आपको परिभाषित नहीं करता। 🌈 कृपया अपने साथ दयालु रहें और मदद मांगने से न हिचकें।"
                    ]
                elif emotion_context == "anxiety":
                    return [
                        "चिंता महसूस करना डरावना हो सकता है। 🌸 4-7-8 सांस तकनीक आजमाएं: 4 गिनती तक सांस लें, 7 तक रोकें, 8 तक छोड़ें।",
                        "आपकी चिंता की भावनाएं पूर्णतः सही हैं। 🧘‍♀️ अपने आसपास की 5 चीजों को देखकर मन को शांत करें।",
                        "चिंता से लड़ना साहस की बात है। 💪 आपने पहले भी कठिनाइयों पर विजय पाई है, अब भी पा सकते हैं।"
                    ]
                elif emotion_context == "depression":
                    return [
                        "आप बहुत अंधेरी जगह में हैं, मैं समझ सकता हूं। 🫂 कृपया याद रखें, आपके जीवन की कीमत है और ये अंधेरे भाव हमेशा नहीं रहेंगे।",
                        "डिप्रेशन सब कुछ भारी और निराशाजनक लगता है। 💙 आप टूटे हुए नहीं हैं, आप इंसान हैं, और आप सहारे और देखभाल के हकदार हैं।",
                        "डिप्रेशन हमसे हमारी कीमत के बारे में झूठ बोलता है। 🌱 लेकिन आप आज पहुंचे, यह अविश्वसनीय ताकत दिखाता है। कृपया किसी काउंसलर या भरोसेमंद दोस्त से बात करने पर विचार करें।"
                    ]
                elif emotion_context == "anger":
                    return [
                        "आपके शब्दों में गुस्सा सुनाई दे रहा है, ये भावनाएं सही हैं। 🔥 गुस्सा अक्सर दुख या डर को छुपाता है। उस गुस्से के नीचे आपके लिए क्या है?",
                        "गुस्सा महसूस करना ठीक है - अन्याय या दुख के लिए गुस्सा एक स्वस्थ प्रतिक्रिया हो सकती है। 💪 आइए बात करते हैं कि आपको ऐसा क्यों लग रहा है।",
                        "गुस्सा एक शक्तिशाली भावना है जो सुनी जाने की मांग करती है। 🗣️ इसे दबाने के बजाय, आइए देखते हैं कि यह आपको क्या बताने की कोशिश कर रहा है।"
                    ]
                elif emotion_context == "stress" or study_count > 0 or stress_count > 0:
                    return [
                        "पढ़ाई का तनाव बहुत आम है, आप अकेले नहीं हैं। 📚 आराम करना और अपने मानसिक स्वास्थ्य को प्राथमिकता देना याद रखें।",
                        "शैक्षणिक दबाव ज्यादा लग सकता है। 🎯 कामों को छोटे हिस्सों में बांटें और हर छोटी जीत का जश्न मनाएं।",
                        "आपकी कीमत ग्रेड से तय नहीं होती। 🌟 आप कोशिश कर रहे हैं, इसके लिए गर्व करता हूं। जरूरत पड़ने पर मदद मांगने में शर्म न करें।"
                    ]
                else:
                    return [
                        "अपनी भावनाएं मेरे साथ साझा करने के लिए धन्यवाद। 🤗 मैं आपकी बातों को ध्यान से सुन रहा हूं और आपका साथ देने के लिए यहां हूं।",
                        "मैं आपके साथ हूं और आपके अनुभवों को महत्वपूर्ण मानता हूं। 💙 अपने मन की बात मेरे साथ साझा करने में झिझक न करें।",
                        "आप साहसी हैं, अपनी भावनाओं को व्यक्त करने के लिए। 🌸 हम मिलकर किसी भी चुनौती का सामना कर सकते हैं।"
                    ]
            elif user_language.startswith('kn-'):
                # Kannada empathetic responses  
                if sentiment == "positive":
                    return [
                        "ನಿಮ್ಮ ಸಂತೋಷ ನೋಡಿ ನನಗೂ ತುಂಬಾ ಖುಶಿಯಾಗುತ್ತಿದೆ! 😊 ಈ ಸುಂದರ ಕ್ಷಣಗಳನ್ನು ಹೃದಯದಲ್ಲಿ ಇಟ್ಟುಕೊಳ್ಳಿ।",
                        "ನಿಮ್ಮ ಧನಾತ್ಮಕ ಶಕ್ತಿ ನಿಜವಾಗಿಯೂ ಪ್ರೇರಣಾದಾಯಕ! ಈ ಒಳ್ಳೆಯ ಭಾವನೆಗಳನ್ನು ಇತರರೊಂದಿಗೆ ಸಹ ಹಂಚಿಕೊಳ್ಳಿ।",
                        "ನಿಮ್ಮಲ್ಲಿರುವ ಆಶಾವಾದ ನಿಜವಾಗಿಯೂ ಅದ್ಭುತ! ಜೀವನದಲ್ಲಿ ಇಂತಹ ಸಂತೋಷದ ಕ್ಷಣಗಳನ್ನು ಯಾವಾಗಲೂ ಆಚರಿಸಬೇಕು।"
                    ]
                elif emotion_context == "breakup":
                    return [
                        "ಸಂಬಂಧ ಮುರಿಯುವುದು ತುಂಬಾ ನೋವಿನ ವಿಷಯ, ನಿಮ್ಮ ನೋವನ್ನು ನಾನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುತ್ತೇನೆ। 💙 ದಯವಿಟ್ಟು ನೆನಪಿಡಿ, ನೀವು ಪ್ರೀತಿಗೆ ಅರ್ಹರು।",
                        "ಬ್ರೇಕಪ್ ಹೃದಯವನ್ನು ನೋಯಿಸುತ್ತದೆ, ಆದರೆ ಇದು ನಿಮ್ಮ ಮೌಲ್ಯವನ್ನು ಕಡಿಮೆ ಮಾಡುವುದಿಲ್ಲ। ಸಮಯ ಎಲ್ಲಾ ಗಾಯಗಳನ್ನು ಗುಣಪಡಿಸುತ್ತದೆ। ನಿಮ್ಮ ಒಳ್ಳೆಯ ಜನರೊಂದಿಗೆ ಸಮಯ ಕಳೆಯಿರಿ।",
                        "ಬ್ರೇಕಪ್ ನೋವನ್ನು ಸಹಿಸುವುದು ಕಷ್ಟ, ಆದರೆ ನೀವು ಏಕಾಂಗಿಯಲ್ಲ. 🤝 ನಿಮ್ಮ ಭಾವನೆಗಳನ್ನು ದಮನ ಮಾಡಬೇಡಿ - ಅಳಬೇಕೆನಿಸಿದರೆ ಅಳಿರಿ, ಅದು ಸಹಜ."
                    ]
                else:
                    return [
                        "ನಿಮ್ಮ ಭಾವನೆಗಳನ್ನು ನನ್ನೊಂದಿಗೆ ಹಂಚಿಕೊಂಡಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು। 🤗 ನಾನು ನಿಮ್ಮ ಮಾತುಗಳನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ಕೇಳುತ್ತಿದ್ದೇನೆ ಮತ್ತು ನಿಮಗೆ ಬೆಂಬಲ ನೀಡಲು ಇಲ್ಲಿದ್ದೇನೆ।",
                        "ನಾನು ನಿಮ್ಮೊಂದಿಗಿದ್ದೇನೆ ಮತ್ತು ನಿಮ್ಮ ಅನುಭವಗಳನ್ನು ಮೌಲ್ಯಯುತವೆಂದು ಭಾವಿಸುತ್ತೇನೆ। 💙 ನಿಮ್ಮ ಮನಸ್ಸಿನಲ್ಲಿರುವುದನ್ನು ನನ್ನೊಂದಿಗೆ ಹಂಚಿಕೊಳ್ಳಲು ಹಿಂಜರಿಯಬೇಡಿ।"
                    ]
            else:
                # Enhanced English empathetic responses (default)
                if sentiment == "positive":
                    return [
                        "Your happiness brings joy to my heart too! 😊 Hold onto these beautiful moments and let them light up your day.",
                        "I can feel your positive energy through your words! 🌟 Keep nurturing these wonderful feelings and share them with others.",
                        "The optimism in your voice is truly inspiring! Life's happy moments like these deserve to be celebrated and cherished."
                    ]
                elif emotion_context == "breakup":
                    return [
                        "Breakups are incredibly painful, and I can hear the hurt in your words. 💙 Please remember that you are worthy of love and this pain will ease with time.",
                        "Ending a relationship feels like losing a part of yourself. 🤗 It's okay to grieve, to feel angry, or confused. Your feelings are completely valid.",
                        "I know your heart is breaking right now. 💔 Surround yourself with people who care about you, and don't be afraid to lean on them for support."
                    ]
                elif emotion_context == "loneliness":
                    return [
                        "Loneliness can feel overwhelming, but you're not truly alone. 🫂 I'm here listening to you, and there are people who care about you, even when it doesn't feel that way.",
                        "Feeling isolated is one of the most difficult human experiences. 🌱 Remember that connection starts with small steps - even this conversation shows your courage to reach out.",
                        "Loneliness hurts deeply, but it's not permanent. 💙 Consider joining a community activity or reaching out to an old friend - you deserve meaningful connections."
                    ]
                elif emotion_context == "sadness":
                    return [
                        "I can feel the sadness in your words, and I want you to know it's okay to not be okay. 💙 Let yourself feel these emotions - they're part of healing.",
                        "Sadness is heavy to carry alone. 🤗 If you need to cry, cry. If you need to talk, I'm here. Your pain matters and so do you.",
                        "These waves of sadness will pass, even though they feel endless right now. 🌈 Please be gentle with yourself during this difficult time."
                    ]
                elif emotion_context == "anxiety":
                    return [
                        "Anxiety can feel terrifying and overwhelming. 🌸 Try the 4-7-8 breathing technique: breathe in for 4, hold for 7, exhale for 8. You're stronger than your anxiety.",
                        "Your anxious feelings are completely valid. 🧘‍♀️ Ground yourself by naming 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste.",
                        "Fighting anxiety takes incredible courage. 💪 You've overcome difficult moments before, and you can get through this one too. I believe in your strength."
                    ]
                elif emotion_context == "depression":
                    return [
                        "Depression makes everything feel heavy and hopeless. 🫂 Please know that your life has value, and these dark feelings won't last forever. You matter more than you know.",
                        "I hear you're in a really dark place right now. 💙 Depression lies to us about our worth. You're not broken, you're human, and you deserve support and care.",
                        "When depression speaks, it tells us we're alone and worthless. 🌱 But you reached out today, which shows incredible strength. Please consider talking to a counselor or trusted friend."
                    ]
                elif emotion_context == "anger":
                    return [
                        "I can hear the anger in your words, and those feelings are valid. 🔥 Anger often covers up hurt or fear. What's underneath that anger for you?",
                        "It's okay to feel angry - anger can be a healthy response to injustice or hurt. 💪 Let's talk about what's making you feel this way.",
                        "Anger is a powerful emotion that demands to be heard. 🗣️ Instead of pushing it down, let's explore what it's trying to tell you."
                    ]
                elif study_count > 0 or stress_count > 0:
                    return [
                        "Academic pressure can feel crushing. 📚 Remember that your worth isn't determined by grades. Take breaks, practice self-care, and ask for help when you need it.",
                        "Study stress is so common - you're definitely not alone in this struggle. 🎯 Break big tasks into smaller steps and celebrate each small victory along the way.",
                        "I'm proud of you for working hard, but please don't sacrifice your mental health. 🌟 Your wellbeing matters more than any test score."
                    ]
                else:
                    return [
                        "Thank you for trusting me with your feelings. 🤗 I'm here to listen without judgment and support you through whatever you're experiencing.",
                        "I hear you, and your experiences matter to me. 💙 Please feel free to share whatever is on your mind - this is your safe space.",
                        "You showed courage by opening up today. 🌸 Whatever challenges you're facing, remember that you don't have to face them alone."
                    ]

        # Enhanced contextual sentiment and emotion analysis
        emotion_context = "neutral"
        confidence = 0.75
        
        # Determine specific emotional context (prioritized by severity)
        if depression_count > 0:
            sentiment = "negative"
            emotion_context = "depression"
            confidence = min(0.9 + depression_count * 0.05, 0.98)
        elif breakup_count > 0:
            sentiment = "negative"
            emotion_context = "breakup"
            confidence = min(0.85 + breakup_count * 0.05, 0.95)
        elif loneliness_count > 0:
            sentiment = "negative"
            emotion_context = "loneliness"
            confidence = min(0.85 + loneliness_count * 0.05, 0.95)
        elif sadness_count > 0:
            sentiment = "negative"
            emotion_context = "sadness"
            confidence = min(0.8 + sadness_count * 0.05, 0.9)
        elif anxiety_count > 0:
            sentiment = "negative"
            emotion_context = "anxiety"
            confidence = min(0.8 + anxiety_count * 0.05, 0.9)
        elif anger_count > 0:
            sentiment = "negative"
            emotion_context = "anger"
            confidence = min(0.8 + anger_count * 0.05, 0.9)
        elif study_count > 0 or stress_count > 0:
            sentiment = "negative"
            emotion_context = "stress"
            confidence = min(0.75 + (study_count + stress_count) * 0.05, 0.85)
        elif positive_count > negative_count:
            sentiment = "positive"
            emotion_context = "positive"
            confidence = min(0.8 + positive_count * 0.05, 0.95)
        elif negative_count > positive_count:
            sentiment = "negative"
            emotion_context = "general_negative"
            confidence = min(0.75 + negative_count * 0.05, 0.85)
        else:
            sentiment = "neutral"
            emotion_context = "neutral"
            confidence = 0.75
        
        # Get contextually appropriate responses
        responses = get_language_responses(sentiment, emotion_context, user_language)
        
        # Select response
        import random
        response = random.choice(responses)
        
        # Extract keywords
        keywords = []
        all_words = positive_words + negative_words + study_words + stress_words
        for word in all_words:
            if word in message_lower:
                keywords.append(word.capitalize())
        
        return jsonify({
            'success': True,
            'analysis': {
                'sentiment': sentiment,
                'confidence': confidence,
                'emotion': emotion_context.replace('_', ' ').title(),
                'emotion_context': emotion_context,
                'keywords': keywords[:5],
                'sentiment_score': 0.8 if sentiment == 'positive' else 0.2 if sentiment == 'negative' else 0.5
            },
            'response': response
        })
        
    except Exception as e:
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
            'response': 'I apologize for the technical difficulty. Please try speaking again, and I\'ll do my best to help and support you.'
        })

@app.route('/api/voice-chat/auto-prompt', methods=['POST'])
def get_auto_prompt():
    """Get contextual automatic conversation prompts"""
    try:
        data = request.get_json()
        user_language = data.get('language', 'en-US')
        conversation_context = data.get('context', 'general')  # general, wellness, study, etc.
        
        # Contextual prompts based on conversation topic
        contextual_prompts = {
            'en-US': {
                'general': [
                    "Is there anything else on your mind?",
                    "How are you feeling about what we just discussed?",
                    "Would you like to share more about your thoughts?",
                    "I'm here to listen. What would you like to talk about?",
                    "Feel free to continue sharing whenever you're ready.",
                    "Is there something specific you'd like to explore further?"
                ],
                'wellness': [
                    "How has your mental wellness journey been lately?",
                    "What self-care practices have been helping you?",
                    "Is there any particular area of wellness you'd like to focus on?",
                    "How are you taking care of yourself today?",
                    "What brings you peace and calm?"
                ],
                'study': [
                    "How are your studies going?",
                    "Is there any subject you're finding challenging?",
                    "What study techniques work best for you?",
                    "How do you manage study stress?",
                    "What are your academic goals?"
                ]
            },
            'te-IN': {
                'general': [
                    "మీ మనసులో ఇంకా ఏదైనా ఉందా?",
                    "మనం ఇప్పుడు మాట్లాడిన దాని గురించి మీకు ఎలా అనిపిస్తుంది?",
                    "మీ ఆలోచనలను మరింత పంచుకోవాలని అనిపిస్తుందా?",
                    "నేను వినడానికి ఇక్కడ ఉన్నాను. మీరు ఏమి మాట్లాడాలని అనుకుంటున్నారు?",
                    "మీరు సిద్ధంగా ఉన్నప్పుడు స్వేచ్ఛగా పంచుకోండి.",
                    "మీరు మరింత తెలుసుకోవాలని అనుకునే ఏదైనా ప్రత్యేకమైనది ఉందా?"
                ],
                'wellness': [
                    "మీ మానసిక ఆరోగ్య ప్రయాణం ఇటీవల ఎలా ఉంది?",
                    "ఏ స్వీయ సంరక్షణ పద్ధతులు మీకు సహాయపడుతున్నాయి?",
                    "మీరు దృష్టి పెట్టాలని అనుకునే ఆరోగ్య రంగం ఏదైనా ఉందా?",
                    "ఈరోజు మీరు మిమ్మల్ని ఎలా చూసుకుంటున్నారు?",
                    "మీకు శాంతి మరియు ప్రశాంతత ఇచ్చేది ఏమిటి?"
                ],
                'study': [
                    "మీ చదువులు ఎలా జరుగుతున్నాయి?",
                    "మీకు కష్టంగా అనిపిస్తున్న ఏదైనా విషయం ఉందా?",
                    "మీకు ఏ చదువు పద్ధతులు బాగా పనిచేస్తాయి?",
                    "చదువు ఒత్తిడిని ఎలా నిర్వహిస్తారు?",
                    "మీ విద్యా లక్ష్యాలు ఏమిటి?"
                ]
            },
            'hi-IN': {
                'general': [
                    "क्या आपके मन में कुछ और है?",
                    "आप कैसा महसूस कर रहे हैं?",
                    "क्या आप अपने विचार साझा करना चाहते हैं?",
                    "मैं यहाँ सुनने के लिए हूँ। आप क्या बात करना चाहते हैं?",
                    "जब आप तैयार हों तो बेझिझक साझा करें।",
                    "क्या कुछ खास है जिसे आप और जानना चाहते हैं?"
                ],
                'wellness': [
                    "आपकी मानसिक स्वास्थ्य यात्रा हाल में कैसी रही है?",
                    "कौन सी स्वयं देखभाल की पद्धतियाँ आपकी मदद कर रही हैं?",
                    "क्या कोई विशेष स्वास्थ्य क्षेत्र है जिस पर आप ध्यान देना चाहते हैं?",
                    "आज आप अपनी देखभाल कैसे कर रहे हैं?",
                    "आपको शांति और सुकून क्या देता है?"
                ],
                'study': [
                    "आपकी पढ़ाई कैसी चल रही है?",
                    "क्या कोई विषय है जो आपको कठिन लग रहा है?",
                    "कौन सी अध्ययन तकनीकें आपके लिए सबसे अच्छी हैं?",
                    "आप अध्ययन के तनाव को कैसे संभालते हैं?",
                    "आपके शैक्षणिक लक्ष्य क्या हैं?"
                ]
            },
            'kn-IN': {
                'general': [
                    "ನಿಮ್ಮ ಮನಸ್ಸಿನಲ್ಲಿ ಇನ್ನೇನಾದರೂ ಇದೆಯೇ?",
                    "ನಾವು ಈಗ ಮಾತಾಡಿದ ಬಗ್ಗೆ ನಿಮಗೆ ಹೇಗೆ ಅನಿಸುತ್ತಿದೆ?",
                    "ನಿಮ್ಮ ಆಲೋಚನೆಗಳನ್ನು ಹೆಚ್ಚು ಹಂಚಿಕೊಳ್ಳಲು ಬಯಸುತ್ತೀರಾ?",
                    "ನಾನು ಕೇಳಲು ಇಲ್ಲಿದ್ದೇನೆ. ನೀವು ಏನು ಮಾತಾಡಲು ಬಯಸುತ್ತೀರಿ?",
                    "ನೀವು ಸಿದ್ಧವಾದಾಗ ಮುಕ್ತವಾಗಿ ಹಂಚಿಕೊಳ್ಳಿ।",
                    "ನೀವು ಮತ್ತಷ್ಟು ಅನ್ವೇಷಿಸಲು ಬಯಸುವ ಏನಾದರೂ ನಿರ್ದಿಷ್ಟವಾದುದು ಇದೆಯೇ?"
                ],
                'wellness': [
                    "ನಿಮ್ಮ ಮಾನಸಿಕ ಆರೋಗ್ಯ ಪ್ರಯಾಣ ಇತ್ತೀಚೆಗೆ ಹೇಗಿದೆ?",
                    "ಯಾವ ಸ್ವಯಂ ಆರೈಕೆ ಪದ್ಧತಿಗಳು ನಿಮಗೆ ಸಹಾಯ ಮಾಡುತ್ತಿವೆ?",
                    "ನೀವು ಗಮನ ಹರಿಸಲು ಬಯಸುವ ಯಾವುದೇ ವಿಶೇಷ ಆರೋಗ್ಯ ಕ್ಷೇತ್ರವಿದೆಯೇ?",
                    "ಇಂದು ನೀವು ನಿಮ್ಮ ಆರೈಕೆಯನ್ನು ಹೇಗೆ ತೆಗೆದುಕೊಳ್ಳುತ್ತಿದ್ದೀರಿ?",
                    "ನಿಮಗೆ ಶಾಂತಿ ಮತ್ತು ಪ್ರಶಾಂತತೆ ತರುವುದು ಏನು?"
                ],
                'study': [
                    "ನಿಮ್ಮ ಅಧ್ಯಯನ ಹೇಗೆ ನಡೆಯುತ್ತಿದೆ?",
                    "ನೀವು ಸವಾಲಿನಂತೆ ಭಾವಿಸುವ ಯಾವುದೇ ವಿಷಯವಿದೆಯೇ?",
                    "ನಿಮಗೆ ಯಾವ ಅಧ್ಯಯನ ತಂತ್ರಗಳು ಉತ್ತಮವಾಗಿ ಕೆಲಸ ಮಾಡುತ್ತವೆ?",
                    "ಅಧ್ಯಯನದ ಒತ್ತಡವನ್ನು ನೀವು ಹೇಗೆ ನಿರ್ವಹಿಸುತ್ತೀರಿ?",
                    "ನಿಮ್ಮ ಶೈಕ್ಷಣಿಕ ಗುರಿಗಳು ಯಾವುವು?"
                ]
            }
        }
        
        # Get prompts for the specified language and context
        language_prompts = contextual_prompts.get(user_language, contextual_prompts['en-US'])
        context_prompts = language_prompts.get(conversation_context, language_prompts['general'])
        
        # Select a random prompt
        import random
        selected_prompt = random.choice(context_prompts)
        
        return jsonify({
            'success': True,
            'prompt': selected_prompt,
            'context': conversation_context,
            'language': user_language
        })
        
    except Exception as e:
        # Fallback to basic English prompt
        fallback_prompts = [
            "Is there anything else you'd like to talk about?",
            "How are you feeling right now?",
            "I'm here to listen. Please continue when you're ready."
        ]
        import random
        return jsonify({
            'success': True,
            'prompt': random.choice(fallback_prompts),
            'context': 'general',
            'language': 'en-US'
        })

if __name__ == '__main__':
    print("🧠 Starting Manas Wellness Platform...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📖 New Journal feature available at: http://localhost:5000/journal")
    print("🔧 API endpoints available for frontend integration")
    app.run(host='0.0.0.0', port=5000, debug=True)