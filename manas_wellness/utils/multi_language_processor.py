# 🧠 Manas: Multi-Language Processing System
# Support for Indian regional languages and cultural contexts

import json
import logging
from typing import Dict, List, Optional, Any
import re

from .gemini_api import gemini_text

# Configure logging
logger = logging.getLogger(__name__)

class MultiLanguageProcessor:
    """Multi-language processing system for Indian regional languages"""
    
    def __init__(self):
        """Initialize multi-language processor"""
        # Supported languages
        self.supported_languages = {
            'english': {
                'name': 'English',
                'code': 'en',
                'script': 'latin',
                'direction': 'ltr'
            },
            'hindi': {
                'name': 'हिंदी',
                'code': 'hi',
                'script': 'devanagari',
                'direction': 'ltr'
            },
            'telugu': {
                'name': 'తెలుగు',
                'code': 'te',
                'script': 'telugu',
                'direction': 'ltr'
            },
            'tamil': {
                'name': 'தமிழ்',
                'code': 'ta',
                'script': 'tamil',
                'direction': 'ltr'
            },
            'bengali': {
                'name': 'বাংলা',
                'code': 'bn',
                'script': 'bengali',
                'direction': 'ltr'
            },
            'gujarati': {
                'name': 'ગુજરાતી',
                'code': 'gu',
                'script': 'gujarati',
                'direction': 'ltr'
            },
            'marathi': {
                'name': 'मराठी',
                'code': 'mr',
                'script': 'devanagari',
                'direction': 'ltr'
            },
            'kannada': {
                'name': 'ಕನ್ನಡ',
                'code': 'kn',
                'script': 'kannada',
                'direction': 'ltr'
            },
            'malayalam': {
                'name': 'മലയാളം',
                'code': 'ml',
                'script': 'malayalam',
                'direction': 'ltr'
            },
            'punjabi': {
                'name': 'ਪੰਜਾਬੀ',
                'code': 'pa',
                'script': 'gurmukhi',
                'direction': 'ltr'
            }
        }
        
        # Cultural context mappings
        self.cultural_contexts = {
            'hindi': {
                'greeting': 'नमस्ते',
                'family_terms': ['माता-पिता', 'परिवार', 'बुजुर्ग'],
                'spiritual_terms': ['शांति', 'ध्यान', 'योग', 'प्राणायाम'],
                'emotional_terms': {
                    'stress': 'तनाव',
                    'anxiety': 'चिंता',
                    'peace': 'शांति',
                    'happiness': 'खुशी',
                    'sadness': 'उदासी'
                }
            },
            'telugu': {
                'greeting': 'నమస్కారం',
                'family_terms': ['తల్లిదండ్రులు', 'కుటుంబం', 'పెద్దలు'],
                'spiritual_terms': ['శాంతి', 'ధ్యానం', 'యోగా', 'ప్రాణాయామం'],
                'emotional_terms': {
                    'stress': 'ఒత్తిడి',
                    'anxiety': 'ఆందోళన',
                    'peace': 'శాంతి',
                    'happiness': 'ఆనందం',
                    'sadness': 'దుఃఖం'
                }
            },
            'tamil': {
                'greeting': 'வணக்கம்',
                'family_terms': ['பெற்றோர்', 'குடும்பம்', 'பெரியவர்கள்'],
                'spiritual_terms': ['அமைதி', 'தியானம்', 'யோகா', 'பிராணாயாமம்'],
                'emotional_terms': {
                    'stress': 'மன அழுத்தம்',
                    'anxiety': 'கவலை',
                    'peace': 'அமைதி',
                    'happiness': 'மகிழ்ச்சி',
                    'sadness': 'துக்கம்'
                }
            }
        }
        
        # Common mental health terms in different languages
        self.mental_health_vocabulary = {
            'english': {
                'mental_health': 'mental health',
                'wellbeing': 'wellbeing',
                'therapy': 'therapy',
                'counseling': 'counseling',
                'meditation': 'meditation',
                'breathing': 'breathing exercise',
                'mindfulness': 'mindfulness',
                'support': 'support',
                'help': 'help',
                'crisis': 'crisis'
            },
            'hindi': {
                'mental_health': 'मानसिक स्वास्थ्य',
                'wellbeing': 'कल्याण',
                'therapy': 'चिकित्सा',
                'counseling': 'परामर्श',
                'meditation': 'ध्यान',
                'breathing': 'श्वास अभ्यास',
                'mindfulness': 'सचेतता',
                'support': 'सहायता',
                'help': 'मदद',
                'crisis': 'संकट'
            },
            'telugu': {
                'mental_health': 'మానసిక ఆరోగ్యం',
                'wellbeing': 'క్షేమం',
                'therapy': 'చికిత్స',
                'counseling': 'సలహా',
                'meditation': 'ధ్యానం',
                'breathing': 'శ్వాస వ్యాయామం',
                'mindfulness': 'అవగాహన',
                'support': 'మద్దతు',
                'help': 'సహాయం',
                'crisis': 'సంక్షోభం'
            }
        }
        
        logger.info("MultiLanguageProcessor initialized successfully")
    
    def translate(self, text: str, target_language: str, context: str = "mental_health") -> str:
        """
        Translate text to target language with cultural context
        
        Args:
            text: Text to translate
            target_language: Target language code
            context: Context for translation (mental_health, therapy, etc.)
        
        Returns:
            Translated text
        """
        try:
            if target_language == 'english' or target_language not in self.supported_languages:
                return text
            
            # Get language info
            lang_info = self.supported_languages[target_language]
            cultural_context = self.cultural_contexts.get(target_language, {})
            
            # Create translation prompt with cultural context
            prompt = f"""
            Translate the following text to {lang_info['name']} ({target_language}):
            "{text}"
            
            Context: {context}
            
            Guidelines:
            1. Maintain cultural sensitivity for Indian {target_language} speakers
            2. Use appropriate formal/informal tone for mental health context
            3. Include cultural concepts where relevant
            4. Ensure the translation is natural and empathetic
            5. Consider family and social dynamics in Indian culture
            
            Cultural terms to consider:
            - Family: {cultural_context.get('family_terms', [])}
            - Spiritual: {cultural_context.get('spiritual_terms', [])}
            - Emotional: {cultural_context.get('emotional_terms', {})}
            
            Return only the translated text.
            """
            
            translated_text = gemini_text(prompt)
            
            # Post-process translation
            processed_text = self._post_process_translation(translated_text, target_language)
            
            return processed_text
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text  # Return original text if translation fails
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language of input text
        
        Args:
            text: Text to analyze
        
        Returns:
            Language detection result
        """
        try:
            # Use simple heuristics first
            detected_lang = self._heuristic_language_detection(text)
            
            if detected_lang:
                return {
                    'language': detected_lang,
                    'confidence': 0.8,
                    'method': 'heuristic'
                }
            
            # Use AI for more complex detection
            prompt = f"""
            Detect the language of this text: "{text}"
            
            Consider these Indian languages:
            - English
            - Hindi (हिंदी)
            - Telugu (తెలుగు)
            - Tamil (தமிழ்)
            - Bengali (বাংলা)
            - Gujarati (ગુજરાતી)
            - Marathi (मराठी)
            - Kannada (ಕನ್ನಡ)
            - Malayalam (മലയാളം)
            - Punjabi (ਪੰਜਾਬੀ)
            
            Return only the language name in lowercase (e.g., "hindi", "english", "telugu").
            """
            
            detected_language = gemini_text(prompt).strip().lower()
            
            if detected_language in self.supported_languages:
                return {
                    'language': detected_language,
                    'confidence': 0.9,
                    'method': 'ai_detection'
                }
            else:
                return {
                    'language': 'english',
                    'confidence': 0.5,
                    'method': 'fallback'
                }
                
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return {
                'language': 'english',
                'confidence': 0.3,
                'method': 'error_fallback'
            }
    
    def localize_content(self, content: Dict[str, Any], target_language: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Localize content for specific language and cultural context
        
        Args:
            content: Content to localize
            target_language: Target language
            user_context: User cultural context
        
        Returns:
            Localized content
        """
        try:
            if target_language == 'english':
                return content
            
            localized_content = content.copy()
            
            # Localize text fields
            text_fields = ['title', 'description', 'instructions']
            for field in text_fields:
                if field in content:
                    if isinstance(content[field], str):
                        localized_content[field] = self.translate(content[field], target_language)
                    elif isinstance(content[field], list):
                        localized_content[field] = [
                            self.translate(item, target_language) if isinstance(item, str) else item
                            for item in content[field]
                        ]
            
            # Add cultural adaptations
            cultural_adaptations = self._get_cultural_adaptations(target_language, user_context)
            localized_content['cultural_adaptations'] = cultural_adaptations
            
            # Add language-specific metadata
            localized_content['language'] = target_language
            localized_content['script'] = self.supported_languages[target_language]['script']
            localized_content['direction'] = self.supported_languages[target_language]['direction']
            
            return localized_content
            
        except Exception as e:
            logger.error(f"Content localization error: {e}")
            return content
    
    def generate_culturally_appropriate_response(self, user_input: str, user_language: str, emotional_context: Dict[str, Any]) -> str:
        """
        Generate culturally appropriate response in user's language
        
        Args:
            user_input: User's input text
            user_language: User's preferred language
            emotional_context: Current emotional context
        
        Returns:
            Culturally appropriate response
        """
        try:
            lang_info = self.supported_languages.get(user_language, self.supported_languages['english'])
            cultural_context = self.cultural_contexts.get(user_language, {})
            
            prompt = f"""
            Generate a culturally sensitive and empathetic response in {lang_info['name']} for:
            User input: "{user_input}"
            
            Context:
            - Language: {user_language}
            - Emotional state: {emotional_context.get('primary_emotion', 'neutral')}
            - Intensity: {emotional_context.get('emotion_intensity', 5)}/10
            
            Cultural considerations for Indian {user_language} speakers:
            - Family values and respect for elders
            - Educational and career pressures
            - Community and social expectations
            - Spiritual and traditional practices
            - Regional cultural nuances
            
            Guidelines:
            1. Be warm, empathetic, and respectful
            2. Acknowledge cultural context appropriately
            3. Use culturally relevant metaphors or examples
            4. Consider family dynamics in advice
            5. Be sensitive to mental health stigma
            6. Offer practical, culturally appropriate coping strategies
            
            Respond in {lang_info['name']} with cultural sensitivity.
            """
            
            response = gemini_text(prompt)
            
            # Add cultural greeting if appropriate
            if cultural_context.get('greeting') and emotional_context.get('primary_emotion') not in ['crisis', 'emergency']:
                greeting = cultural_context['greeting']
                if not response.startswith(greeting):
                    response = f"{greeting}! {response}"
            
            return response
            
        except Exception as e:
            logger.error(f"Culturally appropriate response generation error: {e}")
            return "I understand you're going through a difficult time. Please know that support is available, and it's okay to seek help."
    
    def get_crisis_resources_by_language(self, language: str) -> Dict[str, Any]:
        """
        Get crisis resources localized for specific language
        
        Args:
            language: Target language
        
        Returns:
            Localized crisis resources
        """
        try:
            # Base crisis resources
            crisis_resources = {
                'emergency_contacts': [
                    {'name': 'AASRA', 'number': '91-22-27546669', 'hours': '24/7'},
                    {'name': 'Sneha', 'number': '044-24640050', 'hours': '24/7'},
                    {'name': 'Vandrevala Foundation', 'number': '1860-2662-345', 'hours': '24/7'},
                    {'name': 'Emergency Services', 'number': '112', 'type': 'emergency'}
                ],
                'immediate_actions': [
                    'Take slow, deep breaths',
                    'Find a safe, comfortable space',
                    'Call a trusted friend or family member',
                    'Contact crisis helpline',
                    'Seek immediate professional help if needed'
                ]
            }
            
            # Localize content
            if language != 'english':
                localized_resources = self.localize_content(crisis_resources, language)
                
                # Add language-specific helplines if available
                language_specific_helplines = self._get_language_specific_helplines(language)
                if language_specific_helplines:
                    localized_resources['emergency_contacts'].extend(language_specific_helplines)
                
                return localized_resources
            
            return crisis_resources
            
        except Exception as e:
            logger.error(f"Crisis resources localization error: {e}")
            return crisis_resources
    
    def _heuristic_language_detection(self, text: str) -> Optional[str]:
        """Simple heuristic language detection"""
        try:
            # Check for script patterns
            if re.search(r'[\u0900-\u097F]', text):  # Devanagari (Hindi/Marathi)
                if any(word in text for word in ['मराठी', 'महाराष्ट्र']):
                    return 'marathi'
                return 'hindi'
            elif re.search(r'[\u0C00-\u0C7F]', text):  # Telugu
                return 'telugu'
            elif re.search(r'[\u0B80-\u0BFF]', text):  # Tamil
                return 'tamil'
            elif re.search(r'[\u0980-\u09FF]', text):  # Bengali
                return 'bengali'
            elif re.search(r'[\u0A80-\u0AFF]', text):  # Gujarati
                return 'gujarati'
            elif re.search(r'[\u0C80-\u0CFF]', text):  # Kannada
                return 'kannada'
            elif re.search(r'[\u0D00-\u0D7F]', text):  # Malayalam
                return 'malayalam'
            elif re.search(r'[\u0A00-\u0A7F]', text):  # Gurmukhi (Punjabi)
                return 'punjabi'
            elif re.search(r'^[a-zA-Z\s.,!?]+$', text):  # Latin script
                return 'english'
            
            return None
            
        except Exception as e:
            logger.error(f"Heuristic language detection error: {e}")
            return None
    
    def _post_process_translation(self, translated_text: str, target_language: str) -> str:
        """Post-process translated text for quality"""
        try:
            # Remove any unwanted prefixes/suffixes from AI response
            cleaned_text = translated_text.strip()
            
            # Remove common AI response patterns
            patterns_to_remove = [
                r'^Translation:\s*',
                r'^Translated text:\s*',
                r'^In ' + target_language + r':\s*',
                r'^Here is the translation:\s*'
            ]
            
            for pattern in patterns_to_remove:
                cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)
            
            return cleaned_text.strip()
            
        except Exception as e:
            logger.error(f"Translation post-processing error: {e}")
            return translated_text
    
    def _get_cultural_adaptations(self, language: str, user_context: Dict[str, Any] = None) -> List[str]:
        """Get cultural adaptations for specific language"""
        adaptations = []
        
        cultural_context = self.cultural_contexts.get(language, {})
        
        if cultural_context:
            adaptations.append(f"Content adapted for {language} cultural context")
            
            if 'family_terms' in cultural_context:
                adaptations.append("Considers family dynamics and relationships")
            
            if 'spiritual_terms' in cultural_context:
                adaptations.append("Incorporates traditional spiritual practices")
        
        # Add user-specific adaptations
        if user_context:
            if user_context.get('age', 0) < 18:
                adaptations.append("Age-appropriate content for youth")
            
            if user_context.get('educational_context'):
                adaptations.append("Considers academic and career pressures")
        
        return adaptations
    
    def _get_language_specific_helplines(self, language: str) -> List[Dict[str, str]]:
        """Get language-specific crisis helplines"""
        # This would be expanded with actual regional helplines
        language_helplines = {
            'hindi': [
                {'name': 'Kiran (Hindi)', 'number': '1800-599-0019', 'hours': '24/7'}
            ],
            'tamil': [
                {'name': 'Sneha (Tamil)', 'number': '044-24640050', 'hours': '24/7'}
            ],
            'telugu': [
                {'name': 'Roshni (Telugu)', 'number': '040-66202000', 'hours': '11 AM - 9 PM'}
            ]
        }
        
        return language_helplines.get(language, [])