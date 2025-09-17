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
    except Exception as e:
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

if __name__ == '__main__':
    print("🧠 Starting Manas Wellness Platform...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📖 New Journal feature available at: http://localhost:5000/journal")
    print("🔧 API endpoints available for frontend integration")
    app.run(host='0.0.0.0', port=5000, debug=True)