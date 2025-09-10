# 🧠 Manas: Accessibility Engine
# Eye tracking, gesture recognition, and adaptive interface system

import cv2
import numpy as np
import mediapipe as mp
import logging
from typing import Dict, List, Optional, Any, Tuple
import json

# Configure logging
logger = logging.getLogger(__name__)

class AccessibilityEngine:
    """Comprehensive accessibility engine for inclusive mental wellness platform"""
    
    def __init__(self):
        """Initialize accessibility components"""
        # MediaPipe setup
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_hands = mp.solutions.hands
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Eye tracking setup
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Hand tracking setup
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Pose tracking setup
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Eye tracking landmarks (MediaPipe face mesh indices)
        self.eye_landmarks = {
            'left_eye': [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246],
            'right_eye': [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398],
            'left_iris': [468, 469, 470, 471, 472],
            'right_iris': [473, 474, 475, 476, 477]
        }
        
        # UI element mapping for eye tracking
        self.ui_elements = {
            'top_left': {'bounds': (0, 0, 0.3, 0.3), 'action': 'menu'},
            'top_center': {'bounds': (0.3, 0, 0.7, 0.3), 'action': 'title'},
            'top_right': {'bounds': (0.7, 0, 1.0, 0.3), 'action': 'settings'},
            'center_left': {'bounds': (0, 0.3, 0.3, 0.7), 'action': 'navigation'},
            'center': {'bounds': (0.3, 0.3, 0.7, 0.7), 'action': 'main_content'},
            'center_right': {'bounds': (0.7, 0.3, 1.0, 0.7), 'action': 'sidebar'},
            'bottom_left': {'bounds': (0, 0.7, 0.3, 1.0), 'action': 'back'},
            'bottom_center': {'bounds': (0.3, 0.7, 0.7, 1.0), 'action': 'controls'},
            'bottom_right': {'bounds': (0.7, 0.7, 1.0, 1.0), 'action': 'next'}
        }
        
        # Gesture recognition patterns
        self.gesture_patterns = {
            'thumbs_up': 'positive_feedback',
            'thumbs_down': 'negative_feedback',
            'peace_sign': 'calm_request',
            'open_palm': 'stop_pause',
            'pointing': 'selection',
            'fist': 'stress_indicator'
        }
        
        # Accessibility preferences
        self.accessibility_features = {
            'eye_tracking': True,
            'gesture_control': True,
            'voice_navigation': True,
            'high_contrast': False,
            'large_text': False,
            'audio_descriptions': False,
            'vibration_feedback': False,
            'simplified_interface': False
        }
        
        logger.info("AccessibilityEngine initialized successfully")
    
    def process_eye_tracking(self, frame_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process eye tracking data for navigation
        
        Args:
            frame_data: Dictionary containing frame and metadata
        
        Returns:
            Eye tracking navigation result
        """
        try:
            if 'frame' not in frame_data:
                return {'success': False, 'error': 'No frame data provided'}
            
            frame = frame_data['frame']
            if isinstance(frame, str):
                # If frame is base64 encoded
                import base64
                frame_bytes = base64.b64decode(frame)
                frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
                frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.face_mesh.process(rgb_frame)
            
            if not results.multi_face_landmarks:
                return {
                    'success': False,
                    'error': 'No face detected',
                    'gaze_point': None,
                    'ui_element': None
                }
            
            # Extract eye landmarks
            face_landmarks = results.multi_face_landmarks[0]
            landmarks_array = np.array([[lm.x, lm.y, lm.z] for lm in face_landmarks.landmark])
            
            # Calculate gaze direction
            gaze_point = self._calculate_gaze_point(landmarks_array, frame.shape)
            
            # Map to UI element
            ui_element = self._map_gaze_to_ui_element(gaze_point)
            
            # Calculate dwell time (would need frame history in production)
            dwell_time = frame_data.get('dwell_time', 0)
            
            # Determine if action should be triggered
            action_triggered = dwell_time > 1.5  # 1.5 seconds dwell time
            
            return {
                'success': True,
                'gaze_point': gaze_point,
                'ui_element': ui_element,
                'action_triggered': action_triggered,
                'dwell_time': dwell_time,
                'confidence': self._calculate_gaze_confidence(landmarks_array)
            }
            
        except Exception as e:
            logger.error(f"Eye tracking processing error: {e}")
            return {
                'success': False,
                'error': str(e),
                'gaze_point': None,
                'ui_element': None
            }
    
    def process_gesture(self, frame_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process hand gesture recognition
        
        Args:
            frame_data: Dictionary containing frame and metadata
        
        Returns:
            Gesture recognition result
        """
        try:
            if 'frame' not in frame_data:
                return {'success': False, 'error': 'No frame data provided'}
            
            frame = frame_data['frame']
            if isinstance(frame, str):
                # If frame is base64 encoded
                import base64
                frame_bytes = base64.b64decode(frame)
                frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
                frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
            
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = self.hands.process(rgb_frame)
            
            if not results.multi_hand_landmarks:
                return {
                    'success': False,
                    'error': 'No hands detected',
                    'gesture': None,
                    'action': None
                }
            
            # Analyze hand landmarks
            gestures_detected = []
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks_array = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
                gesture = self._recognize_gesture(landmarks_array)
                if gesture:
                    gestures_detected.append(gesture)
            
            # Get primary gesture and corresponding action
            primary_gesture = gestures_detected[0] if gestures_detected else None
            action = self.gesture_patterns.get(primary_gesture, 'unknown') if primary_gesture else None
            
            return {
                'success': True,
                'gesture': primary_gesture,
                'action': action,
                'all_gestures': gestures_detected,
                'confidence': 0.8 if primary_gesture else 0.0
            }
            
        except Exception as e:
            logger.error(f"Gesture processing error: {e}")
            return {
                'success': False,
                'error': str(e),
                'gesture': None,
                'action': None
            }
    
    def adapt_interface(self, user_preferences: Dict[str, Any], current_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adapt interface based on user accessibility needs and current context
        
        Args:
            user_preferences: User accessibility preferences
            current_context: Current application context
        
        Returns:
            Interface adaptation recommendations
        """
        try:
            adaptations = {
                'visual': {},
                'audio': {},
                'interaction': {},
                'content': {}
            }
            
            # Visual adaptations
            if user_preferences.get('visual_impairment'):
                adaptations['visual'].update({
                    'high_contrast': True,
                    'large_text': True,
                    'font_size_multiplier': 1.5,
                    'color_scheme': 'high_contrast',
                    'reduce_animations': True,
                    'focus_indicators': 'enhanced'
                })
            
            if user_preferences.get('color_blindness'):
                adaptations['visual'].update({
                    'color_scheme': 'colorblind_friendly',
                    'use_patterns': True,
                    'avoid_color_only_info': True
                })
            
            # Audio adaptations
            if user_preferences.get('hearing_impairment'):
                adaptations['audio'].update({
                    'visual_alerts': True,
                    'vibration_feedback': True,
                    'captions_enabled': True,
                    'sign_language_support': True
                })
            
            # Interaction adaptations
            if user_preferences.get('motor_impairment'):
                adaptations['interaction'].update({
                    'eye_tracking_enabled': True,
                    'voice_control_enabled': True,
                    'larger_touch_targets': True,
                    'gesture_alternatives': True,
                    'dwell_time_adjustment': True
                })
            
            # Cognitive adaptations
            if user_preferences.get('cognitive_support_needed'):
                adaptations['content'].update({
                    'simplified_language': True,
                    'step_by_step_guidance': True,
                    'visual_aids': True,
                    'progress_indicators': True,
                    'reduced_cognitive_load': True
                })
            
            # Context-based adaptations
            emotional_state = current_context.get('emotional_state', {})
            if emotional_state.get('primary_emotion') in ['anxious', 'overwhelmed']:
                adaptations['content'].update({
                    'calming_colors': True,
                    'reduced_stimulation': True,
                    'breathing_reminders': True
                })
            
            return {
                'success': True,
                'adaptations': adaptations,
                'priority_features': self._prioritize_adaptations(adaptations, user_preferences)
            }
            
        except Exception as e:
            logger.error(f"Interface adaptation error: {e}")
            return {
                'success': False,
                'error': str(e),
                'adaptations': {}
            }
    
    def generate_audio_description(self, content_data: Dict[str, Any]) -> str:
        """
        Generate audio descriptions for visual content
        
        Args:
            content_data: Visual content data
        
        Returns:
            Audio description text
        """
        try:
            descriptions = []
            
            # Describe UI elements
            if 'ui_elements' in content_data:
                for element in content_data['ui_elements']:
                    desc = f"{element['type']} located at {element['position']}"
                    if element.get('text'):
                        desc += f" with text '{element['text']}'"
                    descriptions.append(desc)
            
            # Describe images
            if 'images' in content_data:
                for image in content_data['images']:
                    desc = f"Image showing {image.get('description', 'visual content')}"
                    descriptions.append(desc)
            
            # Describe current state
            if 'current_state' in content_data:
                state = content_data['current_state']
                descriptions.append(f"Current page: {state.get('page_title', 'Unknown')}")
                if state.get('active_element'):
                    descriptions.append(f"Focus on: {state['active_element']}")
            
            return ". ".join(descriptions) + "."
            
        except Exception as e:
            logger.error(f"Audio description generation error: {e}")
            return "Audio description unavailable."
    
    def process_sign_language(self, frame_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process sign language recognition (basic implementation)
        
        Args:
            frame_data: Video frame data
        
        Returns:
            Sign language recognition result
        """
        try:
            # This is a simplified implementation
            # In production, you'd use specialized sign language recognition models
            
            gesture_result = self.process_gesture(frame_data)
            
            if not gesture_result['success']:
                return gesture_result
            
            # Map gestures to basic sign language meanings
            sign_mappings = {
                'thumbs_up': 'good/yes',
                'thumbs_down': 'bad/no',
                'peace_sign': 'peace/calm',
                'open_palm': 'stop/wait',
                'pointing': 'that/there',
                'fist': 'strong/emphasis'
            }
            
            gesture = gesture_result.get('gesture')
            sign_meaning = sign_mappings.get(gesture, 'unknown_sign')
            
            return {
                'success': True,
                'gesture': gesture,
                'sign_meaning': sign_meaning,
                'confidence': gesture_result.get('confidence', 0.0)
            }
            
        except Exception as e:
            logger.error(f"Sign language processing error: {e}")
            return {
                'success': False,
                'error': str(e),
                'sign_meaning': None
            }
    
    def _calculate_gaze_point(self, landmarks: np.ndarray, frame_shape: Tuple[int, int, int]) -> Tuple[float, float]:
        """Calculate gaze point from eye landmarks"""
        try:
            # Get iris landmarks (simplified approach)
            left_iris_center = np.mean(landmarks[self.eye_landmarks['left_iris']], axis=0)
            right_iris_center = np.mean(landmarks[self.eye_landmarks['right_iris']], axis=0)
            
            # Average iris positions
            iris_center = (left_iris_center + right_iris_center) / 2
            
            # Convert to screen coordinates (normalized 0-1)
            gaze_x = iris_center[0]
            gaze_y = iris_center[1]
            
            return (gaze_x, gaze_y)
            
        except Exception as e:
            logger.error(f"Gaze point calculation error: {e}")
            return (0.5, 0.5)  # Center of screen as fallback
    
    def _map_gaze_to_ui_element(self, gaze_point: Tuple[float, float]) -> Optional[str]:
        """Map gaze point to UI element"""
        try:
            gaze_x, gaze_y = gaze_point
            
            for element_name, element_data in self.ui_elements.items():
                bounds = element_data['bounds']
                if (bounds[0] <= gaze_x <= bounds[2] and 
                    bounds[1] <= gaze_y <= bounds[3]):
                    return element_data['action']
            
            return None
            
        except Exception as e:
            logger.error(f"Gaze to UI mapping error: {e}")
            return None
    
    def _calculate_gaze_confidence(self, landmarks: np.ndarray) -> float:
        """Calculate confidence in gaze detection"""
        try:
            # Simple confidence based on eye openness and landmark quality
            left_eye_landmarks = landmarks[self.eye_landmarks['left_eye']]
            right_eye_landmarks = landmarks[self.eye_landmarks['right_eye']]
            
            # Calculate eye openness
            left_eye_height = np.max(left_eye_landmarks[:, 1]) - np.min(left_eye_landmarks[:, 1])
            right_eye_height = np.max(right_eye_landmarks[:, 1]) - np.min(right_eye_landmarks[:, 1])
            
            # Average eye openness as confidence indicator
            avg_openness = (left_eye_height + right_eye_height) / 2
            
            # Normalize to 0-1 range (this is simplified)
            confidence = min(avg_openness * 10, 1.0)
            
            return confidence
            
        except Exception as e:
            logger.error(f"Gaze confidence calculation error: {e}")
            return 0.5
    
    def _recognize_gesture(self, landmarks: np.ndarray) -> Optional[str]:
        """Recognize hand gesture from landmarks"""
        try:
            # Simplified gesture recognition
            # In production, you'd use trained models or more sophisticated algorithms
            
            # Get key landmark positions
            thumb_tip = landmarks[4]
            thumb_ip = landmarks[3]
            index_tip = landmarks[8]
            index_pip = landmarks[6]
            middle_tip = landmarks[12]
            middle_pip = landmarks[10]
            ring_tip = landmarks[16]
            ring_pip = landmarks[14]
            pinky_tip = landmarks[20]
            pinky_pip = landmarks[18]
            
            # Check for thumbs up
            if (thumb_tip[1] < thumb_ip[1] and  # Thumb extended up
                index_tip[1] > index_pip[1] and  # Other fingers down
                middle_tip[1] > middle_pip[1] and
                ring_tip[1] > ring_pip[1] and
                pinky_tip[1] > pinky_pip[1]):
                return 'thumbs_up'
            
            # Check for peace sign
            if (index_tip[1] < index_pip[1] and  # Index extended
                middle_tip[1] < middle_pip[1] and  # Middle extended
                ring_tip[1] > ring_pip[1] and  # Ring down
                pinky_tip[1] > pinky_pip[1]):  # Pinky down
                return 'peace_sign'
            
            # Check for open palm
            if (index_tip[1] < index_pip[1] and
                middle_tip[1] < middle_pip[1] and
                ring_tip[1] < ring_pip[1] and
                pinky_tip[1] < pinky_pip[1]):
                return 'open_palm'
            
            # Check for fist
            if (index_tip[1] > index_pip[1] and
                middle_tip[1] > middle_pip[1] and
                ring_tip[1] > ring_pip[1] and
                pinky_tip[1] > pinky_pip[1]):
                return 'fist'
            
            return None
            
        except Exception as e:
            logger.error(f"Gesture recognition error: {e}")
            return None
    
    def _prioritize_adaptations(self, adaptations: Dict[str, Any], user_preferences: Dict[str, Any]) -> List[str]:
        """Prioritize adaptations based on user needs"""
        try:
            priorities = []
            
            # High priority adaptations
            if user_preferences.get('visual_impairment'):
                priorities.extend(['high_contrast', 'large_text', 'audio_descriptions'])
            
            if user_preferences.get('hearing_impairment'):
                priorities.extend(['visual_alerts', 'captions_enabled', 'vibration_feedback'])
            
            if user_preferences.get('motor_impairment'):
                priorities.extend(['eye_tracking_enabled', 'voice_control_enabled'])
            
            # Medium priority adaptations
            if user_preferences.get('cognitive_support_needed'):
                priorities.extend(['simplified_language', 'step_by_step_guidance'])
            
            return priorities[:5]  # Return top 5 priorities
            
        except Exception as e:
            logger.error(f"Adaptation prioritization error: {e}")
            return []