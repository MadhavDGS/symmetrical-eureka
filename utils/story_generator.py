# 🧠 Manas: Story Generator for Therapeutic Narratives
# AI-powered story generation for mental wellness using Gemini API

import json
import logging
import random
from typing import Dict, List, Optional, Any
from datetime import datetime

from .gemini_api import gemini_text

# Configure logging
logger = logging.getLogger(__name__)

class StoryGenerator:
    """AI-powered therapeutic story generator for mental wellness"""
    
    def __init__(self):
        """Initialize story generator with therapeutic themes and templates"""
        self.therapeutic_themes = {
            'overcoming_anxiety': {
                'description': 'Stories about facing fears and managing anxiety',
                'keywords': ['courage', 'breathing', 'mindfulness', 'support', 'growth'],
                'therapeutic_goals': ['build confidence', 'learn coping strategies', 'normalize anxiety'],
                'age_adaptations': {
                    '13-15': 'school situations, peer pressure, identity formation',
                    '16-18': 'academic stress, future planning, relationships',
                    '19-22': 'independence, career choices, new environments',
                    '23-25': 'professional life, adult responsibilities, relationships'
                }
            },
            'building_confidence': {
                'description': 'Narratives about self-worth and personal empowerment',
                'keywords': ['self-esteem', 'achievements', 'talents', 'uniqueness', 'pride'],
                'therapeutic_goals': ['enhance self-image', 'recognize strengths', 'build resilience'],
                'age_adaptations': {
                    '13-15': 'discovering talents, standing up to bullies, finding identity',
                    '16-18': 'leadership roles, academic achievements, creative expression',
                    '19-22': 'career success, independence, meaningful relationships',
                    '23-25': 'professional growth, life milestones, personal values'
                }
            },
            'managing_stress': {
                'description': 'Stories about healthy stress management and balance',
                'keywords': ['balance', 'priorities', 'relaxation', 'boundaries', 'wellness'],
                'therapeutic_goals': ['stress management', 'work-life balance', 'self-care'],
                'age_adaptations': {
                    '13-15': 'schoolwork balance, extracurricular activities, family expectations',
                    '16-18': 'exam pressure, college applications, time management',
                    '19-22': 'academic pressure, part-time work, social obligations',
                    '23-25': 'career demands, financial stress, relationship balance'
                }
            },
            'friendship_support': {
                'description': 'Tales of meaningful friendships and social connections',
                'keywords': ['friendship', 'loyalty', 'communication', 'support', 'trust'],
                'therapeutic_goals': ['social skills', 'relationship building', 'emotional support'],
                'age_adaptations': {
                    '13-15': 'making new friends, dealing with conflicts, group dynamics',
                    '16-18': 'deep friendships, supporting friends, social circles',
                    '19-22': 'college friendships, long-distance relationships, new connections',
                    '23-25': 'adult friendships, professional relationships, community building'
                }
            },
            'family_relationships': {
                'description': 'Stories about family bonds and understanding',
                'keywords': ['family', 'understanding', 'communication', 'love', 'tradition'],
                'therapeutic_goals': ['family harmony', 'intergenerational understanding', 'communication'],
                'age_adaptations': {
                    '13-15': 'parent-teen communication, sibling relationships, family rules',
                    '16-18': 'independence vs family, cultural expectations, future plans',
                    '19-22': 'adult-parent relationships, family traditions, personal choices',
                    '23-25': 'family responsibilities, adult relationships, life decisions'
                }
            },
            'school_challenges': {
                'description': 'Academic and school-related growth stories',
                'keywords': ['learning', 'perseverance', 'growth', 'achievement', 'potential'],
                'therapeutic_goals': ['academic confidence', 'learning strategies', 'goal setting'],
                'age_adaptations': {
                    '13-15': 'study habits, teacher relationships, academic struggles',
                    '16-18': 'college preparation, career exploration, academic pressure',
                    '19-22': 'higher education challenges, skill development, career preparation',
                    '23-25': 'professional development, continuing education, skill building'
                }
            },
            'self_discovery': {
                'description': 'Journeys of personal growth and self-understanding',
                'keywords': ['identity', 'values', 'purpose', 'growth', 'authenticity'],
                'therapeutic_goals': ['self-awareness', 'personal values', 'life purpose'],
                'age_adaptations': {
                    '13-15': 'identity exploration, interests, personal values',
                    '16-18': 'future planning, personal goals, value clarification',
                    '19-22': 'life direction, career paths, personal philosophy',
                    '23-25': 'life purpose, professional identity, personal growth'
                }
            },
            'resilience_growth': {
                'description': 'Stories of overcoming challenges and building strength',
                'keywords': ['resilience', 'strength', 'recovery', 'growth', 'perseverance'],
                'therapeutic_goals': ['build resilience', 'coping skills', 'post-traumatic growth'],
                'age_adaptations': {
                    '13-15': 'overcoming setbacks, building confidence, support systems',
                    '16-18': 'handling rejection, academic failures, relationship challenges',
                    '19-22': 'career setbacks, major transitions, personal challenges',
                    '23-25': 'professional challenges, life transitions, personal setbacks'
                }
            },
            'emotional_healing': {
                'description': 'Stories about processing emotions and healing',
                'keywords': ['healing', 'emotions', 'processing', 'acceptance', 'peace'],
                'therapeutic_goals': ['emotional processing', 'healing trauma', 'self-compassion'],
                'age_adaptations': {
                    '13-15': 'processing difficult emotions, self-compassion, support seeking',
                    '16-18': 'emotional maturity, relationship healing, past experiences',
                    '19-22': 'adult emotional challenges, healing relationships, self-care',
                    '23-25': 'emotional maturity, healing past wounds, healthy relationships'
                }
            },
            'goal_achievement': {
                'description': 'Inspiring stories about pursuing and achieving dreams',
                'keywords': ['dreams', 'goals', 'achievement', 'persistence', 'success'],
                'therapeutic_goals': ['goal setting', 'motivation', 'persistence', 'success mindset'],
                'age_adaptations': {
                    '13-15': 'personal goals, talent development, early achievements',
                    '16-18': 'college goals, career aspirations, personal projects',
                    '19-22': 'academic achievements, career goals, personal milestones',
                    '23-25': 'professional success, life goals, personal achievements'
                }
            }
        }
        
        self.setting_contexts = {
            'school_college': 'educational environment with classrooms, libraries, campus life',
            'home_family': 'family home setting with parents, siblings, extended family',
            'workplace': 'professional environment with colleagues, mentors, work challenges',
            'community': 'local neighborhood, community centers, local events and gatherings',
            'nature_outdoors': 'natural settings like parks, mountains, beaches, gardens',
            'city_urban': 'urban environment with bustling streets, cafes, public spaces',
            'virtual_online': 'digital spaces, online communities, virtual interactions',
            'cultural_traditional': 'traditional Indian settings with festivals, ceremonies, cultural events'
        }
        
        self.story_lengths = {
            'short': {
                'word_count': '400-600 words',
                'reading_time': '2-3 minutes',
                'structure': 'simple narrative with clear beginning, challenge, and resolution'
            },
            'medium': {
                'word_count': '800-1200 words',
                'reading_time': '5-7 minutes',
                'structure': 'detailed narrative with character development and multiple scenes'
            },
            'long': {
                'word_count': '1500-2000 words',
                'reading_time': '10-12 minutes',
                'structure': 'comprehensive story with rich details, dialogue, and deep character growth'
            }
        }

    def generate_story(self, theme: str, character_name: str = None, character_age: str = None, 
                      setting: str = None, challenge: str = None, length: str = 'medium') -> Dict[str, Any]:
        """Generate a therapeutic story using Gemini AI"""
        try:
            # Get theme details
            theme_info = self.therapeutic_themes.get(theme)
            if not theme_info:
                raise ValueError(f"Unknown theme: {theme}")
            
            # Prepare story parameters
            character_name = character_name or self._generate_character_name()
            character_age = character_age or '16-18'
            setting = setting or 'school_college'
            length_info = self.story_lengths.get(length, self.story_lengths['medium'])
            
            # Create story prompt
            story_prompt = self._create_story_prompt(
                theme, theme_info, character_name, character_age, 
                setting, challenge, length_info
            )
            
            logger.info(f"Generating story with theme: {theme}, character: {character_name}")
            
            # Generate story using Gemini
            story_response = gemini_text(story_prompt)
            
            if not story_response:
                raise Exception("Failed to generate story content")
            
            # Generate reflection questions
            reflection_prompt = self._create_reflection_prompt(theme, theme_info, story_response)
            reflection_response = gemini_text(reflection_prompt)
            
            # Format the response
            formatted_story = self._format_story_content(story_response)
            formatted_reflections = self._format_reflection_questions(reflection_response)
            
            return {
                'success': True,
                'story': formatted_story,
                'reflections': formatted_reflections,
                'metadata': {
                    'theme': theme,
                    'character_name': character_name,
                    'character_age': character_age,
                    'setting': setting,
                    'length': length,
                    'generated_at': datetime.now().isoformat(),
                    'therapeutic_goals': theme_info['therapeutic_goals']
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating story: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'fallback_story': self._get_fallback_story(theme)
            }

    def _create_story_prompt(self, theme: str, theme_info: Dict, character_name: str, 
                           character_age: str, setting: str, challenge: str, length_info: Dict) -> str:
        """Create a detailed prompt for story generation"""
        
        age_context = theme_info['age_adaptations'].get(character_age, '')
        setting_context = self.setting_contexts.get(setting, '')
        keywords = ', '.join(theme_info['keywords'])
        therapeutic_goals = ', '.join(theme_info['therapeutic_goals'])
        
        prompt = f"""
You are an expert therapeutic storyteller specializing in mental wellness narratives for Indian youth. 
Create an engaging, culturally relevant story that promotes healing and growth.

**Story Requirements:**
- Theme: {theme_info['description']}
- Main Character: {character_name} (aged {character_age})
- Setting: {setting_context}
- Length: {length_info['word_count']} ({length_info['reading_time']})
- Structure: {length_info['structure']}

**Therapeutic Goals:**
- {therapeutic_goals}

**Age-Appropriate Context:**
- {age_context}

**Specific Challenge/Situation:**
{challenge if challenge else 'Create an appropriate challenge that fits the theme and age group'}

**Cultural Context:**
- Include relevant Indian cultural elements, values, and family dynamics
- Use relatable settings and situations for Indian youth
- Incorporate positive role models and support systems
- Show respect for family relationships and cultural traditions

**Key Elements to Include:**
- Keywords: {keywords}
- Clear character growth and learning
- Realistic dialogue and emotions
- Practical coping strategies or insights
- Hope and empowerment
- Healthy relationship dynamics

**Story Structure:**
1. **Introduction:** Establish character, setting, and initial situation
2. **Challenge:** Present the main obstacle or emotional difficulty
3. **Journey:** Show the character's struggles, attempts, and learning process
4. **Growth:** Demonstrate character development and new understanding
5. **Resolution:** Conclude with positive change and hope for the future

**Writing Style:**
- Engaging and age-appropriate language
- Vivid descriptions that create emotional connection
- Natural dialogue that feels authentic
- Balance between realism and hope
- Include sensory details and emotional depth

Create a story that readers can relate to and learn from, showing that challenges are opportunities for growth and that seeking help is a sign of strength.
"""
        
        return prompt

    def _create_reflection_prompt(self, theme: str, theme_info: Dict, story_content: str) -> str:
        """Create a prompt for generating reflection questions"""
        
        therapeutic_goals = ', '.join(theme_info['therapeutic_goals'])
        
        prompt = f"""
Based on the therapeutic story provided, create meaningful reflection questions that help readers:
- {therapeutic_goals}
- Connect the story to their own experiences
- Process emotions and insights
- Develop practical coping strategies

**Story Content:**
{story_content[:1000]}...

**Create 4-6 reflection questions that:**
1. Help readers identify with the character's journey
2. Encourage self-reflection about similar experiences
3. Promote practical application of story lessons
4. Support emotional processing and growth
5. Encourage seeking support when needed

**Format the questions as:**
- Personal connection questions (How does this relate to your life?)
- Insight questions (What did the character learn?)
- Application questions (How can you use this in your life?)
- Support questions (Who could help you in similar situations?)

Make the questions thoughtful, non-judgmental, and empowering. Use language that feels supportive and encouraging.
"""
        
        return prompt

    def _format_story_content(self, story_text: str) -> str:
        """Format the story content for better readability"""
        # Clean up the text and add proper paragraph breaks
        paragraphs = story_text.strip().split('\n\n')
        formatted_paragraphs = []
        
        for paragraph in paragraphs:
            if paragraph.strip():
                formatted_paragraphs.append(f"<p>{paragraph.strip()}</p>")
        
        return '\n'.join(formatted_paragraphs)

    def _format_reflection_questions(self, reflection_text: str) -> str:
        """Format reflection questions for better presentation"""
        # Split into individual questions and format as a list
        lines = reflection_text.strip().split('\n')
        questions = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('1.') or line.startswith('-') or line.startswith('•') or '?' in line):
                # Clean up question formatting
                question = line.lstrip('1234567890.-•').strip()
                if question and '?' in question:
                    questions.append(f"<li>{question}</li>")
        
        if questions:
            return f"<ul>{''.join(questions)}</ul>"
        else:
            # Fallback formatting
            return f"<p>{reflection_text}</p>"

    def _generate_character_name(self) -> str:
        """Generate a culturally appropriate character name"""
        indian_names = [
            'Arjun', 'Priya', 'Rahul', 'Kavya', 'Aditya', 'Meera', 'Vikram', 'Anaya',
            'Rohan', 'Isha', 'Karthik', 'Shreya', 'Aryan', 'Diya', 'Nikhil', 'Riya',
            'Aarav', 'Saanvi', 'Vivaan', 'Avni', 'Vihaan', 'Sara', 'Ayaan', 'Myra'
        ]
        return random.choice(indian_names)

    def _get_fallback_story(self, theme: str) -> str:
        """Provide a fallback story if generation fails"""
        fallback_stories = {
            'overcoming_anxiety': """
            <p>Priya stood at the entrance of her new college, her heart racing with familiar anxiety. The building seemed enormous, filled with hundreds of strangers.</p>
            <p>Taking a deep breath, she remembered her counselor's advice: "Anxiety is not your enemy—it's your mind trying to protect you. Acknowledge it, thank it, and take one small step forward."</p>
            <p>She walked to the registration desk, introduced herself to another nervous-looking student, and discovered they shared the same major. By the end of the day, Priya had made her first friend and realized that courage isn't the absence of fear—it's feeling the fear and moving forward anyway.</p>
            """,
            'building_confidence': """
            <p>Arjun had always believed he wasn't good at anything special. His friends excelled in sports, academics, or music, while he felt ordinary.</p>
            <p>When his school announced a storytelling competition, something sparked inside him. He loved creating stories but had never shared them with anyone.</p>
            <p>Despite his doubts, Arjun decided to participate. His story about a young boy discovering his unique gift resonated with the audience. He didn't win first place, but the applause and genuine compliments showed him that his voice mattered. Sometimes, our greatest strength lies in what makes us different.</p>
            """
        }
        
        return fallback_stories.get(theme, "<p>A story of growth, resilience, and hope is waiting to be told. Every challenge is an opportunity to discover your inner strength.</p>")

    def get_available_themes(self) -> Dict[str, str]:
        """Return available therapeutic themes and their descriptions"""
        return {theme: info['description'] for theme, info in self.therapeutic_themes.items()}

    def get_theme_suggestions(self, emotion: str) -> List[str]:
        """Suggest themes based on detected emotion"""
        emotion_to_themes = {
            'anxious': ['overcoming_anxiety', 'managing_stress', 'building_confidence'],
            'sad': ['emotional_healing', 'friendship_support', 'self_discovery'],
            'angry': ['managing_stress', 'emotional_healing', 'resilience_growth'],
            'stressed': ['managing_stress', 'overcoming_anxiety', 'goal_achievement'],
            'lonely': ['friendship_support', 'family_relationships', 'self_discovery'],
            'confused': ['self_discovery', 'goal_achievement', 'family_relationships'],
            'overwhelmed': ['managing_stress', 'resilience_growth', 'overcoming_anxiety']
        }
        
        return emotion_to_themes.get(emotion.lower(), ['self_discovery', 'resilience_growth', 'building_confidence'])