# 🧠 Manas: Gemini AI Integration
# Advanced AI processing for mental wellness platform

import google.generativeai as genai
import os
import json
import logging
import re
from datetime import datetime
from PIL import Image
import tempfile
from typing import Dict, List, Optional, Any

# Configure logging
logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
DEMO_MODE = False  # Always use real API now

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API configured successfully")
else:
    logger.error("GEMINI_API_KEY not found in environment variables")

def gemini_text(prompt: str, model_name: str = "gemini-1.5-flash", max_retries: int = 2) -> str:
    """
    Generate text response using Gemini AI
    
    Args:
        prompt: Input prompt for text generation
        model_name: Gemini model to use
        max_retries: Number of retry attempts
    
    Returns:
        Generated text response
    """
    try:
        model = genai.GenerativeModel(model_name)
        
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=2048,
            temperature=0.7,
            top_p=0.8,
            top_k=40
        )
        
        response = model.generate_content(prompt, generation_config=generation_config)
        return response.text
        
    except Exception as e:
        logger.error(f"Gemini text generation error: {e}")
        if max_retries > 0:
            return gemini_text(prompt, model_name, max_retries - 1)
        
        # Return a fallback response for mental wellness
        if "emotion" in prompt.lower() or "analyze" in prompt.lower():
            return json.dumps({
                "primary_emotion": "neutral",
                "emotion_intensity": 5,
                "sentiment_score": 0.0,
                "mental_health_indicators": ["analysis_unavailable"],
                "risk_level": 0.1,
                "confidence": 0.3,
                "recommendations": "I'm currently unable to analyze your emotions. Please try again later or reach out for support if needed.",
                "cultural_context": "Remember that seeking help is a sign of strength in any culture."
            })
        return f"I'm currently experiencing technical difficulties. Please try again later. Error: {str(e)}"

def gemini_multimodal(image_path: str, prompt: str, model_name: str = "gemini-1.5-flash") -> str:
    """
    Generate response from image and text using Gemini Vision with enhanced analysis
    
    Args:
        image_path: Path to image file
        prompt: Text prompt to accompany image
        model_name: Gemini model to use
    
    Returns:
        Generated response based on image and text analysis
    """
    try:
        model = genai.GenerativeModel(model_name)
        image = Image.open(image_path)
        
        # Enhanced prompt for facial emotion analysis
        enhanced_prompt = f"""
        You are an expert clinical psychologist analyzing facial expressions for mental wellness assessment. 

        {prompt}

        Analyze this facial image and provide a detailed psychological assessment in JSON format:

        {{
            "facial_emotion_detected": "string - primary emotion from facial expression",
            "emotion_intensity": number (1-10),
            "confidence": number (0-1),
            "facial_features_analysis": {{
                "eye_expression": "string - description of eye area emotions",
                "mouth_expression": "string - description of mouth area emotions", 
                "eyebrow_position": "string - eyebrow positioning analysis",
                "overall_tension": "string - facial tension assessment"
            }},
            "emotions": {{
                "happy": number (0-100 percentage),
                "sad": number (0-100 percentage),
                "angry": number (0-100 percentage),
                "surprised": number (0-100 percentage),
                "neutral": number (0-100 percentage),
                "anxious": number (0-100 percentage)
            }},
            "mental_wellness_indicators": ["array of indicators from facial analysis"],
            "cultural_considerations": "string - considerations for Indian youth",
            "recommendations": "string - therapeutic recommendations based on facial expression",
            "image_quality_assessment": "string - assessment of image quality for analysis"
        }}

        Consider these facial analysis factors:
        - Micro-expressions around eyes and mouth
        - Facial muscle tension patterns
        - Eye contact and gaze direction
        - Symmetry of facial expression
        - Cultural norms in emotional expression for Indian youth

        Return only valid JSON without markdown formatting.
        """
        
        generation_config = genai.types.GenerationConfig(
            max_output_tokens=2048,
            temperature=0.3,  # Lower temperature for more consistent analysis
            top_p=0.8,
            top_k=40
        )
        
        response = model.generate_content([enhanced_prompt, image], generation_config=generation_config)
        
        # Try to extract and validate JSON from response
        response_text = response.text
        
        # Clean up the response to extract JSON
        import re
        json_patterns = [
            r'```json\s*(\{.*?\})\s*```',
            r'```\s*(\{.*?\})\s*```', 
            r'(\{.*\})'
        ]
        
        for pattern in json_patterns:
            match = re.search(pattern, response_text, re.DOTALL)
            if match:
                try:
                    json_str = match.group(1)
                    parsed_result = json.loads(json_str)
                    # Return the validated JSON as string
                    return json.dumps(parsed_result)
                except json.JSONDecodeError:
                    continue
        
        # If no valid JSON found, return the raw response
        return response_text
        
    except Exception as e:
        logger.error(f"Gemini multimodal error: {e}")
        # Return enhanced fallback response for facial emotion analysis
        fallback_response = {
            "facial_emotion_detected": "neutral",
            "emotion_intensity": 5,
            "confidence": 0.3,
            "facial_features_analysis": {
                "eye_expression": "Unable to analyze due to technical error",
                "mouth_expression": "Unable to analyze due to technical error",
                "eyebrow_position": "Unable to analyze due to technical error", 
                "overall_tension": "Unable to analyze due to technical error"
            },
            "emotions": {
                "neutral": 60,
                "happy": 20,
                "sad": 10,
                "angry": 5,
                "surprised": 3,
                "anxious": 2
            },
            "mental_wellness_indicators": ["analysis_unavailable"],
            "cultural_considerations": "Technical difficulties prevent detailed cultural analysis",
            "recommendations": f"Image analysis is currently unavailable ({str(e)}). Please try text or voice input instead.",
            "image_quality_assessment": "Unable to assess due to technical error",
            "error": str(e),
            "fallback_used": True
        }
        return json.dumps(fallback_response)

def gemini_analyze_emotion(text: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Analyze emotional content using Gemini AI with advanced prompting
    
    Args:
        text: Text to analyze for emotional content
        context: Additional context for analysis
    
    Returns:
        Dictionary containing emotion analysis results
    """
    modality = context.get('modality', 'text') if context else 'text'
    user_age = context.get('age', 18) if context else 18
    
    prompt = f"""
    You are an expert clinical psychologist specializing in youth mental health in India. Analyze the following {modality} input for emotional state and mental wellness indicators.

    {f"Text Input: '{text}'" if modality == 'text' else f"Analysis Context: {text}"}
    
    {"Additional Context: " + json.dumps(context) if context else ""}

    Provide a comprehensive psychological assessment in JSON format with these exact fields:

    {{
        "primary_emotion": "string - one of: happy, sad, anxious, angry, neutral, excited, confused, depressed, hopeless, stressed, calm",
        "emotion_intensity": number (1-10 where 1=very mild, 10=extremely intense),
        "sentiment_score": number (-1 to 1 where -1=very negative, 0=neutral, 1=very positive),
        "mental_health_indicators": ["array of strings like stress, depression, anxiety, social_withdrawal, academic_pressure, family_conflict, etc."],
        "risk_level": number (0-1 where 0=no risk, 1=extreme crisis risk),
        "confidence": number (0-1 confidence in this analysis),
        "recommendations": "string - specific therapeutic recommendations appropriate for {user_age}-year-old Indian youth",
        "cultural_context": "string - considerations for Indian family/social context",
        "immediate_actions": "string - if risk_level > 0.7, provide crisis intervention steps",
        "therapy_type": "string - suggested therapy approach: mindfulness, cbt, art_therapy, breathing, journaling, etc.",
        "follow_up_timeline": "string - when to reassess (immediately, daily, weekly, etc.)"
    }}

    Consider these factors specific to Indian youth:
    - Academic pressure and competitive environment
    - Family expectations and intergenerational dynamics
    - Social stigma around mental health
    - Economic stress and career uncertainty
    - Cultural transitions and identity formation
    - Digital media influence and social comparison

    For risk assessment, consider:
    - HIGH RISK (0.8-1.0): Suicidal ideation, self-harm, complete hopelessness
    - MODERATE RISK (0.5-0.7): Persistent depression, severe anxiety, social isolation
    - LOW RISK (0.0-0.4): Normal stress, mild mood fluctuations, manageable challenges

    Return only valid JSON without any markdown formatting or additional text.
    """
    
    try:
        response = gemini_text(prompt)
        logger.info(f"Raw Gemini emotion response: {response[:200]}...")
        
        # Clean the response more thoroughly
        response_clean = response.strip()
        
        # Remove markdown code blocks
        import re
        json_patterns = [
            r'```json\s*(\{.*?\})\s*```',  # ```json { ... } ```
            r'```\s*(\{.*?\})\s*```',      # ``` { ... } ```
            r'(\{.*\})',                    # Just the JSON object
        ]
        
        parsed_json = None
        for pattern in json_patterns:
            match = re.search(pattern, response_clean, re.DOTALL)
            if match:
                try:
                    json_str = match.group(1)
                    parsed_json = json.loads(json_str)
                    break
                except json.JSONDecodeError:
                    continue
        
        if parsed_json:
            # Validate and sanitize the response
            emotion_data = {
                "primary_emotion": parsed_json.get("primary_emotion", "neutral"),
                "emotion_intensity": max(1, min(10, int(parsed_json.get("emotion_intensity", 5)))),
                "sentiment_score": max(-1, min(1, float(parsed_json.get("sentiment_score", 0.0)))),
                "mental_health_indicators": parsed_json.get("mental_health_indicators", []),
                "risk_level": max(0, min(1, float(parsed_json.get("risk_level", 0.0)))),
                "confidence": max(0, min(1, float(parsed_json.get("confidence", 0.5)))),
                "recommendations": parsed_json.get("recommendations", "Take time for self-care and consider talking to someone you trust."),
                "cultural_context": parsed_json.get("cultural_context", "Consider family support and cultural values in your wellness journey."),
                "immediate_actions": parsed_json.get("immediate_actions", ""),
                "therapy_type": parsed_json.get("therapy_type", "mindfulness"),
                "follow_up_timeline": parsed_json.get("follow_up_timeline", "weekly")
            }
            
            # Add analysis metadata
            emotion_data.update({
                "analysis_timestamp": datetime.now().isoformat(),
                "model_used": "gemini-1.5-flash",
                "analysis_version": "2.0"
            })
            
            return emotion_data
        else:
            raise json.JSONDecodeError("No valid JSON found in response", response_clean, 0)
            
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini emotion analysis JSON: {e}")
        logger.error(f"Raw response was: {response}")
        
        # Enhanced fallback analysis based on text patterns
        return _fallback_emotion_analysis(text, context)
        
    except Exception as e:
        logger.error(f"Gemini emotion analysis error: {e}")
        return _fallback_emotion_analysis(text, context, error=str(e))

def _fallback_emotion_analysis(text: str, context: Dict[str, Any] = None, error: str = None) -> Dict[str, Any]:
    """
    Provide fallback emotion analysis when Gemini API fails
    
    Args:
        text: Text to analyze
        context: Analysis context
        error: Error message if any
    
    Returns:
        Fallback emotion analysis result
    """
    try:
        # Simple keyword-based emotion detection as fallback
        text_lower = text.lower()
        
        # Emotion keywords
        emotion_keywords = {
            'happy': ['happy', 'joy', 'excited', 'great', 'awesome', 'amazing', 'wonderful', 'fantastic', 'good'],
            'sad': ['sad', 'depressed', 'down', 'crying', 'tears', 'unhappy', 'miserable', 'heartbroken'],
            'anxious': ['anxious', 'worried', 'nervous', 'stress', 'panic', 'overwhelmed', 'scared', 'afraid'],
            'angry': ['angry', 'mad', 'furious', 'hate', 'annoyed', 'frustrated', 'irritated', 'rage'],
            'confused': ['confused', 'lost', 'uncertain', 'unsure', 'dont know', "don't know", 'puzzled'],
            'hopeless': ['hopeless', 'worthless', 'useless', 'pointless', 'give up', 'cant do', "can't do"]
        }
        
        # Risk keywords
        high_risk_keywords = ['suicide', 'kill myself', 'end it all', 'no point living', 'want to die', 'self harm']
        moderate_risk_keywords = ['depressed', 'hopeless', 'alone', 'no one cares', 'cant take it', "can't take it"]
        
        # Analyze emotions
        emotion_scores = {}
        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score
        
        # Determine primary emotion
        if sum(emotion_scores.values()) == 0:
            primary_emotion = 'neutral'
            intensity = 3
            confidence = 0.3
        else:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            intensity = min(8, max(3, emotion_scores[primary_emotion] * 2))
            confidence = min(0.7, max(0.4, emotion_scores[primary_emotion] / 5))
        
        # Risk assessment
        risk_level = 0.0
        if any(keyword in text_lower for keyword in high_risk_keywords):
            risk_level = 0.9
        elif any(keyword in text_lower for keyword in moderate_risk_keywords):
            risk_level = 0.6
        elif primary_emotion in ['sad', 'hopeless', 'anxious']:
            risk_level = 0.3
        
        # Generate recommendations
        recommendations_map = {
            'happy': "Continue what you're doing! Consider sharing your positive energy with others.",
            'sad': "It's okay to feel sad. Try talking to someone you trust or practicing mindfulness.",
            'anxious': "Practice deep breathing exercises. Consider breaking down overwhelming tasks into smaller steps.",
            'angry': "Try physical exercise or journaling to process these feelings constructively.",
            'confused': "Take time to reflect. Consider talking to a mentor or counselor for clarity.",
            'hopeless': "These feelings are temporary. Please reach out to a trusted adult or counselor.",
            'neutral': "Maintain your emotional balance with regular self-care activities."
        }
        
        return {
            "primary_emotion": primary_emotion,
            "emotion_intensity": intensity,
            "sentiment_score": -0.5 if primary_emotion in ['sad', 'angry', 'anxious', 'hopeless'] else 0.0 if primary_emotion == 'neutral' else 0.3,
            "mental_health_indicators": [primary_emotion] if primary_emotion != 'neutral' else [],
            "risk_level": risk_level,
            "confidence": confidence,
            "recommendations": recommendations_map.get(primary_emotion, "Consider self-care and talking to someone you trust."),
            "cultural_context": "Remember that seeking help is valued in Indian culture and shows wisdom.",
            "immediate_actions": "Contact emergency services or a trusted adult immediately." if risk_level > 0.7 else "",
            "therapy_type": "mindfulness" if primary_emotion in ['anxious', 'stressed'] else "cbt" if primary_emotion in ['sad', 'hopeless'] else "journaling",
            "follow_up_timeline": "immediately" if risk_level > 0.7 else "daily" if risk_level > 0.5 else "weekly",
            "analysis_timestamp": datetime.now().isoformat(),
            "model_used": "fallback_keyword_analysis",
            "analysis_version": "fallback_1.0",
            "fallback_reason": error if error else "Gemini API unavailable"
        }
        
    except Exception as fallback_error:
        logger.error(f"Fallback analysis error: {fallback_error}")
        return {
            "primary_emotion": "neutral",
            "emotion_intensity": 3,
            "sentiment_score": 0.0,
            "mental_health_indicators": [],
            "risk_level": 0.1,
            "confidence": 0.2,
            "recommendations": "Please try again later or speak with a trusted adult if you need support.",
            "cultural_context": "Your mental health matters and help is available.",
            "immediate_actions": "",
            "therapy_type": "mindfulness",
            "follow_up_timeline": "weekly",
            "analysis_timestamp": datetime.now().isoformat(),
            "model_used": "emergency_fallback",
            "analysis_version": "emergency_1.0",
            "error": str(fallback_error)
        }

def generate_therapy_content(emotion_state: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate personalized therapy content using Gemini AI
    
    Args:
        emotion_state: Current emotional state analysis
        user_profile: User profile information
    
    Returns:
        Dictionary containing therapy content and recommendations
    """
    age = user_profile.get('age', 18)
    language = user_profile.get('language', 'english')
    accessibility_needs = user_profile.get('accessibility_needs', '')
    
    prompt = f"""
    Generate personalized mental wellness therapy content for an Indian youth:
    
    User Profile:
    - Age: {age}
    - Language: {language}
    - Accessibility needs: {accessibility_needs}
    
    Current Emotional State:
    - Primary emotion: {emotion_state.get('primary_emotion', 'neutral')}
    - Intensity: {emotion_state.get('emotion_intensity', 5)}/10
    - Risk level: {emotion_state.get('risk_level', 0.0)}
    - Mental health indicators: {emotion_state.get('mental_health_indicators', [])}
    
    Create therapy content with:
    1. therapy_type: Type of therapy (mindfulness, art, journaling, breathing, etc.)
    2. title: Engaging title for the activity
    3. description: Clear description of the therapy activity
    4. instructions: Step-by-step instructions
    5. duration: Estimated time needed
    6. difficulty: easy/medium/hard
    7. cultural_adaptation: How it's adapted for Indian cultural context
    8. accessibility_features: Adaptations for accessibility needs
    9. follow_up_questions: Questions to ask after completion
    10. effectiveness_tracking: How to measure effectiveness
    
    Consider:
    - Indian cultural values and family dynamics
    - Educational stress common in Indian youth
    - Regional language preferences
    - Accessibility requirements
    - Age-appropriate content
    
    Return only valid JSON.
    """
    
    try:
        response = gemini_text(prompt)
        therapy_content = json.loads(response)
        return therapy_content
        
    except json.JSONDecodeError:
        logger.error("Failed to parse therapy content JSON")
        return {
            "therapy_type": "mindfulness",
            "title": "Simple Breathing Exercise",
            "description": "A basic breathing exercise to help calm your mind",
            "instructions": ["Sit comfortably", "Breathe in for 4 counts", "Hold for 4 counts", "Breathe out for 4 counts", "Repeat 5 times"],
            "duration": "5 minutes",
            "difficulty": "easy",
            "cultural_adaptation": "Can be done anywhere, respects privacy",
            "accessibility_features": "Audio instructions available",
            "follow_up_questions": ["How do you feel now?", "Was this helpful?"],
            "effectiveness_tracking": "Rate your stress level before and after"
        }
    except Exception as e:
        logger.error(f"Therapy content generation error: {e}")
        return {
            "therapy_type": "error",
            "title": "Content Generation Error",
            "description": f"Unable to generate therapy content: {str(e)}",
            "instructions": ["Please try again later"],
            "duration": "0 minutes",
            "difficulty": "easy",
            "cultural_adaptation": "N/A",
            "accessibility_features": "N/A",
            "follow_up_questions": [],
            "effectiveness_tracking": "N/A"
        }

def generate_crisis_intervention(risk_level: float, user_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate crisis intervention content using Gemini AI
    
    Args:
        risk_level: Risk assessment score (0-1)
        user_context: User context and situation
    
    Returns:
        Dictionary containing crisis intervention recommendations
    """
    prompt = f"""
    Generate crisis intervention content for Indian youth mental health:
    
    Risk Level: {risk_level} (0=no risk, 1=extreme risk)
    User Context: {json.dumps(user_context)}
    
    Based on risk level, provide:
    
    If risk_level >= 0.8 (HIGH RISK):
    - immediate_actions: Urgent steps to take
    - emergency_contacts: Crisis helplines in India
    - safety_plan: Immediate safety planning
    - professional_help: When and how to seek professional help
    
    If risk_level >= 0.5 (MODERATE RISK):
    - support_resources: Available support systems
    - coping_strategies: Immediate coping techniques
    - monitoring_plan: How to monitor emotional state
    - escalation_triggers: When to seek more help
    
    If risk_level < 0.5 (LOW RISK):
    - preventative_guidance: Preventive mental health tips
    - wellness_activities: Proactive wellness activities
    - support_network: Building support systems
    - early_warning_signs: Signs to watch for
    
    Include:
    - cultural_sensitivity: Indian cultural considerations
    - family_involvement: How to involve family appropriately
    - stigma_reduction: Addressing mental health stigma
    - local_resources: India-specific resources
    
    Return only valid JSON.
    """
    
    try:
        response = gemini_text(prompt)
        intervention_content = json.loads(response)
        return intervention_content
        
    except json.JSONDecodeError:
        logger.error("Failed to parse crisis intervention JSON")
        # Return safe fallback based on risk level
        if risk_level >= 0.8:
            return {
                "immediate_actions": ["Contact emergency services", "Reach out to trusted adult", "Stay with someone"],
                "emergency_contacts": ["AASRA: 91-22-27546669", "Sneha: 044-24640050", "Vandrevala Foundation: 1860-2662-345"],
                "safety_plan": "Remove harmful objects, stay in safe space, contact support",
                "professional_help": "Seek immediate psychiatric evaluation"
            }
        elif risk_level >= 0.5:
            return {
                "support_resources": ["School counselor", "Family support", "Peer support groups"],
                "coping_strategies": ["Deep breathing", "Grounding techniques", "Physical activity"],
                "monitoring_plan": "Track mood daily, note triggers",
                "escalation_triggers": "Persistent negative thoughts, sleep issues, social withdrawal"
            }
        else:
            return {
                "preventative_guidance": ["Regular exercise", "Healthy sleep", "Social connections"],
                "wellness_activities": ["Meditation", "Journaling", "Creative activities"],
                "support_network": ["Friends", "Family", "Teachers", "Community"],
                "early_warning_signs": ["Mood changes", "Sleep disruption", "Academic stress"]
            }
    except Exception as e:
        logger.error(f"Crisis intervention generation error: {e}")
        return {
            "error": f"Unable to generate intervention content: {str(e)}",
            "emergency_contacts": ["AASRA: 91-22-27546669", "Sneha: 044-24640050"],
            "immediate_action": "If in crisis, please contact emergency services or trusted adult immediately"
        }

def generate_motivational_content(user_profile: Dict[str, Any], context: str = "") -> str:
    """
    Generate culturally appropriate motivational content
    
    Args:
        user_profile: User profile information
        context: Additional context for motivation
    
    Returns:
        Motivational message string
    """
    age = user_profile.get('age', 18)
    language = user_profile.get('language', 'english')
    
    prompt = f"""
    Generate a warm, encouraging, culturally sensitive motivational message for an Indian youth:
    
    Age: {age}
    Language preference: {language}
    Context: {context}
    
    The message should:
    - Be encouraging and hopeful
    - Acknowledge their struggles
    - Include Indian cultural values (family, perseverance, dharma)
    - Be age-appropriate
    - Avoid clichés
    - Be authentic and personal
    - Include practical encouragement
    
    Keep it under 150 words and make it feel like it's from a caring mentor.
    """
    
    try:
        return gemini_text(prompt)
    except Exception as e:
        logger.error(f"Motivational content generation error: {e}")
        return "You are stronger than you know, and this difficult time will pass. Take it one day at a time, and remember that seeking help is a sign of courage, not weakness. You matter, and your wellbeing is important."