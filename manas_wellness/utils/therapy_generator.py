# 🧠 Manas: Personalized Therapy Content Generator
# AI-powered therapy content generation for youth mental wellness

import json
import logging
import random
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from .gemini_api import generate_therapy_content, gemini_text

# Configure logging
logger = logging.getLogger(__name__)

class TherapyGenerator:
    """Personalized therapy content generator for mental wellness"""
    
    def __init__(self):
        """Initialize therapy generator with templates and configurations"""
        self.therapy_types = {
            'mindfulness': {
                'description': 'Mindfulness and meditation exercises',
                'suitable_emotions': ['anxious', 'stressed', 'overwhelmed', 'angry'],
                'duration_range': (5, 30),
                'difficulty_levels': ['easy', 'medium', 'hard']
            },
            'art': {
                'description': 'Creative art therapy activities',
                'suitable_emotions': ['sad', 'depressed', 'lonely', 'confused'],
                'duration_range': (15, 60),
                'difficulty_levels': ['easy', 'medium']
            },
            'journaling': {
                'description': 'Structured journaling and reflection',
                'suitable_emotions': ['confused', 'overwhelmed', 'sad', 'angry'],
                'duration_range': (10, 45),
                'difficulty_levels': ['easy', 'medium', 'hard']
            },
            'breathing': {
                'description': 'Breathing exercises and techniques',
                'suitable_emotions': ['anxious', 'panicked', 'stressed', 'angry'],
                'duration_range': (3, 15),
                'difficulty_levels': ['easy', 'medium']
            },
            'movement': {
                'description': 'Physical movement and exercise therapy',
                'suitable_emotions': ['depressed', 'lethargic', 'angry', 'restless'],
                'duration_range': (10, 45),
                'difficulty_levels': ['easy', 'medium', 'hard']
            },
            'cognitive': {
                'description': 'Cognitive behavioral therapy techniques',
                'suitable_emotions': ['anxious', 'depressed', 'negative', 'overwhelmed'],
                'duration_range': (15, 60),
                'difficulty_levels': ['medium', 'hard']
            },
            'social': {
                'description': 'Social connection and communication exercises',
                'suitable_emotions': ['lonely', 'isolated', 'sad', 'anxious'],
                'duration_range': (20, 90),
                'difficulty_levels': ['easy', 'medium']
            }
        }
        
        # Cultural adaptations for Indian context
        self.cultural_elements = {
            'family_values': ['respect for elders', 'family harmony', 'collective wellbeing'],
            'spiritual_practices': ['meditation', 'yoga', 'pranayama', 'mantra'],
            'festivals_celebrations': ['Diwali', 'Holi', 'Eid', 'Christmas', 'regional festivals'],
            'educational_context': ['exam stress', 'career pressure', 'competition', 'expectations'],
            'regional_languages': ['Hindi', 'Telugu', 'Tamil', 'Bengali', 'Gujarati', 'Marathi']
        }
        
        logger.info("TherapyGenerator initialized successfully")
    
    def generate_personalized_therapy(self, emotion_state: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized therapy content based on emotional state and user profile
        
        Args:
            emotion_state: Current emotional state analysis
            user_profile: User profile information
        
        Returns:
            Dictionary containing personalized therapy content
        """
        try:
            # Determine appropriate therapy type
            therapy_type = self._select_therapy_type(emotion_state, user_profile)
            
            # Generate content using Gemini AI
            therapy_content = generate_therapy_content(emotion_state, user_profile)
            
            # Enhance with cultural adaptations
            enhanced_content = self._add_cultural_adaptations(therapy_content, user_profile)
            
            # Add accessibility features
            accessible_content = self._add_accessibility_features(enhanced_content, user_profile)
            
            # Add progress tracking
            final_content = self._add_progress_tracking(accessible_content, emotion_state)
            
            return final_content
            
        except Exception as e:
            logger.error(f"Therapy generation error: {e}")
            return self._get_fallback_therapy(emotion_state, user_profile)
    
    def generate_crisis_therapy(self, risk_level: float, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate immediate crisis intervention therapy content
        
        Args:
            risk_level: Crisis risk level (0-1)
            user_context: User context and situation
        
        Returns:
            Crisis-appropriate therapy content
        """
        try:
            if risk_level >= 0.8:
                # High-risk crisis intervention
                return self._generate_high_risk_intervention(user_context)
            elif risk_level >= 0.5:
                # Moderate-risk support
                return self._generate_moderate_risk_support(user_context)
            else:
                # Preventive wellness
                return self._generate_preventive_wellness(user_context)
                
        except Exception as e:
            logger.error(f"Crisis therapy generation error: {e}")
            return self._get_emergency_fallback()
    
    def generate_follow_up_therapy(self, previous_session: Dict[str, Any], effectiveness_rating: int) -> Dict[str, Any]:
        """
        Generate follow-up therapy based on previous session effectiveness
        
        Args:
            previous_session: Previous therapy session data
            effectiveness_rating: User rating of previous session (1-10)
        
        Returns:
            Follow-up therapy content
        """
        try:
            if effectiveness_rating >= 7:
                # Previous session was effective, continue similar approach
                return self._generate_continuation_therapy(previous_session)
            elif effectiveness_rating >= 4:
                # Moderate effectiveness, adjust approach
                return self._generate_adjusted_therapy(previous_session)
            else:
                # Low effectiveness, try different approach
                return self._generate_alternative_therapy(previous_session)
                
        except Exception as e:
            logger.error(f"Follow-up therapy generation error: {e}")
            return self._get_fallback_therapy({}, {})
    
    def _select_therapy_type(self, emotion_state: Dict[str, Any], user_profile: Dict[str, Any]) -> str:
        """Select appropriate therapy type based on emotion and user profile"""
        try:
            primary_emotion = emotion_state.get('primary_emotion', 'neutral')
            emotion_intensity = emotion_state.get('emotion_intensity', 5)
            user_age = user_profile.get('age', 18)
            accessibility_needs = user_profile.get('accessibility_needs', '')
            
            # Find suitable therapy types for the emotion
            suitable_types = []
            for therapy_type, config in self.therapy_types.items():
                if primary_emotion in config['suitable_emotions']:
                    suitable_types.append(therapy_type)
            
            # If no specific match, use general approaches
            if not suitable_types:
                if emotion_intensity >= 7:
                    suitable_types = ['breathing', 'mindfulness']
                else:
                    suitable_types = ['mindfulness', 'journaling']
            
            # Consider accessibility needs
            if 'visual_impairment' in accessibility_needs:
                suitable_types = [t for t in suitable_types if t in ['breathing', 'mindfulness', 'movement']]
            elif 'hearing_impairment' in accessibility_needs:
                suitable_types = [t for t in suitable_types if t in ['art', 'journaling', 'movement']]
            
            # Consider age appropriateness
            if user_age < 16:
                suitable_types = [t for t in suitable_types if t in ['art', 'breathing', 'movement', 'mindfulness']]
            
            # Select the most appropriate type
            return suitable_types[0] if suitable_types else 'mindfulness'
            
        except Exception as e:
            logger.error(f"Therapy type selection error: {e}")
            return 'mindfulness'
    
    def _add_cultural_adaptations(self, therapy_content: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Add Indian cultural adaptations to therapy content"""
        try:
            enhanced_content = therapy_content.copy()
            
            language = user_profile.get('language', 'english')
            age = user_profile.get('age', 18)
            
            # Add cultural context
            cultural_adaptations = []
            
            # Family-oriented adaptations
            if therapy_content.get('therapy_type') in ['social', 'cognitive']:
                cultural_adaptations.append("Consider involving trusted family members if comfortable")
                cultural_adaptations.append("Respect family dynamics while prioritizing your wellbeing")
            
            # Spiritual/traditional practices
            if therapy_content.get('therapy_type') in ['mindfulness', 'breathing']:
                cultural_adaptations.append("Can be combined with traditional practices like yoga or pranayama")
                cultural_adaptations.append("Use familiar concepts like 'shanti' (peace) and 'dhyana' (meditation)")
            
            # Educational context
            if age >= 15 and age <= 25:
                cultural_adaptations.append("Acknowledge academic and career pressures common in Indian society")
                cultural_adaptations.append("Balance personal wellbeing with educational goals")
            
            # Language adaptations
            if language != 'english':
                cultural_adaptations.append(f"Practice can be done in {language} for better comfort")
                cultural_adaptations.append("Use familiar cultural metaphors and concepts")
            
            enhanced_content['cultural_adaptations'] = cultural_adaptations
            
            # Add culturally relevant examples
            if therapy_content.get('therapy_type') == 'art':
                enhanced_content['cultural_examples'] = [
                    "Draw rangoli patterns for mindfulness",
                    "Create mandala art for focus",
                    "Use traditional motifs from your region"
                ]
            elif therapy_content.get('therapy_type') == 'journaling':
                enhanced_content['cultural_prompts'] = [
                    "Write about a festival that brings you joy",
                    "Reflect on family values that support you",
                    "Describe a place in India that makes you feel peaceful"
                ]
            
            return enhanced_content
            
        except Exception as e:
            logger.error(f"Cultural adaptation error: {e}")
            return therapy_content
    
    def _add_accessibility_features(self, therapy_content: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Add accessibility features to therapy content"""
        try:
            accessible_content = therapy_content.copy()
            accessibility_needs = user_profile.get('accessibility_needs', '')
            
            accessibility_features = []
            
            # Visual impairment adaptations
            if 'visual_impairment' in accessibility_needs:
                accessibility_features.extend([
                    "Audio instructions available",
                    "Screen reader compatible",
                    "High contrast mode available",
                    "Large text options"
                ])
                
                # Modify instructions for audio delivery
                if 'instructions' in accessible_content:
                    audio_instructions = []
                    for instruction in accessible_content['instructions']:
                        audio_instructions.append(f"Audio: {instruction}")
                    accessible_content['audio_instructions'] = audio_instructions
            
            # Hearing impairment adaptations
            if 'hearing_impairment' in accessibility_needs:
                accessibility_features.extend([
                    "Visual cues and indicators",
                    "Text-based instructions",
                    "Sign language video available",
                    "Vibration alerts for timing"
                ])
            
            # Motor impairment adaptations
            if 'motor_impairment' in accessibility_needs:
                accessibility_features.extend([
                    "Eye tracking navigation supported",
                    "Voice control available",
                    "Simplified gestures",
                    "Adjustable timing"
                ])
                
                # Modify movement-based activities
                if therapy_content.get('therapy_type') == 'movement':
                    accessible_content['adapted_movements'] = [
                        "Seated variations available",
                        "Upper body focus options",
                        "Breathing-based alternatives"
                    ]
            
            # Cognitive accessibility
            if 'cognitive_support' in accessibility_needs:
                accessibility_features.extend([
                    "Simplified language",
                    "Step-by-step breakdown",
                    "Visual aids and diagrams",
                    "Repetition and reinforcement"
                ])
                
                # Simplify instructions
                if 'instructions' in accessible_content:
                    simplified_instructions = []
                    for instruction in accessible_content['instructions']:
                        # Break down complex instructions
                        if len(instruction) > 50:
                            parts = instruction.split('. ')
                            simplified_instructions.extend(parts)
                        else:
                            simplified_instructions.append(instruction)
                    accessible_content['simplified_instructions'] = simplified_instructions
            
            accessible_content['accessibility_features'] = accessibility_features
            
            return accessible_content
            
        except Exception as e:
            logger.error(f"Accessibility features error: {e}")
            return therapy_content
    
    def _add_progress_tracking(self, therapy_content: Dict[str, Any], emotion_state: Dict[str, Any]) -> Dict[str, Any]:
        """Add progress tracking features to therapy content"""
        try:
            tracked_content = therapy_content.copy()
            
            # Pre-activity assessment
            tracked_content['pre_activity_questions'] = [
                "Rate your current stress level (1-10)",
                "How are you feeling right now?",
                "What's your energy level (1-10)?",
                "Any specific concerns or thoughts?"
            ]
            
            # Post-activity assessment
            tracked_content['post_activity_questions'] = [
                "Rate your stress level now (1-10)",
                "How do you feel after this activity?",
                "What's your energy level now (1-10)?",
                "What did you find most helpful?",
                "Would you do this activity again?"
            ]
            
            # Progress indicators
            tracked_content['progress_indicators'] = [
                "Stress level change",
                "Mood improvement",
                "Energy level change",
                "Engagement level",
                "Completion rate"
            ]
            
            # Effectiveness tracking
            tracked_content['effectiveness_metrics'] = {
                'immediate_relief': 'How much immediate relief did you feel?',
                'technique_usefulness': 'How useful was this technique?',
                'likelihood_to_repeat': 'How likely are you to use this again?',
                'overall_satisfaction': 'Overall satisfaction with this session'
            }
            
            # Personalized follow-up suggestions
            primary_emotion = emotion_state.get('primary_emotion', 'neutral')
            if primary_emotion in ['anxious', 'stressed']:
                tracked_content['follow_up_suggestions'] = [
                    "Practice this technique daily for best results",
                    "Try shorter sessions if feeling overwhelmed",
                    "Combine with physical exercise for enhanced benefits"
                ]
            elif primary_emotion in ['sad', 'depressed']:
                tracked_content['follow_up_suggestions'] = [
                    "Consider journaling about your experience",
                    "Share your feelings with someone you trust",
                    "Schedule regular self-care activities"
                ]
            
            return tracked_content
            
        except Exception as e:
            logger.error(f"Progress tracking error: {e}")
            return therapy_content
    
    def _generate_high_risk_intervention(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate high-risk crisis intervention content"""
        return {
            'therapy_type': 'crisis_intervention',
            'title': 'Immediate Safety and Support',
            'description': 'Immediate steps to ensure your safety and connect with support',
            'instructions': [
                'Take slow, deep breaths - in for 4, hold for 4, out for 4',
                'Find a safe, comfortable space',
                'Reach out to a trusted person immediately',
                'Contact crisis helpline if needed',
                'Remove any harmful objects from your vicinity',
                'Stay with someone if possible'
            ],
            'duration': 'Immediate - ongoing',
            'difficulty': 'guided',
            'emergency_contacts': [
                'AASRA: 91-22-27546669',
                'Sneha: 044-24640050',
                'Vandrevala Foundation: 1860-2662-345'
            ],
            'safety_plan': 'Focus on immediate safety and professional support',
            'follow_up_required': True
        }
    
    def _generate_moderate_risk_support(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate moderate-risk support content"""
        return {
            'therapy_type': 'support_intervention',
            'title': 'Coping and Support Strategies',
            'description': 'Techniques to manage difficult emotions and build support',
            'instructions': [
                'Practice grounding: Name 5 things you see, 4 you hear, 3 you touch',
                'Use breathing techniques to calm your nervous system',
                'Write down your thoughts and feelings',
                'Identify people you can talk to',
                'Plan one small positive activity for today',
                'Set up regular check-ins with support person'
            ],
            'duration': '20-30 minutes',
            'difficulty': 'medium',
            'support_resources': [
                'School counselor',
                'Family members',
                'Trusted friends',
                'Mental health professionals'
            ],
            'monitoring_plan': 'Daily mood check-ins and weekly support contact'
        }
    
    def _generate_preventive_wellness(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate preventive wellness content"""
        return {
            'therapy_type': 'preventive_wellness',
            'title': 'Building Mental Resilience',
            'description': 'Proactive strategies to maintain and improve mental wellness',
            'instructions': [
                'Establish a daily mindfulness practice',
                'Maintain regular sleep schedule',
                'Engage in physical activity you enjoy',
                'Connect with friends and family regularly',
                'Practice gratitude journaling',
                'Learn stress management techniques'
            ],
            'duration': '15-45 minutes daily',
            'difficulty': 'easy',
            'wellness_activities': [
                'Meditation',
                'Exercise',
                'Creative activities',
                'Social connections',
                'Nature time'
            ],
            'early_warning_signs': [
                'Sleep changes',
                'Mood shifts',
                'Social withdrawal',
                'Academic stress'
            ]
        }
    
    def _get_fallback_therapy(self, emotion_state: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Get fallback therapy content when generation fails"""
        return {
            'therapy_type': 'mindfulness',
            'title': 'Simple Breathing Exercise',
            'description': 'A basic breathing exercise to help calm your mind and body',
            'instructions': [
                'Sit or lie down in a comfortable position',
                'Close your eyes or soften your gaze',
                'Breathe in slowly through your nose for 4 counts',
                'Hold your breath gently for 4 counts',
                'Breathe out slowly through your mouth for 6 counts',
                'Repeat this cycle 5-10 times',
                'Notice how your body feels after completing the exercise'
            ],
            'duration': '5-10 minutes',
            'difficulty': 'easy',
            'cultural_adaptation': 'This practice is similar to pranayama in yoga',
            'accessibility_features': ['Audio guidance available', 'Can be done anywhere'],
            'follow_up_questions': [
                'How do you feel now compared to before?',
                'Was this technique helpful for you?',
                'Would you like to try this again?'
            ]
        }
    
    def _get_emergency_fallback(self) -> Dict[str, Any]:
        """Get emergency fallback content for crisis situations"""
        return {
            'therapy_type': 'emergency',
            'title': 'Immediate Support',
            'description': 'If you are in crisis, please reach out for help immediately',
            'instructions': [
                'Contact emergency services if in immediate danger',
                'Call a crisis helpline',
                'Reach out to a trusted adult',
                'Go to the nearest hospital emergency room if needed'
            ],
            'emergency_contacts': [
                'Emergency: 112',
                'AASRA: 91-22-27546669',
                'Sneha: 044-24640050'
            ],
            'immediate_action': 'Your safety is the top priority. Please seek help immediately.'
        }