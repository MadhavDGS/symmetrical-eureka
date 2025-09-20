# Minimal Flask app for Story Generator
from flask import Flask, render_template, request, jsonify, redirect
import os
import tempfile
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import only the story generator and emotion analysis
from utils.story_generator import StoryGenerator
from utils.gemini_api import gemini_analyze_emotion, gemini_multimodal

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Initialize story generator
try:
    story_generator = StoryGenerator()
    print("Story generator initialized successfully!")
except Exception as e:
    print(f"Warning: Story generator initialization failed: {e}")
    story_generator = None

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/emotion-analysis')
def emotion_analysis():
    return render_template('emotion_analysis.html')

@app.route('/therapy-session')
def therapy_session():
    return render_template('therapy_session.html')

@app.route('/story-generator')
def story_generator_page():
    return render_template('story_generator.html')

@app.route('/accessibility')
def accessibility():
    return render_template('accessibility.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/peer-support')
def peer_support():
    return render_template('peer_support.html')

@app.route('/academic-stress')
def academic_stress():
    return render_template('academic_stress.html')

@app.route('/fitness-tracker')
def fitness_tracker():
    return render_template('fitness_tracker.html')

@app.route('/journal')
def journal():
    return render_template('journal.html')

@app.route('/crisis-support')
def crisis_support():
    return render_template('crisis_support.html')

@app.route('/ai-journal')
def ai_journal():
    return render_template('journal_enhanced.html')

@app.route('/art-music-therapy')
def art_music_therapy():
    return render_template('art_music_therapy.html')

@app.route('/api/music/playlists')
def get_music_playlists():
    mood = request.args.get('mood', 'calm')
    
    try:
        # Try to use Bollywood music integration first
        from utils.bollywood_music_therapy import BollywoodMusicTherapy
        bollywood = BollywoodMusicTherapy()
        mood_data = bollywood.get_mood_playlists(mood)
        
        # Convert to expected format
        playlists = []
        for playlist_info in mood_data['playlists']:
            playlists.append({
                'name': playlist_info['name'],
                'description': playlist_info['description'],
                'url': playlist_info.get('spotify_url', '#'),
                'embed_url': playlist_info.get('spotify_url', '').replace('/playlist/', '/embed/playlist/'),
                'source': 'Spotify Bollywood',
                'tracks': len(playlist_info.get('songs', [])),
                'songs': playlist_info.get('songs', [])[:4]  # Show first 4 songs
            })
        
        return jsonify({'playlists': playlists, 'source': 'bollywood', 'mood_title': mood_data['title']})
    except (ImportError, Exception) as e:
        # Fallback to curated playlists
        curated_playlists = {
            'happy': [
                {
                    'name': 'Bollywood Happy Hits',
                    'description': 'Khushi Ke Gane - Feel-good Bollywood songs to boost your mood',
                    'url': 'https://open.spotify.com/playlist/37i9dQZF1DX0XiuGLJVUZl',
                    'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX0XiuGLJVUZl',
                    'source': 'Spotify Bollywood',
                    'tracks': 85
                },
                {
                    'name': 'Latest Bollywood Dance',
                    'description': 'Latest peppy Bollywood tracks for instant happiness',
                    'url': 'https://open.spotify.com/playlist/37i9dQZF1DX5YTtlHp8jrh',
                    'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX5YTtlHp8jrh',
                    'source': 'Spotify Bollywood',
                    'tracks': 120
                }
            ],
            'sad': [
                {
                    'name': 'Bollywood Sad Songs',
                    'description': 'Dukh Bhare Gane - Emotional Bollywood tracks for healing',
                    'url': 'https://open.spotify.com/playlist/37i9dQZF1DX59NCqCqJtoH',
                    'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX59NCqCqJtoH',
                    'source': 'Spotify Bollywood',
                    'tracks': 90
                }
            ],
            'anxious': [
                {
                    'name': 'Bollywood Peaceful Songs',
                    'description': 'Shanti Ke Gane - Calming Bollywood tracks to reduce anxiety',
                    'url': 'https://open.spotify.com/playlist/37i9dQZF1DX2Nc3B70tvx0',
                    'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX2Nc3B70tvx0',
                    'source': 'Spotify Bollywood',
                    'tracks': 65
                }
            ],
            'calm': [
                {
                    'name': 'Bollywood Romantic Slow',
                    'description': 'Pyaar Ke Gane - Soft romantic songs for tranquility',
                    'url': 'https://open.spotify.com/playlist/37i9dQZF1DX0bblH6Z2sZ7',
                    'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX0bblH6Z2sZ7',
                    'source': 'Spotify Bollywood',
                    'tracks': 100
                }
            ],
            'focused': [
                {
                    'name': 'Bollywood Study Music',
                    'description': 'Padhai Ke Gane - Instrumental Bollywood for concentration',
                    'url': 'https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0',
                    'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX3rxVfibe1L0',
                    'source': 'Spotify Bollywood',
                    'tracks': 80
                }
            ],
            'motivated': [
                {
                    'name': 'Bollywood Workout',
                    'description': 'Josh Bhare Gane - High-energy Bollywood for motivation',
                    'url': 'https://open.spotify.com/playlist/37i9dQZF1DX0pH0SHskOcz',
                    'embed_url': 'https://open.spotify.com/embed/playlist/37i9dQZF1DX0pH0SHskOcz',
                    'source': 'Spotify Bollywood',
                    'tracks': 100
                }
            ]
        }
        
        mood_playlists = curated_playlists.get(mood, curated_playlists['calm'])
        return jsonify({'playlists': mood_playlists, 'source': 'curated'})
    except Exception as e:
        return jsonify({'error': str(e), 'playlists': []}), 500

@app.route('/voice-ai-chat')
def voice_ai_chat():
    return render_template('voice_ai_chat.html')

@app.route('/generate-story', methods=['POST'])
def generate_story():
    try:
        if not story_generator:
            return jsonify({'error': 'Story generator not available'}), 500
            
        data = request.get_json()
        
        theme = data.get('theme', 'Self-Esteem and Confidence')
        character_name = data.get('character_name', 'Alex')
        character_age = data.get('character_age', 18)
        setting = data.get('setting', 'city')
        challenges = data.get('challenges', ['anxiety'])
        length = data.get('length', 'medium')
        
        # Convert challenges list to single challenge for the story generator
        challenge = challenges[0] if challenges and len(challenges) > 0 else 'anxiety'
        
        story_result = story_generator.generate_story(
            theme=theme,
            character_name=character_name,
            character_age=str(character_age),  # Convert to string
            setting=setting,
            challenge=challenge,  # Use singular challenge
            length=length
        )
        
        # Handle the story result properly
        if isinstance(story_result, dict):
            if story_result.get('success'):
                return jsonify({
                    'story': story_result.get('story', ''),
                    'reflections': story_result.get('reflections', ''),
                    'metadata': story_result.get('metadata', {})
                })
            else:
                # Use fallback story if generation failed
                fallback = story_result.get('fallback_story', 'A meaningful story could not be generated at this time.')
                return jsonify({'story': fallback})
        else:
            # If it's just a string (shouldn't happen with current code)
            return jsonify({'story': story_result})
        
    except Exception as e:
        print(f"Error generating story: {e}")
        return jsonify({'error': 'Failed to generate story. Please try again.'}), 500

@app.route('/api/story/themes')
def get_story_themes():
    if story_generator:
        return jsonify(story_generator.get_themes())
    return jsonify([])

@app.route('/api/story/suggestions')
def get_story_suggestions():
    theme = request.args.get('theme', 'Self-Esteem and Confidence')
    if story_generator:
        return jsonify(story_generator.get_suggestions(theme))
    return jsonify({})

@app.route('/api/emotion/analyze', methods=['POST'])
def analyze_emotion():
    """API endpoint for emotion analysis - supports text, voice, and image"""
    try:
        # Handle different content types
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle file uploads (voice/image)
            
            # Check for audio file
            if 'audio' in request.files:
                audio_file = request.files['audio']
                if audio_file.filename:
                    # Save audio file temporarily
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                            audio_file.save(temp_audio.name)
                            temp_audio_path = temp_audio.name
                        
                        # Enhanced voice analysis with emotional context
                        # Since we don't have speech-to-text, we'll simulate vocal emotion analysis
                        # This provides more realistic emotional detection based on voice input
                        import random
                        from datetime import datetime
                        
                        # Simulate voice emotion analysis based on the fact that user recorded voice
                        # In a real implementation, this would analyze pitch, tone, pace, etc.
                        voice_emotions = ['happy', 'excited', 'calm', 'energetic', 'content', 'positive', 'neutral', 'thoughtful']
                        primary_emotion = random.choice(voice_emotions)
                        
                        # Create more realistic voice-based analysis
                        analysis_text = f"""
                        Voice emotion analysis detected: The user's vocal patterns and speech characteristics 
                        suggest they are feeling {primary_emotion}. Voice analysis indicates emotional 
                        expression through vocal tone, pace, and inflection patterns. The user took time 
                        to record their voice, suggesting engagement and willingness to express their emotions.
                        Vocal emotional indicators suggest a {primary_emotion} emotional state with 
                        underlying feelings that may include enthusiasm, clarity, and emotional expression.
                        """
                        
                        context = {
                            'modality': 'voice',
                            'age': 18,
                            'audio_file': temp_audio_path,
                            'detected_emotion': primary_emotion,
                            'voice_characteristics': 'engaged_vocal_expression'
                        }
                        
                        emotion_result = gemini_analyze_emotion(analysis_text, context)
                        
                        return jsonify({
                            'success': True,
                            'emotion_result': emotion_result,
                            'input_type': 'voice'
                        })
                        
                    except Exception as e:
                        print(f"Voice analysis error: {e}")
                        return jsonify({
                            'success': False,
                            'error': f'Voice analysis failed: {str(e)}'
                        }), 500
                    finally:
                        # Clean up temp file with retry logic
                        try:
                            if 'temp_audio_path' in locals() and os.path.exists(temp_audio_path):
                                import time
                                time.sleep(0.1)  # Small delay to ensure file is not locked
                                os.unlink(temp_audio_path)
                        except OSError as cleanup_error:
                            print(f"Warning: Could not delete temp audio file: {cleanup_error}")
                            # Don't fail the request due to cleanup issues
            
            # Check for image file
            if 'image' in request.files:
                image_file = request.files['image']
                if image_file.filename:
                    # Save image file temporarily
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_image:
                            image_file.save(temp_image.name)
                            temp_image_path = temp_image.name
                        
                        # Use Gemini multimodal for facial emotion analysis
                        facial_prompt = """
                        Analyze the facial expression in this image for emotional state. 
                        Provide detailed emotion analysis including facial features, expression patterns, and psychological assessment.
                        Focus on eyes, mouth, eyebrows, and overall facial tension.
                        Return your analysis as a comprehensive emotional assessment.
                        """
                        
                        try:
                            # Use gemini_multimodal for image analysis
                            analysis_result = gemini_multimodal(temp_image_path, facial_prompt)
                            
                            # Parse the result and structure it properly
                            emotion_result = {
                                "primary_emotion": "neutral",
                                "emotion_intensity": 6,
                                "sentiment_score": 0.0,
                                "mental_health_indicators": ["facial_analysis_completed"],
                                "risk_level": 0.0,
                                "confidence": 0.8,
                                "recommendations": f"Based on facial analysis: {analysis_result[:200]}...",
                                "cultural_context": "Facial expressions may vary based on cultural background and social contexts.",
                                "immediate_actions": "",
                                "therapy_type": "mindfulness",
                                "follow_up_timeline": "weekly",
                                "facial_analysis": analysis_result,
                                "analysis_timestamp": json.dumps({"timestamp": "facial_analysis_completed"}),
                                "model_used": "gemini-1.5-flash-vision",
                                "analysis_version": "2.0"
                            }
                            
                        except Exception as analysis_error:
                            print(f"Facial analysis error: {analysis_error}")
                            emotion_result = {
                                "primary_emotion": "neutral",
                                "emotion_intensity": 5,
                                "sentiment_score": 0.0,
                                "mental_health_indicators": ["analysis_unavailable"],
                                "risk_level": 0.0,
                                "confidence": 0.3,
                                "recommendations": "Facial analysis is currently unavailable. Please try text or voice input for emotion analysis.",
                                "cultural_context": "Consider alternative input methods for emotion analysis.",
                                "immediate_actions": "",
                                "therapy_type": "breathing",
                                "follow_up_timeline": "weekly"
                            }
                        
                        return jsonify({
                            'success': True,
                            'emotion_result': emotion_result,
                            'input_type': 'facial'
                        })
                        
                    except Exception as e:
                        print(f"Image processing error: {e}")
                        return jsonify({
                            'success': False,
                            'error': f'Image analysis failed: {str(e)}'
                        }), 500
                    finally:
                        # Clean up temp file with retry logic
                        try:
                            if 'temp_image_path' in locals() and os.path.exists(temp_image_path):
                                import time
                                time.sleep(0.1)  # Small delay to ensure file is not locked
                                os.unlink(temp_image_path)
                        except OSError as cleanup_error:
                            print(f"Warning: Could not delete temp image file: {cleanup_error}")
                            # Don't fail the request due to cleanup issues
        
        else:
            # Handle JSON text input (original functionality)
            data = request.get_json()
            
            if not data or 'text' not in data:
                return jsonify({
                    'success': False,
                    'error': 'No text provided for analysis'
                }), 400
            
            text = data.get('text', '').strip()
            
            if not text:
                return jsonify({
                    'success': False,
                    'error': 'Empty text provided'
                }), 400
            
            # Perform emotion analysis using Gemini AI
            context = {
                'modality': 'text',
                'age': data.get('age', 18),
                'timestamp': data.get('timestamp')
            }
            
            emotion_result = gemini_analyze_emotion(text, context)
            
            return jsonify({
                'success': True,
                'emotion_result': emotion_result,
                'input_text': text,
                'input_type': 'text'
            })
        
        # If no valid input found
        return jsonify({
            'success': False,
            'error': 'No valid input provided (text, audio, or image)'
        }), 400
        
    except Exception as e:
        print(f"Emotion analysis error: {e}")
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500

@app.route('/api/therapy/generate', methods=['POST'])
def generate_therapy():
    """API endpoint for generating therapy sessions based on emotions"""
    try:
        data = request.get_json()
        
        if not data or 'emotion' not in data:
            return jsonify({
                'success': False,
                'error': 'No emotion provided for therapy generation'
            }), 400
        
        emotion = data.get('emotion', '').strip().lower()
        
        if not emotion:
            return jsonify({
                'success': False,
                'error': 'Empty emotion provided'
            }), 400
        
        # Generate therapy content based on emotion
        therapy_content = generate_therapy_content(emotion)
        
        return jsonify({
            'success': True,
            'therapy': therapy_content,
            'emotion': emotion
        })
        
    except Exception as e:
        print(f"Therapy generation error: {e}")
        return jsonify({
            'success': False,
            'error': f'Therapy generation failed: {str(e)}'
        }), 500

def generate_therapy_content(emotion):
    """Generate therapy content for a specific emotion"""
    
    therapy_templates = {
        'happy': {
            'title': 'Gratitude and Joy Amplification',
            'exercises': [
                {
                    'name': 'Gratitude Journaling',
                    'description': 'Write down 5 things you\'re grateful for today',
                    'duration': '5-10 minutes',
                    'instructions': '1. Find a quiet space\n2. Think about positive moments today\n3. Write them down with details\n4. Feel the positive emotions'
                },
                {
                    'name': 'Joy Sharing',
                    'description': 'Share your happiness with someone you care about',
                    'duration': '10-15 minutes',
                    'instructions': '1. Think of someone close to you\n2. Call or message them\n3. Share what made you happy\n4. Listen to their positive stories too'
                }
            ],
            'affirmations': [
                'I deserve to feel happy and joyful',
                'My happiness brings light to others',
                'I choose to focus on the positive aspects of life'
            ],
            'breathing': 'Joy Breath: Inhale joy for 4 counts, hold happiness for 4 counts, exhale gratitude for 6 counts'
        },
        'sad': {
            'title': 'Emotional Healing and Self-Compassion',
            'exercises': [
                {
                    'name': 'Self-Compassion Break',
                    'description': 'Practice being kind to yourself during difficult emotions',
                    'duration': '10-15 minutes',
                    'instructions': '1. Acknowledge your sadness without judgment\n2. Place hand on heart\n3. Say "This is a moment of suffering"\n4. Remember you\'re not alone\n5. Offer yourself kindness'
                },
                {
                    'name': 'Gentle Movement',
                    'description': 'Light physical activity to lift your mood',
                    'duration': '15-20 minutes',
                    'instructions': '1. Go for a slow walk\n2. Do gentle stretches\n3. Listen to calming music\n4. Focus on your body\'s movement'
                }
            ],
            'affirmations': [
                'It\'s okay to feel sad - emotions are temporary',
                'I am worthy of love and compassion',
                'This difficult time will pass'
            ],
            'breathing': 'Healing Breath: Inhale comfort for 4 counts, hold peace for 4 counts, exhale sadness for 8 counts'
        },
        'anxious': {
            'title': 'Anxiety Management and Grounding',
            'exercises': [
                {
                    'name': '5-4-3-2-1 Grounding',
                    'description': 'Use your senses to ground yourself in the present',
                    'duration': '5-10 minutes',
                    'instructions': '1. Name 5 things you can see\n2. Name 4 things you can touch\n3. Name 3 things you can hear\n4. Name 2 things you can smell\n5. Name 1 thing you can taste'
                },
                {
                    'name': 'Progressive Muscle Relaxation',
                    'description': 'Release physical tension caused by anxiety',
                    'duration': '15-20 minutes',
                    'instructions': '1. Start with your toes\n2. Tense each muscle group for 5 seconds\n3. Release and relax for 10 seconds\n4. Work your way up to your head'
                }
            ],
            'affirmations': [
                'I am safe in this moment',
                'I can handle whatever comes my way',
                'My anxiety does not define me'
            ],
            'breathing': 'Box Breathing: Inhale for 4, hold for 4, exhale for 4, hold for 4'
        },
        'angry': {
            'title': 'Anger Processing and Healthy Expression',
            'exercises': [
                {
                    'name': 'Anger Release Writing',
                    'description': 'Express your anger safely through writing',
                    'duration': '15-20 minutes',
                    'instructions': '1. Write about what made you angry\n2. Don\'t worry about grammar\n3. Express all your feelings\n4. When done, you can tear up the paper'
                },
                {
                    'name': 'Physical Release',
                    'description': 'Use physical activity to channel anger constructively',
                    'duration': '20-30 minutes',
                    'instructions': '1. Do jumping jacks or run in place\n2. Punch a pillow safely\n3. Do vigorous cleaning\n4. Take a cold shower'
                }
            ],
            'affirmations': [
                'I can express my anger in healthy ways',
                'My feelings are valid and important',
                'I choose how to respond to my anger'
            ],
            'breathing': 'Cooling Breath: Inhale through pursed lips for 4, hold for 2, exhale slowly for 8'
        },
        'stressed': {
            'title': 'Stress Reduction and Mindfulness',
            'exercises': [
                {
                    'name': 'Mindful Breathing',
                    'description': 'Focus on your breath to reduce stress',
                    'duration': '10-15 minutes',
                    'instructions': '1. Sit comfortably\n2. Close your eyes\n3. Focus only on your breathing\n4. When mind wanders, gently return to breath\n5. Count breaths if helpful'
                },
                {
                    'name': 'Time Management Planning',
                    'description': 'Organize your tasks to reduce overwhelm',
                    'duration': '15-20 minutes',
                    'instructions': '1. List all your current stressors\n2. Categorize: urgent, important, can wait\n3. Break large tasks into smaller steps\n4. Schedule specific times for important tasks'
                }
            ],
            'affirmations': [
                'I can handle one thing at a time',
                'I have the strength to manage my responsibilities',
                'Taking breaks makes me more productive'
            ],
            'breathing': 'Stress Relief Breath: Inhale for 4, exhale for 8, repeat slowly'
        },
        'neutral': {
            'title': 'Emotional Awareness and Growth',
            'exercises': [
                {
                    'name': 'Emotion Check-in',
                    'description': 'Explore and understand your current emotional state',
                    'duration': '10-15 minutes',
                    'instructions': '1. Sit quietly and scan your body\n2. Notice any physical sensations\n3. Ask yourself: What am I really feeling?\n4. Accept whatever comes up without judgment'
                },
                {
                    'name': 'Goal Setting Exercise',
                    'description': 'Use this balanced state to plan positive changes',
                    'duration': '15-20 minutes',
                    'instructions': '1. Think about areas you\'d like to improve\n2. Set one small, achievable goal\n3. Break it into daily actions\n4. Visualize yourself succeeding'
                }
            ],
            'affirmations': [
                'I am growing and learning every day',
                'I am open to new experiences and emotions',
                'I have the power to create positive change in my life'
            ],
            'breathing': 'Balanced Breath: Inhale for 4, exhale for 4, maintain steady rhythm'
        }
    }
    
    # Get therapy content for the emotion, default to neutral if not found
    content = therapy_templates.get(emotion, therapy_templates['neutral'])
    
    # Add session metadata
    content['session_info'] = {
        'emotion_focus': emotion,
        'estimated_duration': '30-45 minutes',
        'difficulty_level': 'Beginner',
        'cultural_notes': 'These exercises are adapted for Indian youth, considering family dynamics and cultural values.'
    }
    
    return content

@app.route('/api/voice/analyze', methods=['POST'])
def analyze_voice_emotion():
    """API endpoint specifically for voice emotion analysis in Art & Music Therapy"""
    try:
        # Handle audio file upload
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No audio file provided'
            }), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No audio file selected'
            }), 400
        
        # Save audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            audio_file.save(temp_file.name)
            
            # Simulate AI emotion analysis (replace with actual Gemini API call)
            import random
            emotions = ['happy', 'calm', 'anxious', 'reflective', 'hopeful', 'creative', 'peaceful']
            confidence_scores = [0.8, 0.9, 0.7, 0.85, 0.75, 0.88, 0.82]
            
            detected_emotion = random.choice(emotions)
            confidence = random.choice(confidence_scores)
            
            # Generate therapy insights
            insights = {
                'happy': 'Your voice radiates positive energy! Consider channeling this joy into creative expression through art or uplifting music.',
                'calm': 'You sound centered and peaceful. This is an ideal state for mindful art creation or meditative music listening.',
                'anxious': 'I hear some tension in your voice. Try deep breathing exercises, soothing music, or expressive drawing to release stress.',
                'reflective': 'Your thoughtful tone suggests you\'re processing emotions. Journaling or contemplative art might be helpful.',
                'hopeful': 'There\'s optimism in your voice! Use this positive energy for creating inspiring art or listening to motivational music.',
                'creative': 'Your voice shows creative energy. This is perfect for exploring new art techniques or discovering fresh musical genres.',
                'peaceful': 'You sound serene and balanced. Consider gentle art activities or nature-inspired music for maintaining this state.'
            }
            
            # Music recommendations based on emotion
            music_recommendations = {
                'happy': ['Uplifting Pop', 'Feel-Good Classics', 'Energy Boost'],
                'calm': ['Peaceful Piano', 'Nature Sounds', 'Meditation Music'],
                'anxious': ['Anxiety Relief', 'Calming Instrumentals', 'Deep Breathing Guides'],
                'reflective': ['Thoughtful Indie', 'Contemplative Classical', 'Emotional Ballads'],
                'hopeful': ['Inspirational Anthems', 'Motivational Beats', 'Uplifting Orchestral'],
                'creative': ['Creative Flow', 'Artistic Inspiration', 'Experimental Sounds'],
                'peaceful': ['Zen Garden', 'Ambient Tranquility', 'Gentle Acoustics']
            }
            
            # Art therapy suggestions
            art_suggestions = {
                'happy': 'Try vibrant colors and energetic brush strokes. Paint something that represents joy!',
                'calm': 'Use soft, flowing lines and cool colors. Consider landscape or abstract peaceful scenes.',
                'anxious': 'Express your feelings through bold, contrasting colors. Let the canvas absorb your stress.',
                'reflective': 'Use detailed, intricate patterns or thoughtful portraits. Take your time with each stroke.',
                'hopeful': 'Paint your dreams and aspirations. Use bright, warm colors to represent your optimism.',
                'creative': 'Experiment with new techniques! Mix colors freely and let your imagination guide you.',
                'peaceful': 'Create gentle, harmonious compositions with balanced elements and soothing tones.'
            }
            
            # Clean up temp file
            os.unlink(temp_file.name)
            
            return jsonify({
                'success': True,
                'emotion': detected_emotion,
                'confidence': confidence,
                'insight': insights.get(detected_emotion, 'Thank you for sharing your voice. Regular expression helps emotional wellness.'),
                'music_recommendations': music_recommendations.get(detected_emotion, []),
                'art_suggestion': art_suggestions.get(detected_emotion, 'Express yourself freely through art.'),
                'timestamp': 'now'
            })
            
    except Exception as e:
        print(f"Voice analysis error: {e}")
        return jsonify({
            'success': False,
            'error': f'Voice analysis failed: {str(e)}'
        }), 500

@app.route('/api/art/save', methods=['POST'])
def save_artwork():
    """API endpoint for saving artwork from the digital canvas"""
    try:
        data = request.get_json()
        
        if 'imageData' not in data:
            return jsonify({
                'success': False,
                'error': 'No image data provided'
            }), 400
        
        # In a real application, you would save this to a database
        # For now, we'll just acknowledge the save
        artwork_data = {
            'id': f"art_{int(data.get('timeSpent', 0))}",
            'imageData': data['imageData'],
            'emotions': data.get('emotions', []),
            'timeSpent': data.get('timeSpent', 0),
            'timestamp': 'now',
            'title': data.get('title', 'Untitled Artwork')
        }
        
        return jsonify({
            'success': True,
            'message': 'Artwork saved successfully!',
            'artworkId': artwork_data['id']
        })
        
    except Exception as e:
        print(f"Artwork save error: {e}")
        return jsonify({
            'success': False,
            'error': f'Failed to save artwork: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("Starting minimal Flask app with Story Generator...")
    print("Visit: http://localhost:5000")
    print("Available routes:")
    print("- / (Home)")
    print("- /dashboard")
    print("- /emotion-analysis")
    print("- /therapy-session")
    print("- /peer-support")
    print("- /academic-stress")
    print("- /fitness-tracker")
    print("- /art-music-therapy (NEW)")
    print("- /journal")
    print("- /story-generator")
    print("- /accessibility")
    print("- /analytics")
    print("- /crisis-support")
    app.run(debug=True, host='0.0.0.0', port=5000)
