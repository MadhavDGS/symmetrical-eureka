# 🧠 Manas: Crisis Detection and Intervention System
# Advanced crisis detection using behavioral pattern analysis and AI

import json
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import numpy as np

from .gemini_api import generate_crisis_intervention, gemini_text

# Configure logging
logger = logging.getLogger(__name__)

class CrisisDetector:
    """Advanced crisis detection and intervention system"""
    
    def __init__(self):
        """Initialize crisis detection system"""
        # Crisis indicators and their weights
        self.crisis_indicators = {
            'emotional': {
                'suicidal_ideation': 1.0,
                'self_harm': 0.9,
                'hopelessness': 0.8,
                'severe_depression': 0.7,
                'panic_attacks': 0.6,
                'extreme_anxiety': 0.6,
                'anger_outbursts': 0.5,
                'emotional_numbness': 0.5
            },
            'behavioral': {
                'social_withdrawal': 0.6,
                'sleep_disruption': 0.4,
                'appetite_changes': 0.4,
                'academic_decline': 0.5,
                'substance_use': 0.7,
                'risky_behavior': 0.6,
                'giving_away_possessions': 0.8,
                'sudden_mood_improvement': 0.7  # Can indicate decision to harm
            },
            'cognitive': {
                'concentration_problems': 0.4,
                'memory_issues': 0.3,
                'negative_self_talk': 0.6,
                'catastrophic_thinking': 0.5,
                'decision_making_difficulty': 0.4,
                'confusion': 0.4
            },
            'physical': {
                'fatigue': 0.3,
                'headaches': 0.2,
                'stomach_problems': 0.2,
                'muscle_tension': 0.3,
                'rapid_heartbeat': 0.4,
                'breathing_difficulty': 0.5
            }
        }
        
        # Crisis keywords for text analysis
        self.crisis_keywords = {
            'high_risk': [
                'suicide', 'kill myself', 'end it all', 'not worth living',
                'better off dead', 'want to die', 'hurt myself', 'cut myself',
                'overdose', 'jump', 'hang', 'gun', 'pills'
            ],
            'moderate_risk': [
                'hopeless', 'worthless', 'useless', 'burden', 'trapped',
                'no way out', 'give up', 'can\'t go on', 'too much',
                'overwhelming', 'exhausted', 'empty', 'numb'
            ],
            'warning_signs': [
                'goodbye', 'sorry for everything', 'forgive me',
                'take care of', 'won\'t need', 'final', 'last time',
                'always remember', 'love you all'
            ]
        }
        
        # Emergency contacts for India
        self.emergency_contacts = {
            'national': [
                {'name': 'AASRA', 'number': '91-22-27546669', 'hours': '24/7'},
                {'name': 'Sneha', 'number': '044-24640050', 'hours': '24/7'},
                {'name': 'Vandrevala Foundation', 'number': '1860-2662-345', 'hours': '24/7'},
                {'name': 'iCall', 'number': '022-25521111', 'hours': '10 AM - 8 PM'},
                {'name': 'Connecting Trust', 'number': '040-67138888', 'hours': '24/7'}
            ],
            'emergency': [
                {'name': 'Emergency Services', 'number': '112', 'type': 'immediate_danger'},
                {'name': 'Police', 'number': '100', 'type': 'immediate_danger'},
                {'name': 'Medical Emergency', 'number': '108', 'type': 'medical'}
            ]
        }
        
        logger.info("CrisisDetector initialized successfully")
    
    def assess_risk(self, emotion_result: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Assess crisis risk based on emotion analysis and user history
        
        Args:
            emotion_result: Current emotion analysis result
            user_id: User identifier
        
        Returns:
            Risk assessment with level and recommendations
        """
        try:
            # Get base risk from emotion analysis
            base_risk = emotion_result.get('risk_level', 0.0)
            
            # Analyze text content if available
            text_risk = 0.0
            if 'text_content' in emotion_result:
                text_risk = self._analyze_text_for_crisis(emotion_result['text_content'])
            
            # Get historical risk patterns
            historical_risk = self._get_historical_risk_pattern(user_id)
            
            # Combine risk factors
            combined_risk = self._combine_risk_factors(base_risk, text_risk, historical_risk)
            
            # Generate risk assessment
            risk_assessment = {
                'risk_level': combined_risk,
                'risk_category': self._categorize_risk(combined_risk),
                'contributing_factors': self._identify_risk_factors(emotion_result),
                'immediate_actions': self._get_immediate_actions(combined_risk),
                'monitoring_required': combined_risk >= 0.3,
                'professional_referral': combined_risk >= 0.6,
                'emergency_intervention': combined_risk >= 0.8,
                'timestamp': datetime.now().isoformat()
            }
            
            # Log risk assessment
            self._log_risk_assessment(user_id, risk_assessment)
            
            return risk_assessment
            
        except Exception as e:
            logger.error(f"Risk assessment error: {e}")
            return {
                'risk_level': 0.5,  # Default to moderate risk for safety
                'risk_category': 'moderate',
                'error': str(e),
                'immediate_actions': ['Contact support person', 'Seek professional help'],
                'emergency_intervention': False
            }
    
    def analyze_risk_level(self, user_data: Dict[str, Any]) -> float:
        """
        Analyze overall risk level from comprehensive user data
        
        Args:
            user_data: Comprehensive user data including emotions, behaviors, etc.
        
        Returns:
            Risk level score (0-1)
        """
        try:
            total_risk = 0.0
            factor_count = 0
            
            # Analyze each category of indicators
            for category, indicators in self.crisis_indicators.items():
                if category in user_data:
                    category_data = user_data[category]
                    for indicator, weight in indicators.items():
                        if indicator in category_data:
                            # Normalize indicator value (assume 0-10 scale)
                            indicator_value = category_data[indicator] / 10.0
                            total_risk += indicator_value * weight
                            factor_count += 1
            
            # Calculate average weighted risk
            if factor_count > 0:
                average_risk = total_risk / factor_count
            else:
                average_risk = 0.0
            
            # Apply additional analysis using AI
            ai_risk = self._ai_risk_analysis(user_data)
            
            # Combine traditional and AI analysis
            final_risk = (average_risk * 0.7) + (ai_risk * 0.3)
            
            return min(final_risk, 1.0)  # Cap at 1.0
            
        except Exception as e:
            logger.error(f"Risk level analysis error: {e}")
            return 0.5  # Default to moderate risk for safety
    
    def emergency_protocol(self, user_id: str) -> Dict[str, Any]:
        """
        Execute emergency protocol for high-risk situations
        
        Args:
            user_id: User identifier
        
        Returns:
            Emergency intervention plan
        """
        try:
            # Generate immediate intervention content
            intervention_content = generate_crisis_intervention(0.9, {'emergency': True})
            
            # Create emergency action plan
            emergency_plan = {
                'immediate_actions': [
                    'Ensure immediate safety',
                    'Contact emergency services if in immediate danger',
                    'Reach out to trusted adult or family member',
                    'Call crisis helpline',
                    'Go to nearest emergency room if necessary'
                ],
                'emergency_contacts': self.emergency_contacts,
                'safety_planning': {
                    'remove_harmful_objects': True,
                    'stay_with_someone': True,
                    'avoid_isolation': True,
                    'professional_help_required': True
                },
                'follow_up_required': True,
                'monitoring_frequency': 'continuous',
                'intervention_content': intervention_content
            }
            
            # Log emergency intervention
            self._log_emergency_intervention(user_id, emergency_plan)
            
            # Notify support system (in production, this would trigger alerts)
            self._notify_support_system(user_id, 'emergency')
            
            return emergency_plan
            
        except Exception as e:
            logger.error(f"Emergency protocol error: {e}")
            return {
                'immediate_actions': ['Contact emergency services: 112', 'Call AASRA: 91-22-27546669'],
                'emergency_contacts': self.emergency_contacts['emergency'],
                'error': str(e)
            }
    
    def support_resources(self, user_id: str) -> Dict[str, Any]:
        """
        Provide support resources for moderate-risk situations
        
        Args:
            user_id: User identifier
        
        Returns:
            Support resources and intervention plan
        """
        try:
            # Generate support intervention content
            intervention_content = generate_crisis_intervention(0.6, {'support_needed': True})
            
            support_plan = {
                'support_resources': [
                    'School counselor or mental health professional',
                    'Trusted family members or friends',
                    'Mental health helplines',
                    'Peer support groups',
                    'Online mental health resources'
                ],
                'coping_strategies': [
                    'Deep breathing exercises',
                    'Grounding techniques (5-4-3-2-1 method)',
                    'Progressive muscle relaxation',
                    'Mindfulness meditation',
                    'Physical exercise or movement',
                    'Creative expression (art, music, writing)'
                ],
                'monitoring_plan': {
                    'daily_check_ins': True,
                    'mood_tracking': True,
                    'trigger_identification': True,
                    'support_person_contact': 'weekly'
                },
                'escalation_triggers': [
                    'Worsening mood or hopelessness',
                    'Thoughts of self-harm',
                    'Increased isolation',
                    'Sleep or appetite changes',
                    'Substance use'
                ],
                'professional_resources': self.emergency_contacts['national'],
                'intervention_content': intervention_content
            }
            
            # Log support intervention
            self._log_support_intervention(user_id, support_plan)
            
            return support_plan
            
        except Exception as e:
            logger.error(f"Support resources error: {e}")
            return {
                'support_resources': ['Contact school counselor', 'Call AASRA: 91-22-27546669'],
                'coping_strategies': ['Deep breathing', 'Talk to trusted person'],
                'error': str(e)
            }
    
    def preventative_guidance(self, user_id: str) -> Dict[str, Any]:
        """
        Provide preventative mental health guidance
        
        Args:
            user_id: User identifier
        
        Returns:
            Preventative guidance and wellness plan
        """
        try:
            # Generate preventative content
            intervention_content = generate_crisis_intervention(0.2, {'preventative': True})
            
            prevention_plan = {
                'wellness_activities': [
                    'Regular exercise or physical activity',
                    'Consistent sleep schedule',
                    'Healthy eating habits',
                    'Social connections and activities',
                    'Hobbies and creative pursuits',
                    'Mindfulness or meditation practice'
                ],
                'stress_management': [
                    'Time management techniques',
                    'Study-life balance',
                    'Relaxation techniques',
                    'Problem-solving skills',
                    'Communication skills',
                    'Boundary setting'
                ],
                'support_network_building': [
                    'Maintain friendships',
                    'Family connections',
                    'Join clubs or groups',
                    'Volunteer activities',
                    'Mentor relationships',
                    'Professional support when needed'
                ],
                'early_warning_signs': [
                    'Changes in sleep patterns',
                    'Mood fluctuations',
                    'Social withdrawal',
                    'Academic or work stress',
                    'Relationship difficulties',
                    'Physical symptoms of stress'
                ],
                'self_care_practices': [
                    'Regular self-reflection',
                    'Gratitude practice',
                    'Setting realistic goals',
                    'Celebrating achievements',
                    'Learning new skills',
                    'Seeking help when needed'
                ],
                'intervention_content': intervention_content
            }
            
            return prevention_plan
            
        except Exception as e:
            logger.error(f"Preventative guidance error: {e}")
            return {
                'wellness_activities': ['Exercise', 'Sleep well', 'Stay connected'],
                'stress_management': ['Deep breathing', 'Time management'],
                'error': str(e)
            }
    
    def _analyze_text_for_crisis(self, text: str) -> float:
        """Analyze text content for crisis indicators"""
        try:
            text_lower = text.lower()
            risk_score = 0.0
            
            # Check for high-risk keywords
            for keyword in self.crisis_keywords['high_risk']:
                if keyword in text_lower:
                    risk_score += 0.3
            
            # Check for moderate-risk keywords
            for keyword in self.crisis_keywords['moderate_risk']:
                if keyword in text_lower:
                    risk_score += 0.1
            
            # Check for warning signs
            for keyword in self.crisis_keywords['warning_signs']:
                if keyword in text_lower:
                    risk_score += 0.2
            
            # Use AI for contextual analysis
            ai_analysis = self._ai_text_analysis(text)
            
            # Combine keyword and AI analysis
            combined_score = min((risk_score * 0.6) + (ai_analysis * 0.4), 1.0)
            
            return combined_score
            
        except Exception as e:
            logger.error(f"Text crisis analysis error: {e}")
            return 0.0
    
    def _ai_text_analysis(self, text: str) -> float:
        """Use AI to analyze text for crisis indicators"""
        try:
            prompt = f"""
            Analyze this text for mental health crisis indicators and suicide risk:
            "{text}"
            
            Consider:
            - Suicidal ideation or self-harm mentions
            - Hopelessness and despair
            - Social isolation indicators
            - Emotional distress level
            - Behavioral warning signs
            
            Return only a risk score from 0.0 to 1.0 where:
            0.0 = No risk indicators
            0.3 = Mild concern
            0.5 = Moderate risk
            0.7 = High risk
            0.9+ = Immediate crisis
            
            Return only the number.
            """
            
            response = gemini_text(prompt)
            
            # Extract numeric score
            try:
                score = float(response.strip())
                return min(max(score, 0.0), 1.0)  # Clamp between 0 and 1
            except ValueError:
                logger.warning(f"Could not parse AI risk score: {response}")
                return 0.0
                
        except Exception as e:
            logger.error(f"AI text analysis error: {e}")
            return 0.0
    
    def _ai_risk_analysis(self, user_data: Dict[str, Any]) -> float:
        """Use AI to analyze comprehensive user data for risk"""
        try:
            prompt = f"""
            Analyze this user data for mental health crisis risk:
            {json.dumps(user_data, indent=2)}
            
            Consider patterns, combinations of factors, and overall risk profile.
            Focus on youth mental health in Indian context.
            
            Return only a risk score from 0.0 to 1.0.
            """
            
            response = gemini_text(prompt)
            
            try:
                score = float(response.strip())
                return min(max(score, 0.0), 1.0)
            except ValueError:
                return 0.0
                
        except Exception as e:
            logger.error(f"AI risk analysis error: {e}")
            return 0.0
    
    def _get_historical_risk_pattern(self, user_id: str) -> float:
        """Get historical risk pattern for user"""
        try:
            # In production, this would query the database for historical data
            # For now, return default
            return 0.0
            
        except Exception as e:
            logger.error(f"Historical risk pattern error: {e}")
            return 0.0
    
    def _combine_risk_factors(self, base_risk: float, text_risk: float, historical_risk: float) -> float:
        """Combine different risk factors into overall risk score"""
        try:
            # Weighted combination
            weights = {'base': 0.5, 'text': 0.3, 'historical': 0.2}
            
            combined = (base_risk * weights['base'] + 
                       text_risk * weights['text'] + 
                       historical_risk * weights['historical'])
            
            return min(combined, 1.0)
            
        except Exception as e:
            logger.error(f"Risk combination error: {e}")
            return max(base_risk, text_risk)  # Use higher of the two main factors
    
    def _categorize_risk(self, risk_level: float) -> str:
        """Categorize risk level"""
        if risk_level >= 0.8:
            return 'critical'
        elif risk_level >= 0.6:
            return 'high'
        elif risk_level >= 0.4:
            return 'moderate'
        elif risk_level >= 0.2:
            return 'low'
        else:
            return 'minimal'
    
    def _identify_risk_factors(self, emotion_result: Dict[str, Any]) -> List[str]:
        """Identify specific risk factors from emotion analysis"""
        factors = []
        
        if emotion_result.get('risk_level', 0) >= 0.5:
            factors.append('High emotional distress')
        
        if emotion_result.get('primary_emotion') in ['sad', 'depressed', 'hopeless']:
            factors.append('Depressive symptoms')
        
        if emotion_result.get('primary_emotion') in ['anxious', 'panicked']:
            factors.append('Anxiety symptoms')
        
        if emotion_result.get('emotion_intensity', 0) >= 8:
            factors.append('High emotional intensity')
        
        return factors
    
    def _get_immediate_actions(self, risk_level: float) -> List[str]:
        """Get immediate actions based on risk level"""
        if risk_level >= 0.8:
            return [
                'Contact emergency services if in immediate danger',
                'Call crisis helpline immediately',
                'Reach out to trusted adult',
                'Ensure immediate safety',
                'Seek professional help'
            ]
        elif risk_level >= 0.5:
            return [
                'Contact support person',
                'Use coping strategies',
                'Monitor emotional state',
                'Consider professional help',
                'Avoid isolation'
            ]
        else:
            return [
                'Practice self-care',
                'Stay connected with support network',
                'Monitor mood changes',
                'Engage in wellness activities'
            ]
    
    def _log_risk_assessment(self, user_id: str, assessment: Dict[str, Any]):
        """Log risk assessment to database"""
        try:
            # In production, this would log to database
            logger.info(f"Risk assessment for user {user_id}: {assessment['risk_category']}")
        except Exception as e:
            logger.error(f"Risk assessment logging error: {e}")
    
    def _log_emergency_intervention(self, user_id: str, plan: Dict[str, Any]):
        """Log emergency intervention"""
        try:
            logger.critical(f"Emergency intervention activated for user {user_id}")
        except Exception as e:
            logger.error(f"Emergency intervention logging error: {e}")
    
    def _log_support_intervention(self, user_id: str, plan: Dict[str, Any]):
        """Log support intervention"""
        try:
            logger.warning(f"Support intervention provided for user {user_id}")
        except Exception as e:
            logger.error(f"Support intervention logging error: {e}")
    
    def _notify_support_system(self, user_id: str, alert_type: str):
        """Notify support system of crisis situation"""
        try:
            # In production, this would trigger notifications to:
            # - Emergency contacts
            # - Mental health professionals
            # - Support network
            logger.critical(f"Support system notification: {alert_type} for user {user_id}")
        except Exception as e:
            logger.error(f"Support system notification error: {e}")