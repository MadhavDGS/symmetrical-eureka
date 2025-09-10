# 🧠 Manas: Multi-Modal Emotion Detection
# Advanced emotion analysis using computer vision, voice, and text processing

import cv2
import numpy as np
import mediapipe as mp
import librosa
import json
import logging
from typing import Dict, List, Optional, Any
from PIL import Image
import tempfile
import os
from datetime import datetime

from .gemini_api import gemini_analyze_emotion

# Configure logging
logger = logging.getLogger(__name__)

class EmotionDetector:
    """Multi-modal emotion detection system"""
    
    def __init__(self):
        """Initialize emotion detection components"""
        # MediaPipe setup for facial emotion detection
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        )
        
        # Emotion mapping for facial landmarks
        self.emotion_landmarks = {
            'happy': [61, 84, 17, 314, 405, 320, 307, 375, 321, 308],
            'sad': [1, 2, 5, 4, 6, 168, 8, 9, 10, 151],
            'angry': [70, 63, 105, 66, 107, 55, 65, 52, 53, 46],
            'surprised': [70, 63, 105, 66, 107, 55, 65, 52, 53, 46],
            'neutral': [1, 2, 5, 4, 6, 168, 8, 9, 10, 151]
        }
        
        logger.info("EmotionDetector initialized successfully")
    
    def analyze_facial_emotion(self, image_path: str) -> Dict[str, Any]:
        """
        Analyze facial emotion from image using enhanced MediaPipe and Gemini AI
        
        Args:
            image_path: Path to image file
        
        Returns:
            Dictionary containing comprehensive emotion analysis results
        """
        try:
            # Load and validate image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Could not load image")
            
            # Convert BGR to RGB for MediaPipe
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Get image dimensions for better analysis
            height, width = rgb_image.shape[:2]
            
            # Process with MediaPipe Face Mesh for detailed landmarks
            results = self.face_mesh.process(rgb_image)
            
            if not results.multi_face_landmarks:
                # Fallback: try with simpler face detection
                mp_face_detection = mp.solutions.face_detection
                face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.3)
                detection_results = face_detection.process(rgb_image)
                
                if not detection_results.detections:
                    return {
                        'primary_emotion': 'neutral',
                        'emotion_intensity': 1,
                        'confidence': 0.3,
                        'facial_landmarks_detected': False,
                        'analysis_method': 'fallback_no_face',
                        'error': 'No face detected in image',
                        'suggestions': 'Please ensure good lighting and face is clearly visible'
                    }
            
            # Extract facial landmarks if available
            landmark_analysis = {}
            if results.multi_face_landmarks:
                face_landmarks = results.multi_face_landmarks[0]
                landmarks_array = np.array([[lm.x, lm.y, lm.z] for lm in face_landmarks.landmark])
                
                # Enhanced geometric analysis
                landmark_analysis = self._enhanced_landmark_analysis(landmarks_array)
                logger.info(f"Landmark analysis: {landmark_analysis}")
            else:
                landmark_analysis = {
                    'primary_emotion': 'neutral',
                    'emotion_intensity': 3,
                    'confidence': 0.4,
                    'facial_features': {}
                }
            
            # Enhanced Gemini AI analysis with better prompting
            gemini_prompt = f"""
            You are an expert clinical psychologist specializing in facial emotion analysis for youth mental health assessment.
            
            Analyze this facial image for emotional state with extreme precision. The MediaPipe geometric analysis detected:
            {json.dumps(landmark_analysis, indent=2)}
            
            Image technical details:
            - Resolution: {width}x{height}
            - Face detected: {results.multi_face_landmarks is not None}
            - Analysis context: Mental wellness assessment for Indian youth
            
            Provide a comprehensive psychological assessment in this EXACT JSON format:
            
            {{
                "facial_emotion_detected": "primary emotion (happy, sad, anxious, angry, neutral, surprised, confused, stressed, calm, excited)",
                "emotion_intensity": integer from 1-10,
                "confidence": decimal from 0.0-1.0,
                "facial_features_analysis": {{
                    "eye_expression": "detailed description of eye area emotions and tension",
                    "mouth_expression": "detailed analysis of mouth curvature and positioning", 
                    "eyebrow_position": "eyebrow elevation, furrow patterns, stress indicators",
                    "overall_facial_tension": "assessment of facial muscle tension and asymmetry",
                    "micro_expressions": "subtle emotional indicators visible in the image"
                }},
                "emotions_breakdown": {{
                    "happy": percentage 0-100,
                    "sad": percentage 0-100,
                    "angry": percentage 0-100,
                    "surprised": percentage 0-100,
                    "neutral": percentage 0-100,
                    "anxious": percentage 0-100,
                    "confused": percentage 0-100
                }},
                "mental_wellness_indicators": ["specific indicators from facial analysis"],
                "cultural_considerations": "considerations for Indian youth emotional expression patterns",
                "recommendations": "specific therapeutic recommendations based on facial emotional state",
                "image_quality_assessment": "assessment of image clarity, lighting, angle for analysis accuracy",
                "analysis_notes": "additional observations relevant to mental wellness assessment"
            }}
            
            CRITICAL ANALYSIS FACTORS:
            1. Eye region: Look for stress lines, tear duct tension, eyelid positioning
            2. Mouth area: Smile authenticity, downturned corners, lip tension
            3. Forehead: Worry lines, eyebrow asymmetry, frown patterns
            4. Cheek area: Natural fullness vs. tension, smile lines
            5. Jaw: Clenching indicators, asymmetry
            6. Overall: Facial symmetry, natural vs. forced expressions
            
            Consider cultural context:
            - Indian youth may mask emotions due to social expectations
            - Academic pressure stress indicators
            - Family dynamics influence on emotional expression
            - Gender-specific emotional expression patterns
            
            Return ONLY the JSON object, no additional text or markdown.
            """
            
            # Get enhanced Gemini analysis
            from .gemini_api import gemini_multimodal
            try:
                gemini_response = gemini_multimodal(image_path, gemini_prompt)
                logger.info(f"Gemini facial analysis response: {gemini_response[:300]}...")
                
                # Enhanced combination of MediaPipe and Gemini results
                combined_result = self._enhanced_facial_analysis_fusion(landmark_analysis, gemini_response)
                
                # Add metadata
                combined_result.update({
                    'facial_landmarks_detected': results.multi_face_landmarks is not None,
                    'analysis_method': 'enhanced_mediapipe_gemini_fusion',
                    'image_resolution': f"{width}x{height}",
                    'processing_timestamp': datetime.now().isoformat()
                })
                
                return combined_result
                
            except Exception as gemini_error:
                logger.warning(f"Gemini facial analysis failed: {gemini_error}")
                # Return enhanced MediaPipe analysis as fallback
                landmark_analysis.update({
                    'facial_landmarks_detected': results.multi_face_landmarks is not None,
                    'analysis_method': 'enhanced_mediapipe_only',
                    'gemini_error': str(gemini_error),
                    'fallback_used': True
                })
                return landmark_analysis
            
        except Exception as e:
            logger.error(f"Enhanced facial emotion analysis error: {e}")
            return {
                'primary_emotion': 'error',
                'emotion_intensity': 0,
                'confidence': 0.0,
                'facial_landmarks_detected': False,
                'analysis_method': 'error',
                'error': str(e),
                'suggestions': 'Please try again with a clearer image in good lighting'
            }
    
    def analyze_voice_emotion(self, audio_path: str) -> Dict[str, Any]:
        """
        Analyze voice emotion from audio file
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            Dictionary containing voice emotion analysis
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=22050)
            
            # Extract audio features
            features = self._extract_audio_features(y, sr)
            
            # Basic emotion classification from audio features
            emotion_scores = self._classify_emotion_from_audio(features)
            
            # Use Gemini for enhanced analysis if we can transcribe
            try:
                # For now, we'll use the audio features for analysis
                # In production, you'd want to use Google Speech-to-Text first
                gemini_prompt = f"""
                Analyze voice emotion based on these audio characteristics:
                - Pitch variation: {features.get('pitch_variation', 0)}
                - Energy level: {features.get('energy', 0)}
                - Speaking rate: {features.get('tempo', 0)}
                - Spectral features: {features.get('spectral_centroid', 0)}
                
                Provide emotion analysis focusing on:
                - Stress indicators in voice
                - Emotional state from vocal patterns
                - Mental wellness indicators
                """
                
                gemini_analysis = gemini_analyze_emotion("Voice analysis based on audio features", {
                    'audio_features': features,
                    'modality': 'voice'
                })
                
                # Combine audio analysis with Gemini insights
                combined_result = self._combine_voice_analysis(emotion_scores, gemini_analysis, features)
                
                return combined_result
                
            except Exception as gemini_error:
                logger.warning(f"Gemini voice analysis failed: {gemini_error}")
                return emotion_scores
            
        except Exception as e:
            logger.error(f"Voice emotion analysis error: {e}")
            return {
                'primary_emotion': 'error',
                'emotion_intensity': 0,
                'confidence': 0.0,
                'audio_features_extracted': False,
                'analysis_method': 'error',
                'error': str(e)
            }
    
    def analyze_text_emotion(self, text: str) -> Dict[str, Any]:
        """
        Analyze emotion from text using Gemini AI
        
        Args:
            text: Text to analyze
        
        Returns:
            Dictionary containing text emotion analysis
        """
        try:
            # Use Gemini AI for comprehensive text emotion analysis
            emotion_result = gemini_analyze_emotion(text, {
                'modality': 'text',
                'analysis_focus': 'youth_mental_wellness'
            })
            
            # Add text-specific metadata
            emotion_result.update({
                'text_length': len(text),
                'word_count': len(text.split()),
                'analysis_method': 'gemini_ai',
                'modality': 'text'
            })
            
            return emotion_result
            
        except Exception as e:
            logger.error(f"Text emotion analysis error: {e}")
            return {
                'primary_emotion': 'error',
                'emotion_intensity': 0,
                'confidence': 0.0,
                'analysis_method': 'error',
                'modality': 'text',
                'error': str(e)
            }
    
    def fuse_multimodal_emotions(self, emotion_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Fuse multiple emotion analysis results for higher accuracy
        
        Args:
            emotion_results: List of emotion analysis results from different modalities
        
        Returns:
            Fused emotion analysis result
        """
        try:
            if not emotion_results:
                return {'primary_emotion': 'neutral', 'confidence': 0.0}
            
            # Weight different modalities
            modality_weights = {
                'text': 0.4,
                'visual': 0.35,
                'audio': 0.25
            }
            
            # Collect emotions and confidences
            emotions = []
            confidences = []
            risk_levels = []
            
            for result in emotion_results:
                if result.get('primary_emotion') != 'error':
                    modality = result.get('modality', 'unknown')
                    weight = modality_weights.get(modality, 0.33)
                    
                    emotions.append(result.get('primary_emotion', 'neutral'))
                    confidences.append(result.get('confidence', 0.0) * weight)
                    risk_levels.append(result.get('risk_level', 0.0) * weight)
            
            if not emotions:
                return {'primary_emotion': 'neutral', 'confidence': 0.0}
            
            # Find most common emotion weighted by confidence
            emotion_counts = {}
            for i, emotion in enumerate(emotions):
                if emotion not in emotion_counts:
                    emotion_counts[emotion] = 0
                emotion_counts[emotion] += confidences[i]
            
            # Get primary emotion
            primary_emotion = max(emotion_counts, key=emotion_counts.get)
            
            # Calculate fused metrics
            fused_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            fused_risk_level = sum(risk_levels) / len(risk_levels) if risk_levels else 0.0
            
            return {
                'primary_emotion': primary_emotion,
                'confidence': min(fused_confidence, 1.0),
                'risk_level': min(fused_risk_level, 1.0),
                'modalities_used': [r.get('modality', 'unknown') for r in emotion_results],
                'fusion_method': 'weighted_confidence',
                'individual_results': emotion_results
            }
            
        except Exception as e:
            logger.error(f"Multimodal fusion error: {e}")
            return {
                'primary_emotion': 'error',
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _classify_emotion_from_landmarks(self, landmarks: np.ndarray) -> Dict[str, Any]:
        """Classify emotion from facial landmarks using advanced geometric analysis"""
        try:
            # More sophisticated facial emotion analysis
            # Key landmark indices for facial features
            LEFT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
            RIGHT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
            MOUTH = [61, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318]
            EYEBROWS = [70, 63, 105, 66, 107, 55, 65, 52, 53, 46]
            
            # Calculate facial feature measurements
            # Eye aspect ratio (EAR) - measures eye openness
            left_ear = self._calculate_eye_aspect_ratio(landmarks, LEFT_EYE)
            right_ear = self._calculate_eye_aspect_ratio(landmarks, RIGHT_EYE)
            avg_ear = (left_ear + right_ear) / 2.0
            
            # Mouth aspect ratio (MAR) - measures mouth openness
            mar = self._calculate_mouth_aspect_ratio(landmarks, MOUTH)
            
            # Eyebrow elevation - measures surprise/stress
            eyebrow_elevation = self._calculate_eyebrow_elevation(landmarks, EYEBROWS)
            
            # Mouth curvature - measures smile/frown
            mouth_curvature = self._calculate_mouth_curvature(landmarks, MOUTH)
            
            # Classify emotion based on feature combinations
            emotion_scores = {
                'happy': 0,
                'sad': 0,
                'angry': 0,
                'surprised': 0,
                'neutral': 0,
                'anxious': 0
            }
            
            # Happy: wide smile, normal eye openness
            if mouth_curvature > 0.02 and mar > 0.01:
                emotion_scores['happy'] = min(80, max(50, mouth_curvature * 2000 + mar * 1000))
            
            # Sad: downturned mouth, droopy eyes
            elif mouth_curvature < -0.01 and avg_ear < 0.25:
                emotion_scores['sad'] = min(75, max(45, abs(mouth_curvature) * 1500 + (0.3 - avg_ear) * 200))
            
            # Surprised: raised eyebrows, wide eyes, open mouth
            elif eyebrow_elevation > 0.02 and avg_ear > 0.3 and mar > 0.02:
                emotion_scores['surprised'] = min(85, max(55, eyebrow_elevation * 2000 + avg_ear * 200 + mar * 800))
            
            # Angry: lowered eyebrows, tense mouth
            elif eyebrow_elevation < -0.01 and mouth_curvature < -0.005:
                emotion_scores['angry'] = min(70, max(45, abs(eyebrow_elevation) * 1500 + abs(mouth_curvature) * 1000))
            
            # Anxious: slight tension in multiple features
            elif abs(mouth_curvature) < 0.005 and avg_ear < 0.28 and eyebrow_elevation > 0.005:
                emotion_scores['anxious'] = min(65, max(40, (0.3 - avg_ear) * 150 + eyebrow_elevation * 1000))
            
            else:
                emotion_scores['neutral'] = 60
            
            # Find primary emotion
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            intensity = max(3, min(10, int(emotion_scores[primary_emotion] / 10)))
            confidence = min(0.9, max(0.4, emotion_scores[primary_emotion] / 100))
            
            return {
                'primary_emotion': primary_emotion,
                'emotion_intensity': intensity,
                'confidence': confidence,
                'facial_landmarks_detected': True,
                'analysis_method': 'mediapipe_advanced_geometric',
                'feature_measurements': {
                    'eye_aspect_ratio': avg_ear,
                    'mouth_aspect_ratio': mar,
                    'eyebrow_elevation': eyebrow_elevation,
                    'mouth_curvature': mouth_curvature
                },
                'emotion_scores': emotion_scores
            }
            
        except Exception as e:
            logger.error(f"Advanced landmark classification error: {e}")
            return {
                'primary_emotion': 'neutral',
                'emotion_intensity': 3,
                'confidence': 0.3,
                'error': str(e)
            }
    
    def _calculate_eye_aspect_ratio(self, landmarks: np.ndarray, eye_indices: List[int]) -> float:
        """Calculate eye aspect ratio for eye openness detection"""
        try:
            # Get eye landmark points
            eye_points = landmarks[eye_indices]
            
            # Vertical eye distances
            v1 = np.linalg.norm(eye_points[1] - eye_points[5])
            v2 = np.linalg.norm(eye_points[2] - eye_points[4])
            
            # Horizontal eye distance
            h = np.linalg.norm(eye_points[0] - eye_points[3])
            
            # Eye aspect ratio
            ear = (v1 + v2) / (2.0 * h) if h > 0 else 0.25
            return ear
        except:
            return 0.25  # Default value
    
    def _calculate_mouth_aspect_ratio(self, landmarks: np.ndarray, mouth_indices: List[int]) -> float:
        """Calculate mouth aspect ratio for mouth openness detection"""
        try:
            mouth_points = landmarks[mouth_indices]
            
            # Vertical mouth distances
            v1 = np.linalg.norm(mouth_points[2] - mouth_points[6])
            v2 = np.linalg.norm(mouth_points[3] - mouth_points[7])
            v3 = np.linalg.norm(mouth_points[4] - mouth_points[8])
            
            # Horizontal mouth distance
            h = np.linalg.norm(mouth_points[0] - mouth_points[6])
            
            # Mouth aspect ratio
            mar = (v1 + v2 + v3) / (3.0 * h) if h > 0 else 0.0
            return mar
        except:
            return 0.0
    
    def _calculate_eyebrow_elevation(self, landmarks: np.ndarray, eyebrow_indices: List[int]) -> float:
        """Calculate eyebrow elevation for surprise/stress detection"""
        try:
            eyebrow_points = landmarks[eyebrow_indices]
            
            # Calculate average eyebrow height relative to eye position
            eyebrow_y = np.mean(eyebrow_points[:, 1])
            eye_y = np.mean(landmarks[33:40, 1])  # Average eye height
            
            elevation = eye_y - eyebrow_y  # Higher values = raised eyebrows
            return elevation
        except:
            return 0.0
    
    def _calculate_mouth_curvature(self, landmarks: np.ndarray, mouth_indices: List[int]) -> float:
        """Calculate mouth curvature for smile/frown detection"""
        try:
            mouth_points = landmarks[mouth_indices]
            
            # Get mouth corners and center
            left_corner = mouth_points[0]
            right_corner = mouth_points[6]
            center_top = mouth_points[3]
            center_bottom = mouth_points[9] if len(mouth_points) > 9 else mouth_points[7]
            
            # Calculate mouth center
            mouth_center_y = (center_top[1] + center_bottom[1]) / 2
            corners_y = (left_corner[1] + right_corner[1]) / 2
            
            # Positive curvature = smile, negative = frown
            curvature = corners_y - mouth_center_y
            return curvature
        except:
            return 0.0
    
    def _extract_audio_features(self, y: np.ndarray, sr: int) -> Dict[str, float]:
        """Extract audio features for emotion analysis"""
        try:
            features = {}
            
            # Pitch/Fundamental frequency
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            pitch_values = pitches[magnitudes > np.percentile(magnitudes, 85)]
            features['pitch_mean'] = np.mean(pitch_values) if len(pitch_values) > 0 else 0
            features['pitch_variation'] = np.std(pitch_values) if len(pitch_values) > 0 else 0
            
            # Energy/Amplitude
            features['energy'] = np.mean(librosa.feature.rms(y=y)[0])
            
            # Spectral features
            features['spectral_centroid'] = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)[0])
            features['spectral_rolloff'] = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)[0])
            
            # Tempo
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            features['tempo'] = tempo
            
            # Zero crossing rate (speech clarity indicator)
            features['zcr'] = np.mean(librosa.feature.zero_crossing_rate(y)[0])
            
            # MFCCs (Mel-frequency cepstral coefficients)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            for i in range(13):
                features[f'mfcc_{i}'] = np.mean(mfccs[i])
            
            return features
            
        except Exception as e:
            logger.error(f"Audio feature extraction error: {e}")
            return {}
    
    def _classify_emotion_from_audio(self, features: Dict[str, float]) -> Dict[str, Any]:
        """Classify emotion from audio features"""
        try:
            # Basic rule-based classification
            # In production, you'd use trained ML models
            
            pitch_mean = features.get('pitch_mean', 0)
            pitch_variation = features.get('pitch_variation', 0)
            energy = features.get('energy', 0)
            tempo = features.get('tempo', 120)
            
            # Simple heuristics
            if energy > 0.1 and pitch_variation > 50:
                if tempo > 140:
                    emotion = 'excited'
                    intensity = 7
                else:
                    emotion = 'angry'
                    intensity = 6
            elif energy < 0.05 and pitch_mean < 150:
                emotion = 'sad'
                intensity = 5
            elif pitch_variation > 80:
                emotion = 'anxious'
                intensity = 6
            else:
                emotion = 'neutral'
                intensity = 4
            
            return {
                'primary_emotion': emotion,
                'emotion_intensity': intensity,
                'confidence': 0.5,
                'audio_features_extracted': True,
                'analysis_method': 'audio_features'
            }
            
        except Exception as e:
            logger.error(f"Audio emotion classification error: {e}")
            return {
                'primary_emotion': 'neutral',
                'emotion_intensity': 3,
                'confidence': 0.3,
                'error': str(e)
            }
    
    def _enhanced_landmark_analysis(self, landmarks: np.ndarray) -> Dict[str, Any]:
        """Enhanced geometric analysis of facial landmarks for better emotion detection"""
        try:
            # Key facial landmarks indices for MediaPipe Face Mesh
            # Eye landmarks
            left_eye_indices = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
            right_eye_indices = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
            
            # Mouth landmarks
            mouth_outer_indices = [61, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318]
            mouth_inner_indices = [13, 82, 81, 80, 78, 95, 88, 178, 87, 14, 317, 402, 318, 324]
            
            # Eyebrow landmarks
            left_eyebrow_indices = [70, 63, 105, 66, 107, 55, 65, 52, 53, 46]
            right_eyebrow_indices = [296, 334, 293, 300, 276, 283, 282, 295, 285, 336]
            
            # Calculate enhanced ratios
            left_ear = self._calculate_eye_aspect_ratio(landmarks, left_eye_indices[:6])
            right_ear = self._calculate_eye_aspect_ratio(landmarks, right_eye_indices[:6])
            avg_ear = (left_ear + right_ear) / 2
            
            mouth_ar = self._calculate_mouth_aspect_ratio(landmarks, mouth_outer_indices[:6])
            mouth_curvature = self._calculate_mouth_curvature(landmarks, mouth_outer_indices)
            
            left_eyebrow_height = self._calculate_eyebrow_elevation(landmarks, left_eyebrow_indices[:4])
            right_eyebrow_height = self._calculate_eyebrow_elevation(landmarks, right_eyebrow_indices[:4])
            avg_eyebrow_height = (left_eyebrow_height + right_eyebrow_height) / 2
            
            # Enhanced emotion classification
            emotion_scores = {
                'happy': max(0, min(100, (mouth_curvature * 60 + (1 - avg_ear) * 40))),
                'sad': max(0, min(100, ((1 - mouth_curvature) * 50 + (1 - avg_ear) * 30 + (1 - avg_eyebrow_height) * 20))),
                'surprised': max(0, min(100, (avg_ear * 40 + mouth_ar * 35 + avg_eyebrow_height * 25))),
                'angry': max(0, min(100, ((1 - avg_ear) * 35 + (1 - mouth_curvature) * 30 + avg_eyebrow_height * 35))),
                'neutral': max(0, min(100, (100 - abs(mouth_curvature - 0.5) * 80 - abs(avg_ear - 0.4) * 60))),
                'anxious': max(0, min(100, ((1 - avg_ear) * 40 + avg_eyebrow_height * 45 + mouth_ar * 15)))
            }
            
            # Determine primary emotion
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            max_score = emotion_scores[primary_emotion]
            
            # Calculate confidence based on distinctiveness
            sorted_scores = sorted(emotion_scores.values(), reverse=True)
            confidence = (sorted_scores[0] - sorted_scores[1]) / 100 if len(sorted_scores) > 1 else 0.5
            confidence = max(0.3, min(0.9, confidence))
            
            return {
                'primary_emotion': primary_emotion,
                'emotion_intensity': max(1, min(10, int(max_score / 10))),
                'confidence': confidence,
                'emotions_breakdown': emotion_scores,
                'facial_features': {
                    'eye_openness': avg_ear,
                    'mouth_openness': mouth_ar,
                    'mouth_curvature': mouth_curvature,
                    'eyebrow_elevation': avg_eyebrow_height,
                    'left_right_asymmetry': abs(left_ear - right_ear) + abs(left_eyebrow_height - right_eyebrow_height)
                },
                'geometric_analysis': {
                    'left_eye_ratio': left_ear,
                    'right_eye_ratio': right_ear,
                    'mouth_aspect_ratio': mouth_ar,
                    'eyebrow_symmetry': abs(left_eyebrow_height - right_eyebrow_height)
                }
            }
            
        except Exception as e:
            logger.error(f"Enhanced landmark analysis error: {e}")
            return {
                'primary_emotion': 'neutral',
                'emotion_intensity': 3,
                'confidence': 0.4,
                'emotions_breakdown': {'neutral': 60, 'happy': 20, 'sad': 10, 'angry': 5, 'surprised': 3, 'anxious': 2},
                'facial_features': {},
                'analysis_error': str(e)
            }
    
    def _enhanced_facial_analysis_fusion(self, mediapipe_result: Dict, gemini_analysis: str) -> Dict[str, Any]:
        """Advanced fusion of MediaPipe and Gemini facial analysis results"""
        try:
            # Start with MediaPipe result as base
            combined = mediapipe_result.copy()
            
            # Parse Gemini JSON response with better error handling
            try:
                # Clean and extract JSON from Gemini response
                import re
                json_patterns = [
                    r'```json\s*(\{.*?\})\s*```',
                    r'```\s*(\{.*?\})\s*```',
                    r'(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})'
                ]
                
                gemini_data = None
                for pattern in json_patterns:
                    match = re.search(pattern, gemini_analysis, re.DOTALL)
                    if match:
                        try:
                            json_str = match.group(1)
                            gemini_data = json.loads(json_str)
                            break
                        except json.JSONDecodeError:
                            continue
                
                if not gemini_data:
                    # Try parsing the entire response as JSON
                    gemini_data = json.loads(gemini_analysis)
                
                if gemini_data:
                    # Enhanced fusion algorithm
                    gemini_emotion = gemini_data.get('facial_emotion_detected', 'neutral')
                    gemini_confidence = float(gemini_data.get('confidence', 0.5))
                    gemini_intensity = int(gemini_data.get('emotion_intensity', 5))
                    
                    # Weighted fusion based on confidence levels
                    mediapipe_weight = 0.4 if gemini_confidence > 0.7 else 0.6
                    gemini_weight = 1.0 - mediapipe_weight
                    
                    # Combine emotion intensities
                    mp_intensity = combined.get('emotion_intensity', 5)
                    combined_intensity = int(mp_intensity * mediapipe_weight + gemini_intensity * gemini_weight)
                    
                    # Combine confidence scores
                    mp_confidence = combined.get('confidence', 0.5)
                    combined_confidence = mp_confidence * mediapipe_weight + gemini_confidence * gemini_weight
                    
                    # Choose primary emotion based on highest confidence
                    if gemini_confidence > mp_confidence:
                        combined['primary_emotion'] = gemini_emotion
                        combined['emotion_intensity'] = gemini_intensity
                    
                    # Update combined result
                    combined.update({
                        'confidence': min(0.95, combined_confidence),
                        'analysis_method': 'enhanced_mediapipe_gemini_fusion',
                        'gemini_analysis': gemini_data,
                        'fusion_weights': {
                            'mediapipe': mediapipe_weight,
                            'gemini': gemini_weight
                        }
                    })
                    
                    # Merge emotion breakdowns if available
                    if 'emotions_breakdown' in gemini_data:
                        gemini_emotions = gemini_data['emotions_breakdown']
                        mp_emotions = combined.get('emotions_breakdown', {})
                        
                        # Weighted average of emotion percentages
                        fused_emotions = {}
                        all_emotions = set(list(mp_emotions.keys()) + list(gemini_emotions.keys()))
                        
                        for emotion in all_emotions:
                            mp_score = mp_emotions.get(emotion, 0)
                            gemini_score = gemini_emotions.get(emotion, 0)
                            fused_emotions[emotion] = mp_score * mediapipe_weight + gemini_score * gemini_weight
                        
                        combined['emotions_breakdown'] = fused_emotions
                    
                    # Add Gemini-specific insights
                    for key in ['facial_features_analysis', 'mental_wellness_indicators', 
                               'cultural_considerations', 'recommendations', 'image_quality_assessment']:
                        if key in gemini_data:
                            combined[key] = gemini_data[key]
                    
                    logger.info(f"Successfully fused MediaPipe and Gemini analysis. Final emotion: {combined['primary_emotion']} (confidence: {combined['confidence']:.2f})")
                    
                else:
                    # Fallback to text-based analysis
                    logger.warning("Could not parse Gemini JSON, using text analysis")
                    combined = self._text_based_gemini_fusion(combined, gemini_analysis)
                
            except json.JSONDecodeError as je:
                logger.warning(f"Gemini JSON parsing failed: {je}")
                combined = self._text_based_gemini_fusion(combined, gemini_analysis)
            
            return combined
            
        except Exception as e:
            logger.error(f"Enhanced facial analysis fusion error: {e}")
            # Return MediaPipe result with error information
            mediapipe_result['fusion_error'] = str(e)
            mediapipe_result['analysis_method'] = 'mediapipe_only_with_fusion_error'
            return mediapipe_result
    
    def _text_based_gemini_fusion(self, base_result: Dict, gemini_text: str) -> Dict[str, Any]:
        """Fallback fusion using text analysis of Gemini response"""
        try:
            gemini_lower = gemini_text.lower()
            
            # Extract emotions mentioned in text
            emotion_mentions = {
                'happy': ['happy', 'joy', 'smile', 'positive', 'cheerful', 'pleased'],
                'sad': ['sad', 'down', 'melancholy', 'unhappy', 'depressed', 'gloomy'],
                'angry': ['angry', 'mad', 'furious', 'irritated', 'annoyed', 'hostile'],
                'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'tense', 'concerned'],
                'surprised': ['surprised', 'shocked', 'amazed', 'astonished', 'startled'],
                'neutral': ['neutral', 'calm', 'composed', 'balanced', 'stable']
            }
            
            # Count emotion mentions
            emotion_scores = {}
            for emotion, keywords in emotion_mentions.items():
                count = sum(1 for keyword in keywords if keyword in gemini_lower)
                emotion_scores[emotion] = count
            
            # Update result if strong emotion indicators found
            if sum(emotion_scores.values()) > 0:
                top_emotion = max(emotion_scores, key=emotion_scores.get)
                if emotion_scores[top_emotion] >= 2:  # Require multiple mentions
                    base_result['primary_emotion'] = top_emotion
                    base_result['confidence'] = min(base_result.get('confidence', 0.5) + 0.1, 0.8)
            
            # Adjust confidence based on descriptive language
            confidence_boosters = ['clear', 'obvious', 'evident', 'distinct', 'pronounced']
            confidence_reducers = ['subtle', 'slight', 'ambiguous', 'unclear', 'uncertain']
            
            for booster in confidence_boosters:
                if booster in gemini_lower:
                    base_result['confidence'] = min(base_result['confidence'] + 0.1, 0.9)
            
            for reducer in confidence_reducers:
                if reducer in gemini_lower:
                    base_result['confidence'] = max(base_result['confidence'] - 0.1, 0.2)
            
            base_result['analysis_method'] = 'mediapipe_with_gemini_text_fusion'
            base_result['gemini_text_analysis'] = gemini_text[:200] + "..." if len(gemini_text) > 200 else gemini_text
            
            return base_result
            
        except Exception as e:
            logger.error(f"Text-based fusion error: {e}")
            base_result['text_fusion_error'] = str(e)
            return base_result
        """Combine MediaPipe and Gemini facial analysis results with advanced fusion"""
        try:
            # Start with MediaPipe result
            combined = mediapipe_result.copy()
            
            # Try to parse Gemini JSON response
            try:
                gemini_data = json.loads(gemini_analysis)
                
                # Extract Gemini insights
                gemini_emotion = gemini_data.get('facial_emotion_detected', 'neutral')
                gemini_confidence = gemini_data.get('confidence', 0.5)
                gemini_intensity = gemini_data.get('emotion_intensity', 5)
                
                # Weighted fusion of results
                mediapipe_weight = 0.6  # MediaPipe is more reliable for geometric analysis
                gemini_weight = 0.4     # Gemini provides contextual understanding
                
                # Combine confidence scores
                combined_confidence = (
                    combined.get('confidence', 0.5) * mediapipe_weight + 
                    gemini_confidence * gemini_weight
                )
                
                # Use higher confidence emotion as primary
                if gemini_confidence > combined.get('confidence', 0.5):
                    combined['primary_emotion'] = gemini_emotion
                    combined['emotion_intensity'] = gemini_intensity
                
                # Combine analysis methods
                combined['analysis_method'] = 'mediapipe_gemini_fusion'
                combined['confidence'] = min(0.95, combined_confidence)
                
                # Add Gemini insights
                combined['gemini_analysis'] = gemini_data
                combined['facial_features_analysis'] = gemini_data.get('facial_features_analysis', {})
                combined['cultural_considerations'] = gemini_data.get('cultural_considerations', '')
                
                # Enhanced recommendations combining both analyses
                mediapipe_emotion = combined.get('primary_emotion', 'neutral')
                recommendations = gemini_data.get('recommendations', '')
                if not recommendations:
                    recommendations = self._generate_emotion_recommendations(mediapipe_emotion)
                
                combined['recommendations'] = recommendations
                
            except json.JSONDecodeError:
                # Fallback to text-based analysis if JSON parsing fails
                gemini_lower = gemini_analysis.lower()
                
                # Adjust confidence based on Gemini text analysis
                if any(word in gemini_lower for word in ['confident', 'clear', 'obvious']):
                    combined['confidence'] = min(combined['confidence'] + 0.2, 1.0)
                elif any(word in gemini_lower for word in ['uncertain', 'unclear', 'ambiguous']):
                    combined['confidence'] = max(combined['confidence'] - 0.2, 0.0)
                
                # Add text analysis
                combined['gemini_analysis'] = gemini_analysis
                combined['analysis_method'] = 'mediapipe_gemini_text_combined'
            
            return combined
            
        except Exception as e:
            logger.error(f"Facial analysis combination error: {e}")
            # Return MediaPipe result with error information
            mediapipe_result['gemini_error'] = str(e)
            mediapipe_result['analysis_method'] = 'mediapipe_only'
            return mediapipe_result
    
    def _generate_emotion_recommendations(self, emotion: str) -> str:
        """Generate therapeutic recommendations based on detected emotion"""
        recommendations_map = {
            'happy': "Great to see you're feeling positive! Continue activities that bring you joy and consider sharing your positive energy with others.",
            'sad': "It's natural to feel sad sometimes. Try talking to someone you trust, practicing mindfulness, or engaging in gentle physical activity.",
            'angry': "Anger is a valid emotion. Try deep breathing, physical exercise, or journaling to process these feelings constructively.",
            'anxious': "Anxiety can be overwhelming. Practice grounding techniques, deep breathing, or break down overwhelming tasks into smaller steps.",
            'surprised': "Unexpected emotions can be processed through reflection and discussion with trusted friends or family.",
            'neutral': "Maintaining emotional balance is positive. Continue with regular self-care and wellness activities.",
            'confused': "Feeling confused is normal. Take time to reflect, and consider talking to a mentor or counselor for clarity.",
            'stressed': "Stress management is crucial. Try relaxation techniques, time management, and ensure adequate rest.",
            'excited': "Channel your excitement into positive activities and goals that align with your values.",
            'depressed': "These feelings are serious but treatable. Please consider reaching out to a mental health professional or trusted adult."
        }
        return recommendations_map.get(emotion, "Consider self-care activities and talking to someone you trust about your feelings.")
    
    def _combine_voice_analysis(self, audio_result: Dict, gemini_result: Dict, features: Dict) -> Dict[str, Any]:
        """Combine audio analysis with Gemini insights"""
        try:
            # Start with audio result
            combined = audio_result.copy()
            
            # Incorporate Gemini analysis
            if gemini_result.get('primary_emotion') != 'error':
                # Weight the results
                audio_weight = 0.6
                gemini_weight = 0.4
                
                # Combine confidence scores
                audio_conf = combined.get('confidence', 0.0)
                gemini_conf = gemini_result.get('confidence', 0.0)
                combined['confidence'] = (audio_conf * audio_weight + gemini_conf * gemini_weight)
                
                # Use Gemini's emotion if it has higher confidence
                if gemini_conf > audio_conf:
                    combined['primary_emotion'] = gemini_result.get('primary_emotion')
                    combined['emotion_intensity'] = gemini_result.get('emotion_intensity', 5)
            
            # Add audio features for reference
            combined['audio_features'] = features
            combined['analysis_method'] = 'audio_gemini_combined'
            
            return combined
            
        except Exception as e:
            logger.error(f"Voice analysis combination error: {e}")
            return audio_result