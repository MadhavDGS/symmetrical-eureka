"""
Bollywood Music Therapy Integration
Mood-based Bollywood song recommendations for mental wellness
"""

class BollywoodMusicTherapy:
    def __init__(self):
        self.bollywood_playlists = {
            'happy': {
                'title': 'खुशी के गाने (Happy Songs)',
                'description': 'Feel-good Bollywood tracks to boost your mood',
                'playlists': [
                    {
                        'name': 'Latest Bollywood Dance Hits',
                        'description': 'नवीनतम बॉलीवुड डांस हिट्स',
                        'songs': [
                            'Kesariya - Brahmastra', 'Raataan Lambiyan - Shershaah',
                            'Mann Mera - Table No. 21', 'Sooraj Dooba Hain - Roy',
                            'Nagada Sang Dhol - Ramleela', 'Jai Ho - Slumdog Millionaire',
                            'Dil Se Re - Dil Se', 'Bhangra Paale - Force'
                        ],
                        'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX0XiuGLJVUZl',
                        'youtube_url': 'https://youtube.com/playlist?list=PLjjV8mYP1bJYz_jJ5q7_pEYrKRQ3W3q9p',
                        'gaana_url': 'https://gaana.com/playlist/bollywood-happy-hits'
                    },
                    {
                        'name': 'Classic Bollywood Joy',
                        'description': 'पुराने खुशी के गाने',
                        'songs': [
                            'Yeh Jo Des Hai Tera - Swades', 'Mere Sapno Ki Rani - Aradhana',
                            'Aaj Phir Jeene Ki - Guide', 'Dekha Ek Khwab - Silsila',
                            'Jeena Yahan Marna Yahan - Mera Naam Joker',
                            'Main Hoon Hero Tera - Hero', 'Tumhi Dekho Na - Kabhi Alvida Na Kehna'
                        ],
                        'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX7jFE0xNlqvJ',
                        'youtube_url': 'https://youtube.com/playlist?list=PLjjV8mYP1bJYz_classic_happy'
                    }
                ]
            },
            
            'sad': {
                'title': 'दुःख भरे गाने (Sad Songs)',
                'description': 'Emotional Bollywood tracks for healing and processing emotions',
                'playlists': [
                    {
                        'name': 'Heart-touching Bollywood',
                        'description': 'दिल को छूने वाले गाने',
                        'songs': [
                            'Agar Tum Saath Ho - Tamasha', 'Ae Dil Hai Mushkil - Ae Dil Hai Mushkil',
                            'Khairiyat - Chhichhore', 'Tum Hi Ho - Aashiqui 2',
                            'Dil Diyan Gallan - Tiger Zinda Hai', 'Hamari Adhuri Kahani - Hamari Adhuri Kahani',
                            'Tere Bina - Guru', 'Phir Mohabbat - Murder 2'
                        ],
                        'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX59NCqCqJtoH',
                        'youtube_url': 'https://youtube.com/playlist?list=PLjjV8mYP1bJYz_sad_bollywood'
                    },
                    {
                        'name': 'Vintage Bollywood Melancholy',
                        'description': 'पुराने दुखी गाने',
                        'songs': [
                            'Lag Ja Gale - Woh Kaun Thi', 'Hothon Se Chu Lo Tum - Prem Geet',
                            'Raina Beeti Jaye - Amar Prem', 'Kahin Door Jab - Anand',
                            'Yeh Vaada Raha - Tina Munim', 'Tere Bina Zindagi Se - Aandhi'
                        ],
                        'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX7K31D69s4M1',
                        'youtube_url': 'https://youtube.com/playlist?list=PLjjV8mYP1bJYz_vintage_sad'
                    }
                ]
            },
            
            'anxious': {
                'title': 'शांति के गाने (Peaceful Songs)',
                'description': 'Calming Bollywood tracks to reduce anxiety and stress',
                'playlists': [
                    {
                        'name': 'Spiritual & Sufi Bollywood',
                        'description': 'आध्यात्मिक और सूफी गाने',
                        'songs': [
                            'Kun Faya Kun - Rockstar', 'Allah Ke Bande - Khatarnak',
                            'Ishq Sufiyana - The Dirty Picture', 'Tu Hi Re - Bombay',
                            'Arziyan - Delhi 6', 'Chaap Tilak - Delhi 6',
                            'Shiv Tandav - various', 'Allah Hoo - various'
                        ],
                        'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX2Nc3B70tvx0',
                        'youtube_url': 'https://youtube.com/playlist?list=PLjjV8mYP1bJYz_sufi_bollywood'
                    },
                    {
                        'name': 'Devotional Bollywood',
                        'description': 'भक्ति गीत',
                        'songs': [
                            'Om Jai Jagdish Hare - various', 'Vande Mataram - various',
                            'Raghupati Raghav - Kuch Kuch Hota Hai', 'Piyu Bole - Parineeta',
                            'Bhajan songs from movies'
                        ],
                        'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DWZqd5JICZI0u'
                    }
                ]
            },
            
            'calm': {
                'title': 'प्रेम के गाने (Romantic Calm)',
                'description': 'Soft romantic Bollywood songs for tranquility',
                'playlists': [
                    {
                        'name': 'Romantic Slow Bollywood',
                        'description': 'धीमे प्रेम गीत',
                        'songs': [
                            'Tum Mile - Tum Mile', 'Jeene Laga Hoon - Ramaiya Vastavaiya',
                            'Pehla Nasha - Jo Jeeta Wohi Sikandar', 'Tujh Mein Rab Dikhta Hai - Rab Ne Bana Di Jodi',
                            'Raabta - Agent Vinod', 'Gerua - Dilwale',
                            'Tujhe Kitna Chahne Lage - Kabir Singh'
                        ],
                        'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX0bblH6Z2sZ7',
                        'youtube_url': 'https://youtube.com/playlist?list=PLjjV8mYP1bJYz_romantic_slow'
                    },
                    {
                        'name': 'AR Rahman Peaceful Collection',
                        'description': 'ए.आर. रहमान के शांत गाने',
                        'songs': [
                            'Vande Mataram - Vande Mataram', 'Maa Tujhe Salaam - Vande Mataram',
                            'Noor-Un-Ala Noor - Meenaxi', 'Pray for Me Brother - The Legend of Bhagat Singh',
                            'Infinite Love - Raavan'
                        ],
                        'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DWY7RSRVO2Q7U'
                    }
                ]
            },
            
            'focused': {
                'title': 'पढ़ाई के गाने (Study Music)',
                'description': 'Instrumental and focus-enhancing Bollywood music',
                'playlists': [
                    {
                        'name': 'Bollywood Instrumental Focus',
                        'description': 'बॉलीवुड वाद्य संगीत',
                        'songs': [
                            'Background scores from movies', 'Classical Indian fusion',
                            'Instrumental versions of popular songs', 'Movie theme music',
                            'Sitar and tabla compositions', 'Flute melodies from films'
                        ],
                        'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0',
                        'youtube_url': 'https://youtube.com/playlist?list=PLjjV8mYP1bJYz_instrumental'
                    },
                    {
                        'name': 'Indian Classical for Focus',
                        'description': 'एकाग्रता के लिए शास्त्रीय संगीत',
                        'songs': [
                            'Raga Yaman compositions', 'Raga Bhairavi melodies',
                            'Tabla & Sitar classical', 'Flute compositions',
                            'Classical fusion tracks'
                        ],
                        'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX4bmKe1x8uP9'
                    }
                ]
            },
            
            'motivated': {
                'title': 'जोश भरे गाने (Motivational Songs)',
                'description': 'High-energy Bollywood tracks for motivation and confidence',
                'playlists': [
                    {
                        'name': 'Bollywood Power Anthems',
                        'description': 'शक्ति देने वाले गाने',
                        'songs': [
                            'Malhari - Bajirao Mastani', 'Seeti Maar - Radhe',
                            'Jai Jai Shivshankar - War', 'Sher Aaya Sher - Gully Boy',
                            'Dangal - Dangal', 'Sultan - Sultan',
                            'Chak De India - Chak De India', 'Zinda Hai Hum - Zinda'
                        ],
                        'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX0pH0SHskOcz',
                        'youtube_url': 'https://youtube.com/playlist?list=PLjjV8mYP1bJYz_motivational'
                    },
                    {
                        'name': 'Patriotic Bollywood Motivation',
                        'description': 'देशभक्ति के प्रेरणादायक गाने',
                        'songs': [
                            'Vande Mataram - various versions', 'Ae Watan - Raazi',
                            'Maa Tujhe Salaam - Vande Mataram', 'Bharat Mata - various',
                            'Des Rangila - Fanaa', 'Sandese Aate Hai - Border'
                        ],
                        'spotify_url': 'https://open.spotify.com/playlist/37i9dQZF1DX1EBuotBhhgr'
                    }
                ]
            }
        }
        
        # Mood-specific therapy benefits in Hindi/English
        self.mood_benefits = {
            'happy': {
                'title': 'खुशी के फायदे (Benefits of Happy Music)',
                'benefits': [
                    'Releases endorphins and serotonin (खुशी के हार्मोन निकालता है)',
                    'Reduces stress and anxiety levels (तनाव और चिंता कम करता है)',
                    'Improves social connections (सामाजिक संबंध बेहतर बनाता है)',
                    'Boosts energy and motivation (ऊर्जा और प्रेरणा बढ़ाता है)'
                ]
            },
            'sad': {
                'title': 'दुःख प्रसंस्करण के फायदे (Benefits of Processing Sadness)',
                'benefits': [
                    'Helps process and release emotions (भावनाओं को समझने में मदद)',
                    'Provides emotional catharsis (भावनात्मक शुद्धिकरण)',
                    'Validates feelings and experiences (भावनाओं को मान्यता)',
                    'Promotes healing and acceptance (उपचार और स्वीकृति)'
                ]
            },
            'anxious': {
                'title': 'शांति के फायदे (Benefits of Calming Music)',
                'benefits': [
                    'Lowers heart rate and blood pressure (हृदय गति धीमी करता है)',
                    'Reduces cortisol stress hormone (तनाव हार्मोन कम करता है)',
                    'Promotes deep breathing (गहरी सांस लेने में मदद)',
                    'Activates parasympathetic nervous system (शांति तंत्र सक्रिय करता है)'
                ]
            },
            'calm': {
                'title': 'शांत संगीत के फायदे (Benefits of Peaceful Music)',
                'benefits': [
                    'Improves sleep quality (नींद की गुणवत्ता बेहतर)',
                    'Enhances meditation and mindfulness (ध्यान में सुधार)',
                    'Reduces mental chatter (मानसिक शोर कम करता है)',
                    'Promotes inner peace (आंतरिक शांति बढ़ाता है)'
                ]
            },
            'focused': {
                'title': 'एकाग्रता संगीत के फायदे (Benefits of Focus Music)',
                'benefits': [
                    'Improves concentration and attention (एकाग्रता बढ़ाता है)',
                    'Enhances cognitive performance (मानसिक प्रदर्शन सुधारता है)',
                    'Reduces distractions (विकर्षण कम करता है)',
                    'Boosts productivity (उत्पादकता बढ़ाता है)'
                ]
            },
            'motivated': {
                'title': 'प्रेरणादायक संगीत के फायदे (Benefits of Motivational Music)',
                'benefits': [
                    'Increases dopamine levels (प्रेरणा हार्मोन बढ़ाता है)',
                    'Boosts confidence and self-esteem (आत्मविश्वास बढ़ाता है)',
                    'Enhances physical performance (शारीरिक प्रदर्शन सुधारता है)',
                    'Promotes goal achievement (लक्ष्य प्राप्ति में मदद)'
                ]
            }
        }
    
    def get_mood_playlists(self, mood):
        """Get Bollywood playlists for a specific mood"""
        if mood in self.bollywood_playlists:
            return self.bollywood_playlists[mood]
        return self.bollywood_playlists['calm']  # Default fallback
    
    def get_mood_benefits(self, mood):
        """Get therapeutic benefits for a specific mood"""
        if mood in self.mood_benefits:
            return self.mood_benefits[mood]
        return self.mood_benefits['calm']  # Default fallback
    
    def get_random_song_recommendation(self, mood):
        """Get a random song recommendation for mood"""
        import random
        mood_data = self.get_mood_playlists(mood)
        if mood_data and mood_data['playlists']:
            random_playlist = random.choice(mood_data['playlists'])
            if random_playlist['songs']:
                random_song = random.choice(random_playlist['songs'])
                return {
                    'song': random_song,
                    'playlist': random_playlist['name'],
                    'mood_title': mood_data['title']
                }
        return None
    
    def search_bollywood_song_by_emotion(self, emotion_keywords):
        """Search for Bollywood songs based on emotion keywords"""
        emotion_mapping = {
            'खुशी': 'happy', 'happy': 'happy', 'joy': 'happy', 'celebration': 'happy',
            'दुःख': 'sad', 'sad': 'sad', 'heartbreak': 'sad', 'melancholy': 'sad',
            'चिंता': 'anxious', 'anxious': 'anxious', 'worry': 'anxious', 'stress': 'anxious',
            'शांति': 'calm', 'calm': 'calm', 'peace': 'calm', 'romantic': 'calm',
            'एकाग्रता': 'focused', 'focus': 'focused', 'study': 'focused', 'concentration': 'focused',
            'प्रेरणा': 'motivated', 'motivation': 'motivated', 'energy': 'motivated', 'power': 'motivated'
        }
        
        for keyword in emotion_keywords:
            if keyword.lower() in emotion_mapping:
                mood = emotion_mapping[keyword.lower()]
                return self.get_mood_playlists(mood)
        
        return self.get_mood_playlists('calm')  # Default fallback