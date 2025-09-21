"""
Google Cloud Services Integration for Enhanced AI Features
"""

import os
import logging
from google.cloud import speech
from google.cloud import texttospeech
from google.cloud import translate_v2 as translate
from google.cloud import vision
import io

class GoogleCloudServices:
    def __init__(self):
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
        self.credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        
        # Initialize clients only if credentials are available
        self.speech_client = None
        self.tts_client = None
        self.translate_client = None
        self.vision_client = None
        
        if self.credentials_path and os.path.exists(self.credentials_path):
            try:
                self._initialize_clients()
                logging.info("Google Cloud services initialized successfully")
            except Exception as e:
                logging.error(f"Google Cloud initialization failed: {e}")
        else:
            logging.warning("Google Cloud credentials not found, using fallbacks")
    
    def _initialize_clients(self):
        """Initialize Google Cloud service clients"""
        try:
            self.speech_client = speech.SpeechClient()
            self.tts_client = texttospeech.TextToSpeechClient()
            self.translate_client = translate.Client()
            self.vision_client = vision.ImageAnnotatorClient()
        except Exception as e:
            logging.error(f"Client initialization error: {e}")
    
    def transcribe_audio(self, audio_file_path, language_code='en-US'):
        """Convert speech to text for voice journaling"""
        if not self.speech_client:
            return self._fallback_transcription(audio_file_path)
        
        try:
            with io.open(audio_file_path, 'rb') as audio_file:
                content = audio_file.read()
            
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=language_code,
                enable_automatic_punctuation=True,
                enable_emotion_recognition=True
            )
            
            response = self.speech_client.recognize(config=config, audio=audio)
            
            transcriptions = []
            for result in response.results:
                transcriptions.append({
                    'text': result.alternatives[0].transcript,
                    'confidence': result.alternatives[0].confidence
                })
            
            return {
                'transcriptions': transcriptions,
                'language_detected': language_code,
                'source': 'google_speech'
            }
            
        except Exception as e:
            logging.error(f"Speech transcription error: {e}")
            return self._fallback_transcription(audio_file_path)
    
    def synthesize_speech(self, text, language_code='en-US', voice_gender='NEUTRAL'):
        """Convert text to speech for accessibility"""
        if not self.tts_client:
            return self._fallback_speech_synthesis(text)
        
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                ssml_gender=getattr(texttospeech.SsmlVoiceGender, voice_gender)
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            return {
                'audio_content': response.audio_content,
                'format': 'mp3',
                'language': language_code,
                'source': 'google_tts'
            }
            
        except Exception as e:
            logging.error(f"Speech synthesis error: {e}")
            return self._fallback_speech_synthesis(text)
    
    def translate_text(self, text, target_language='hi', source_language='en'):
        """Translate text for multi-language support"""
        if not self.translate_client:
            return self._fallback_translation(text, target_language)
        
        try:
            result = self.translate_client.translate(
                text,
                target_language=target_language,
                source_language=source_language
            )
            
            return {
                'translated_text': result['translatedText'],
                'source_language': result.get('detectedSourceLanguage', source_language),
                'target_language': target_language,
                'confidence': 1.0,
                'source': 'google_translate'
            }
            
        except Exception as e:
            logging.error(f"Translation error: {e}")
            return self._fallback_translation(text, target_language)
    
    def analyze_facial_emotions(self, image_path):
        """Analyze facial emotions from images"""
        if not self.vision_client:
            return self._fallback_emotion_analysis()
        
        try:
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            # Detect faces and emotions
            response = self.vision_client.face_detection(image=image)
            faces = response.face_annotations
            
            if not faces:
                return {'emotions': {}, 'faces_detected': 0, 'source': 'google_vision'}
            
            # Process first face for emotion analysis
            face = faces[0]
            emotions = {
                'joy': self._likelihood_to_score(face.joy_likelihood),
                'sorrow': self._likelihood_to_score(face.sorrow_likelihood),
                'anger': self._likelihood_to_score(face.anger_likelihood),
                'surprise': self._likelihood_to_score(face.surprise_likelihood)
            }
            
            return {
                'emotions': emotions,
                'faces_detected': len(faces),
                'dominant_emotion': max(emotions, key=emotions.get),
                'confidence': max(emotions.values()),
                'source': 'google_vision'
            }
            
        except Exception as e:
            logging.error(f"Facial emotion analysis error: {e}")
            return self._fallback_emotion_analysis()
    
    def _likelihood_to_score(self, likelihood):
        """Convert Google Vision likelihood to numerical score"""
        likelihood_scores = {
            'UNKNOWN': 0.0,
            'VERY_UNLIKELY': 0.1,
            'UNLIKELY': 0.25,
            'POSSIBLE': 0.5,
            'LIKELY': 0.75,
            'VERY_LIKELY': 0.9
        }
        return likelihood_scores.get(str(likelihood), 0.0)
    
    # Fallback methods when APIs are not available
    def _fallback_transcription(self, audio_file_path):
        return {
            'transcriptions': [{'text': 'Audio transcription not available - please add Google Cloud credentials', 'confidence': 0.0}],
            'source': 'fallback'
        }
    
    def _fallback_speech_synthesis(self, text):
        return {
            'audio_content': b'',
            'format': 'mp3',
            'message': 'Speech synthesis not available - please add Google Cloud credentials',
            'source': 'fallback'
        }
    
    def _fallback_translation(self, text, target_language):
        return {
            'translated_text': text,  # Return original text
            'source_language': 'unknown',
            'target_language': target_language,
            'message': 'Translation not available - please add Google Cloud credentials',
            'source': 'fallback'
        }
    
    def _fallback_emotion_analysis(self):
        return {
            'emotions': {'joy': 0.5, 'sorrow': 0.0, 'anger': 0.0, 'surprise': 0.0},
            'faces_detected': 0,
            'message': 'Facial emotion analysis not available - please add Google Cloud credentials',
            'source': 'fallback'
        }

# Global instance
google_services = GoogleCloudServices()
