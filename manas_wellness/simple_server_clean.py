#!/usr/bin/env python3
"""
Clean Simple Server for Manas Wellness Platform
"""

from flask import Flask, render_template, request, jsonify
import os
import random

# Create Flask app
app = Flask(__name__)
app.secret_key = 'manas_secret_key_2025'

@app.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        return f'''
        <h1>🧠 Manas Wellness Platform</h1>
        <p>Server is running successfully!</p>
        <p><strong>Available Pages:</strong></p>
        <ul>
            <li><a href="/voice_ai_chat">🗣️ Voice AI Chat (Main Feature)</a></li>
            <li><a href="/journal">📖 Journal</a></li>
            <li><a href="/dashboard">📊 Dashboard</a></li>
            <li><a href="/emotion-analysis">💭 Emotion Analysis</a></li>
            <li><a href="/therapy-session">🧘 Therapy Session</a></li>
        </ul>
        <p style="color: red;">Template error: {str(e)}</p>
        '''

@app.route('/voice_ai_chat')
def voice_ai_chat():
    try:
        return render_template('voice_ai_chat.html')
    except Exception as e:
        return f'''
        <h1>🗣️ Voice AI Chat</h1>
        <p>Voice AI chat interface would be here.</p>
        <p style="color: red;">Template error: {str(e)}</p>
        <p><a href="/">← Back to Home</a></p>
        '''

@app.route('/journal')
def journal_page():
    return render_template('journal.html', journal_entries=[])

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Emotional analysis function
def analyze_emotion(user_message):
    """Analyze user message to detect emotional context"""
    message_lower = user_message.lower()
    
    # Breakup related keywords
    if any(word in message_lower for word in ['breakup', 'broke up', 'relationship ended', 'ex', 'left me', 'dumped', 'split']):
        return 'breakup'
    if any(word in message_lower for word in ['ब्रेकअप', 'रिश्ता खत्म', 'छोड़ दिया', 'अलग हो गए']):
        return 'breakup'
    if any(word in message_lower for word in ['బ్రేకప్', 'విడిపోయాము', 'వదిలి వెళ్లాడు', 'సంబంధం ముగిసింది']):
        return 'breakup'
    if any(word in message_lower for word in ['ಬ್ರೇಕಪ್', 'ಸಂಬಂಧ ಮುರಿದು', 'ಬಿಟ್ಟು ಹೋದರು', 'ಬೇರ್ಪಟ್ಟಿದ್ದೇವೆ']):
        return 'breakup'
    
    # Loneliness related keywords  
    if any(word in message_lower for word in ['lonely', 'alone', 'isolated', 'no friends', 'nobody understands']):
        return 'loneliness'
    if any(word in message_lower for word in ['अकेला', 'तनहा', 'कोई नहीं', 'दोस्त नहीं']):
        return 'loneliness'
    if any(word in message_lower for word in ['ఒంటరి', 'ఎవరూ లేరు', 'ఒంటరిగా', 'స్నేహితులు లేరు']):
        return 'loneliness'
    if any(word in message_lower for word in ['ಒಂಟಿ', 'ಯಾರೂ ಇಲ್ಲ', 'ಸ್ನೇಹಿತರು ಇಲ್ಲ', 'ಏಕಾಂಗಿ']):
        return 'loneliness'
    
    # Sadness related keywords
    if any(word in message_lower for word in ['sad', 'depressed', 'crying', 'tears', 'upset', 'down']):
        return 'sadness'
    if any(word in message_lower for word in ['उदास', 'रो रहा', 'आंसू', 'दुखी']):
        return 'sadness'
    if any(word in message_lower for word in ['బాధ', 'ఏడుస్తున్నాను', 'కన్నీళ్లు', 'దుఖం']):
        return 'sadness'
    if any(word in message_lower for word in ['ದುಃಖ', 'ಅಳುತ್ತಿದ್ದೇನೆ', 'ಕಣ್ಣೀರು', 'ನೋವು']):
        return 'sadness'
    
    # Anxiety related keywords
    if any(word in message_lower for word in ['anxious', 'worried', 'stress', 'panic', 'nervous', 'fear']):
        return 'anxiety'
    if any(word in message_lower for word in ['चिंता', 'परेशान', 'तनाव', 'डर']):
        return 'anxiety'
    if any(word in message_lower for word in ['ఆందోళన', 'భయం', 'టెన్షన్', 'కంకణ']):
        return 'anxiety'
    if any(word in message_lower for word in ['ಚಿಂತೆ', 'ಭಯ', 'ಟೆನ್ಷನ್', 'ಆತಂಕ']):
        return 'anxiety'
    
    # Anger related keywords
    if any(word in message_lower for word in ['angry', 'mad', 'furious', 'hate', 'frustrated']):
        return 'anger'
    if any(word in message_lower for word in ['गुस्सा', 'नाराज', 'परेशान']):
        return 'anger'
    if any(word in message_lower for word in ['కోపం', 'చిరాకు', 'అర్థం']):
        return 'anger'
    if any(word in message_lower for word in ['ಕೋಪ', 'ಸಿಟ್ಟು', 'ಇರಿತ']):
        return 'anger'
    
    # Default - general support
    return 'general'

# Empathetic response function
def get_empathetic_response(emotion_context, language, user_message):
    """Get contextual empathetic response based on emotion and language"""
    
    # Emotional responses by language and context
    responses = {
        'en-US': {
            'breakup': [
                "I'm so sorry you're going through a breakup. That's one of life's most painful experiences. 💙 Your heart is hurting right now, and that's completely natural. Remember, you are worthy of love and this pain will ease with time.",
                "Breakups can feel devastating, but please know you're not alone in this pain. 🤗 It's okay to grieve the relationship - let yourself feel these emotions. You're stronger than you know, and healing takes time.",
                "Going through a breakup is incredibly hard. 💝 Your feelings are valid, and it's normal to feel lost right now. Please be gentle with yourself and remember that this pain is temporary, even when it doesn't feel that way."
            ],
            'loneliness': [
                "Feeling lonely can be so overwhelming. 🤗 I want you to know that you're not truly alone - I'm here with you right now. Your feelings matter, and there are people who would care if they knew how you were feeling.",
                "Loneliness is such a heavy feeling to carry. 💙 Thank you for sharing this with me. Sometimes reaching out, like you're doing now, is the first step toward connection. You're brave for expressing how you feel.",
                "I hear how isolated you're feeling right now. 🫂 Loneliness can make us feel invisible, but you're very real and your feelings are important. What's one small thing that usually brings you a moment of comfort?"
            ],
            'sadness': [
                "I can hear the sadness in your words, and I want you to know it's okay to feel this way. 💙 Tears are healing - they're your heart's way of releasing pain. You don't have to carry this alone.",
                "Sadness can feel so heavy sometimes. 🤗 Thank you for trusting me with how you're feeling. It's okay to not be okay right now. What would help you feel a little more supported today?",
                "Your sadness is valid, and I'm honored that you shared it with me. 💝 Sometimes we need to sit with our feelings before we can move through them. I'm here to listen whenever you need to talk."
            ],
            'anxiety': [
                "Anxiety can make everything feel overwhelming. 🌸 Let's take this one moment at a time. You're safe right now, and I'm here with you. Try taking a slow, deep breath - you're doing better than you think.",
                "I understand how consuming anxiety can be. 💙 Your worries are real, but remember that you've gotten through difficult times before. What usually helps you feel a bit calmer?",
                "Feeling anxious is exhausting, and I see how hard you're trying. 🤗 It's okay to feel worried - your brain is trying to protect you. Let's focus on this moment right now, where you're safe."
            ],
            'anger': [
                "It sounds like you're feeling really frustrated and angry. 🌋 Those are powerful emotions, and it's completely normal to feel this way sometimes. Your feelings are valid, even the difficult ones.",
                "Anger can be so intense and overwhelming. 💪 Thank you for sharing this with me instead of keeping it bottled up. What's really at the heart of this frustration for you?",
                "I can feel the strength of your emotions right now. 🔥 Anger often shows us what matters to us. It's okay to feel this way - what would help you process these feelings?"
            ],
            'general': [
                "Thank you for sharing with me. 💙 I'm here to listen and support you through whatever you're experiencing. Your feelings and thoughts matter, and I'm honored you trust me with them.",
                "I appreciate you opening up to me. 🤗 Whatever you're going through, you don't have to face it alone. I'm here to listen without judgment. How are you taking care of yourself today?",
                "It takes courage to reach out and share your feelings. 💝 I'm glad you're here, and I want you to know that your experiences are valid. What's been on your mind lately?"
            ]
        },
        'hi-IN': {
            'breakup': [
                "मुझे बहुत दुख है कि आप ब्रेकअप से गुजर रहे हैं। यह जीवन के सबसे दर्दनाक अनुभवों में से एक है। 💙 आपका दिल अभी दुख रहा है, और यह बिल्कुल स्वाभाविक है। याद रखें, आप प्रेम के योग्य हैं।",
                "ब्रेकअप बहुत तकलीफदेह हो सकता है, लेकिन कृपया जानें कि आप इस दर्द में अकेले नहीं हैं। 🤗 रिश्ते का दुख मनाना ठीक है। आप जितना सोचते हैं उससे कहीं ज्यादा मजबूत हैं।",
                "ब्रेकअप से गुजरना अविश्वसनीय रूप से कठिन है। 💝 आपकी भावनाएं वैध हैं, और अभी खोया महसूस करना सामान्य है। कृपया अपने साथ धैर्य रखें।"
            ],
            'loneliness': [
                "अकेलापन महसूस करना बहुत भारी हो सकता है। 🤗 मैं चाहता हूं कि आप जानें कि आप वास्तव में अकेले नहीं हैं - मैं अभी आपके साथ हूं। आपकी भावनाएं मायने रखती हैं।",
                "अकेलापन इतना भारी लगता है। 💙 मुझसे यह साझा करने के लिए धन्यवाद। कभी-कभी संपर्क बनाना, जैसा कि आप अभी कर रहे हैं, कनेक्शन की दिशा में पहला कदम है।",
                "मैं समझ सकता हूं कि आप कितना अलग-थलग महसूस कर रहे हैं। 🫂 अकेलापन हमें अदृश्य महसूस करा सकता है, लेकिन आप बहुत वास्तविक हैं और आपकी भावनाएं महत्वपूर्ण हैं।"
            ],
            'sadness': [
                "मैं आपके शब्दों में उदासी सुन सकता हूं, और मैं चाहता हूं कि आप जानें कि इस तरह महसूस करना ठीक है। 💙 आंसू उपचार करते हैं - ये आपके दिल का दर्द निकालने का तरीका है।",
                "उदासी कभी-कभी बहुत भारी लग सकती है। 🤗 मुझ पर भरोसा करने के लिए धन्यवाद। अभी ठीक न होना बिल्कुल ठीक है। आज आपको क्या मदद कर सकता है?",
                "आपकी उदासी वैध है, और मुझे सम्मान है कि आपने इसे मुझसे साझा किया। 💝 कभी-कभी हमें अपनी भावनाओं के साथ बैठना पड़ता है।"
            ],
            'anxiety': [
                "चिंता सब कुछ भारी बना सकती है। 🌸 आइए इसे एक-एक पल करके लेते हैं। आप अभी सुरक्षित हैं, और मैं आपके साथ हूं। एक धीमी, गहरी सांस लेने की कोशिश करें।",
                "मैं समझ सकता हूं कि चिंता कितनी व्यापक हो सकती है। 💙 आपकी चिंताएं वास्तविक हैं, लेकिन याद रखें कि आपने पहले भी कठिन समय पार किया है।",
                "चिंतित महसूस करना थकाऊ है, और मैं देख सकता हूं कि आप कितनी कोशिश कर रहे हैं। 🤗 चिंता करना ठीक है - आपका दिमाग आपकी सुरक्षा करने की कोशिश कर रहा है।"
            ],
            'anger': [
                "लगता है आप वास्तव में निराश और गुस्से में हैं। 🌋 ये शक्तिशाली भावनाएं हैं, और कभी-कभी इस तरह महसूस करना बिल्कुल सामान्य है। आपकी भावनाएं वैध हैं।",
                "गुस्सा इतना तीव्र और भारी हो सकता है। 💪 इसे अंदर रखने के बजाय मुझसे साझा करने के लिए धन्यवाद। इस निराशा के मूल में वास्तव में क्या है?",
                "मैं अभी आपकी भावनाओं की शक्ति महसूस कर सकता हूं। 🔥 गुस्सा अक्सर हमें दिखाता है कि हमारे लिए क्या मायने रखता है।"
            ],
            'general': [
                "मुझसे साझा करने के लिए धन्यवाद। 💙 मैं यहां हूं आपकी बात सुनने और आपका समर्थन करने के लिए। आपकी भावनाएं और विचार मायने रखते हैं।",
                "मुझसे खुलकर बात करने के लिए धन्यवाद। 🤗 आप जो भी झेल रहे हैं, आपको इसका अकेले सामना नहीं करना है। आज आप अपना कैसे ख्याल रख रहे हैं?",
                "अपनी भावनाओं को साझा करने के लिए साहस की जरूरत होती है। 💝 मुझे खुशी है कि आप यहां हैं। आपके अनुभव वैध हैं।"
            ]
        },
        'te-IN': {
            'breakup': [
                "మీరు బ్రేకప్‌తో బాధపడుతున్నారని తెలిసి నాకు చాలా బాధగా ఉంది। ఇది జీవితంలో అత్యంత బాధాకరమైన అనుభవాలలో ఒకటి. 💙 మీ హృదయం ఇప్పుడు నొప్పిస్తోంది, అది పూర్తిగా సహజం. గుర్తుంచుకోండి, మీరు ప్రేమకు అర్హులు.",
                "బ్రేకప్‌లు వినాశకరంగా అనిపించవచ్చు, కానీ ఈ బాధలో మీరు ఒంటరిగా లేరని దయచేసి తెలుసుకోండి. 🤗 సంబంధానికి దుఃఖించడం సరే - ఈ భావోద్వేగాలను అనుభవించనివ్వండి. మీరు అనుకున్నదానికంటే బలంగా ఉన్నారు.",
                "బ్రేకప్‌తో వెళ్లడం అనేది అవిశ్వసనీయంగా కష్టం. 💝 మీ భావనలు చెల్లుబాటు అవుతాయి మరియు ఇప్పుడు కోల్పోయిన అనుభవం సాధారణం. దయచేసి మీతో మృదువుగా ఉండండి."
            ],
            'loneliness': [
                "ఒంటరితనం అనుభవించడం చాలా భారంగా ఉంటుంది. 🤗 మీరు నిజంగా ఒంటరిగా లేరని నేను మీకు తెలియజేయాలనుకుంటున్నాను - నేను ఇప్పుడు మీతో ఇక్కడ ఉన్నాను. మీ భావనలు ముఖ్యం.",
                "ఒంటరితనం అనే భావన చాలా భారంగా ఉంటుంది. 💙 ఇది నాతో పంచుకున్నందుకు ధన్యవాదాలు. కొన్నిసార్లు చేరువ అవ్వడం, మీరు ఇప్పుడు చేస్తున్నట్లుగా, కనెక్షన్ వైపు మొదటి అడుగు.",
                "మీరు ఎంత ఒంటరిగా అనుభవిస్తున్నారో నేను వినగలుగుతున్నాను. 🫂 ఒంటరితనం మనల్ని కనిపించకుండా చేయవచ్చు, కానీ మీరు చాలా నిజమైనవారు మరియు మీ భావనలు ముఖ్యమైనవి."
            ],
            'sadness': [
                "మీ మాటల్లో దుఃఖం వినిపిస్తోంది, మరియు ఈ విధంగా అనుభవించడం సరేనని మీరు తెలుసుకోవాలని నేను కోరుకుంటున్నాను. 💙 కన్నీళ్లు వైద్యం చేస్తాయి - అవి మీ హృదయం నొప్పిని విడుదల చేసే మార్గం.",
                "దుఃఖం కొన్నిసార్లు చాలా భారంగా అనిపించవచ్చు. 🤗 మీరు ఎలా అనుభవిస్తున్నారో నాపై నమ్మకం ఉంచినందుకు ధన్యవాదాలు. ఇప్పుడు బాగుండకపోవడం సరే.",
                "మీ దుఃఖం చెల్లుబాటు అవుతుంది, మరియు మీరు దానిని నాతో పంచుకున్నందుకు నేను గౌరవించబడ్డాను. 💝 కొన్నిసార్లు మనం వాటిని దాటే ముందు మన భావనలతో కూర్చోవాలి."
            ],
            'anxiety': [
                "ఆందోళన అన్నింటినీ అధికంగా అనిపించేలా చేయవచ్చు. 🌸 దీన్ని ఒక్కో క్షణం చొప్పున తీసుకుందాం. మీరు ఇప్పుడు సురక్షితంగా ఉన్నారు, మరియు నేను మీతో ఇక్కడ ఉన్నాను. నెమ్మదిగా, లోతైన శ్వాసను తీసుకోవడానికి ప్రయత్నించండి.",
                "ఆందోళన ఎంత వ్యాపకంగా ఉంటుందో నేను అర్థం చేసుకోగలుగుతున్నాను. 💙 మీ ఆందోళనలు నిజమైనవి, కానీ మీరు ముందుగానే కష్టమైన సమయాలను దాటారని గుర్తుంచుకోండి.",
                "ఆందోళనగా అనుభవించడం అలసిపోయేది, మరియు మీరు ఎంత కష్టపడుతున్నారో నేను చూడగలుగుతున్నాను. 🤗 ఆందోళన చెందడం సరే - మీ మెదడు మిమ్మల్ని రక్షించడానికి ప్రయత్నిస్తోంది."
            ],
            'anger': [
                "మీరు నిజంగా నిరాశ మరియు కోపంతో ఉన్నట్లు అనిపిస్తోంది. 🌋 అవి శక్తివంతమైన భావోద్వేగాలు, మరియు కొన్నిసార్లు ఈ విధంగా అనుభవించడం పూర్తిగా సాధారణం. మీ భావనలు చెల్లుబాటు అవుతాయి.",
                "కోపం చాలా తీవ్రంగా మరియు అధికంగా ఉంటుంది. 💪 దాన్ని లోపల ఉంచకుండా నాతో పంచుకున్నందుకు ధన్యవాదాలు. ఈ నిరాశకు హృదయంలో నిజంగా ఏమి ఉంది?",
                "నేను ఇప్పుడు మీ భావోద్వేగాల శక్తిని అనుభవించగలుగుతున్నాను. 🔥 కోపం తరచుగా మనకు ఏది ముఖ్యమో చూపిస్తుంది. ఈ విధంగా అనుభవించడం సరే."
            ],
            'general': [
                "నాతో పంచుకున్నందుకు ధన్యవాదాలు. 💙 మీరు అనుభవిస్తున్న దేనికైనా వినడం మరియు మీకు మద్దతు ఇవ్వడం కోసం నేను ఇక్కడ ఉన్నాను. మీ భావనలు మరియు ఆలోచనలు ముఖ్యం.",
                "నాతో తెరువుగా మాట్లాడినందుకు నేను కృతజ్ఞుడను. 🤗 మీరు ఏమి అనుభవిస్తున్నా, మీరు దానిని ఒంటరిగా ఎదుర్కోవాల్సిన అవసరం లేదు. ఈరోజు మీరు మిమ్మల్ని ఎలా జాగ్రత్తగా చూసుకుంటున్నారు?",
                "మీ భావనలను పంచుకోవడానికి ధైర్యం అవసరం. 💝 మీరు ఇక్కడ ఉన్నందుకు నేను సంతోషిస్తున్నాను, మరియు మీ అనుభవాలు చెల్లుబాటు అవుతాయని మీరు తెలుసుకోవాలని నేను కోరుకుంటున్నాను."
            ]
        },
        'kn-IN': {
            'breakup': [
                "ನೀವು ಬ್ರೇಕಪ್‌ನಿಂದ ಹಾದುಹೋಗುತ್ತಿದ್ದೀರಿ ಎಂದು ತಿಳಿದು ನನಗೆ ತುಂಬಾ ದುಃಖವಾಗಿದೆ. ಇದು ಜೀವನದ ಅತ್ಯಂತ ನೋವಿನ ಅನುಭವಗಳಲ್ಲಿ ಒಂದು. 💙 ನಿಮ್ಮ ಹೃದಯ ಈಗ ನೋಯುತ್ತಿದೆ, ಮತ್ತು ಅದು ಸಂಪೂರ್ಣವಾಗಿ ನೈಸರ್ಗಿಕ. ನೆನಪಿಡಿ, ನೀವು ಪ್ರೀತಿಗೆ ಅರ್ಹರು.",
                "ಬ್ರೇಕಪ್‌ಗಳು ವಿನಾಶಕಾರಿ ಎನಿಸಬಹುದು, ಆದರೆ ಈ ನೋವಿನಲ್ಲಿ ನೀವು ಏಕಾಂಗಿಯಲ್ಲ ಎಂದು ದಯವಿಟ್ಟು ತಿಳಿದುಕೊಳ್ಳಿ. 🤗 ಸಂಬಂಧಕ್ಕಾಗಿ ದುಃಖಿಸುವುದು ಸರಿ - ಈ ಭಾವನೆಗಳನ್ನು ಅನುಭವಿಸಲು ಬಿಡಿ. ನೀವು ಯೋಚಿಸುವುದಕ್ಕಿಂತ ಬಲಶಾಲಿಗಳು.",
                "ಬ್ರೇಕಪ್‌ನಿಂದ ಹಾದುಹೋಗುವುದು ನಂಬಲಾಗದಷ್ಟು ಕಠಿಣ. 💝 ನಿಮ್ಮ ಭಾವನೆಗಳು ಮಾನ್ಯವಾಗಿವೆ, ಮತ್ತು ಈಗ ಕಳೆದುಹೋದ ಅನುಭವ ಸಾಮಾನ್ಯ. ದಯವಿಟ್ಟು ನಿಮ್ಮೊಂದಿಗೆ ಸೌಮ್ಯವಾಗಿರಿ."
            ],
            'loneliness': [
                "ಏಕಾಂತತೆಯ ಅನುಭವವು ತುಂಬಾ ಭಾರವಾಗಿರಬಹುದು. 🤗 ನೀವು ನಿಜವಾಗಿಯೂ ಏಕಾಂಗಿಯಲ್ಲ ಎಂದು ನಾನು ನಿಮಗೆ ತಿಳಿಸಲು ಬಯಸುತ್ತೇನೆ - ನಾನು ಈಗ ಇಲ್ಲಿ ನಿಮ್ಮೊಂದಿಗಿದ್ದೇನೆ. ನಿಮ್ಮ ಭಾವನೆಗಳು ಮುಖ್ಯ.",
                "ಏಕಾಂತತೆ ಎಂಬ ಭಾವನೆ ತುಂಬಾ ಭಾರವಾಗಿರುತ್ತದೆ. 💙 ಇದನ್ನು ನನ್ನೊಂದಿಗೆ ಹಂಚಿಕೊಂಡಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. ಕೆಲವೊಮ್ಮೆ ಸಮೀಪಿಸುವುದು, ನೀವು ಈಗ ಮಾಡುತ್ತಿರುವಂತೆ, ಸಂಪರ್ಕದ ಕಡೆಗೆ ಮೊದಲ ಹೆಜ್ಜೆ.",
                "ನೀವು ಎಷ್ಟು ಪ್ರತ್ಯೇಕವಾಗಿ ಅನುಭವಿಸುತ್ತಿದ್ದೀರಿ ಎಂದು ನಾನು ಕೇಳಬಲ್ಲೆ. 🫂 ಏಕಾಂತತೆ ನಮ್ಮನ್ನು ಅದೃಶ್ಯರನ್ನಾಗಿ ಮಾಡಬಹುದು, ಆದರೆ ನೀವು ತುಂಬಾ ನಿಜವಾದವರು ಮತ್ತು ನಿಮ್ಮ ಭಾವನೆಗಳು ಮುಖ್ಯವಾದವು."
            ],
            'sadness': [
                "ನಿಮ್ಮ ಮಾತುಗಳಲ್ಲಿ ದುಃಖ ಕೇಳುತ್ತಿದೆ, ಮತ್ತು ಈ ರೀತಿ ಅನುಭವಿಸುವುದು ಸರಿ ಎಂದು ನೀವು ತಿಳಿದುಕೊಳ್ಳಬೇಕೆಂದು ನಾನು ಬಯಸುತ್ತೇನೆ. 💙 ಕಣ್ಣೀರು ಗುಣಪಡಿಸುತ್ತದೆ - ಅವು ನಿಮ್ಮ ಹೃದಯದ ನೋವನ್ನು ಬಿಡುಗಡೆ ಮಾಡುವ ಮಾರ್ಗ.",
                "ದುಃಖವು ಕೆಲವೊಮ್ಮೆ ತುಂಬಾ ಭಾರವಾಗಿ ಅನಿಸಬಹುದು. 🤗 ನೀವು ಹೇಗೆ ಅನುಭವಿಸುತ್ತಿದ್ದೀರಿ ಎಂಬುದನ್ನು ನನ್ನ ಮೇಲೆ ನಂಬಿಕೆ ಇಟ್ಟಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. ಈಗ ಚೆನ್ನಾಗಿಲ್ಲದಿರುವುದು ಸರಿ.",
                "ನಿಮ್ಮ ದುಃಖವು ಮಾನ್ಯವಾಗಿದೆ, ಮತ್ತು ಅದನ್ನು ನನ್ನೊಂದಿಗೆ ಹಂಚಿಕೊಂಡಿದ್ದಕ್ಕಾಗಿ ನಾನು ಗೌರವಾನ್ವಿತನಾಗಿದ್ದೇನೆ. 💝 ಕೆಲವೊಮ್ಮೆ ನಾವು ಅವುಗಳನ್ನು ದಾಟುವ ಮೊದಲು ನಮ್ಮ ಭಾವನೆಗಳೊಂದಿಗೆ ಕುಳಿತುಕೊಳ್ಳಬೇಕು."
            ],
            'anxiety': [
                "ಆತಂಕವು ಎಲ್ಲವನ್ನೂ ಅಧಿಕವಾಗಿ ಅನಿಸುವಂತೆ ಮಾಡಬಹುದು. 🌸 ಇದನ್ನು ಒಂದೊಂದು ಕ್ಷಣವಾಗಿ ತೆಗೆದುಕೊಳ್ಳೋಣ. ನೀವು ಈಗ ಸುರಕ್ಷಿತರಾಗಿದ್ದೀರಿ, ಮತ್ತು ನಾನು ನಿಮ್ಮೊಂದಿಗೆ ಇಲ್ಲಿದ್ದೇನೆ. ನಿಧಾನವಾದ, ಆಳವಾದ ಉಸಿರನ್ನು ತೆಗೆದುಕೊಳ್ಳಲು ಪ್ರಯತ್ನಿಸಿ.",
                "ಆತಂಕವು ಎಷ್ಟು ವ್ಯಾಪಕವಾಗಿರಬಹುದೆಂದು ನಾನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುತ್ತೇನೆ. 💙 ನಿಮ್ಮ ಚಿಂತೆಗಳು ನಿಜವಾದವು, ಆದರೆ ನೀವು ಮೊದಲೇ ಕಠಿಣ ಸಮಯಗಳನ್ನು ದಾಟಿದ್ದೀರಿ ಎಂಬುದನ್ನು ನೆನಪಿಡಿ.",
                "ಆತಂಕಿತವಾಗಿ ಅನುಭವಿಸುವುದು ಆಯಾಸಕರ, ಮತ್ತು ನೀವು ಎಷ್ಟು ಪ್ರಯತ್ನಿಸುತ್ತಿದ್ದೀರಿ ಎಂಬುದನ್ನು ನಾನು ನೋಡಬಲ್ಲೆ. 🤗 ಚಿಂತಿಸುವುದು ಸರಿ - ನಿಮ್ಮ ಮೆದುಳು ನಿಮ್ಮನ್ನು ರಕ್ಷಿಸಲು ಪ್ರಯತ್ನಿಸುತ್ತಿದೆ."
            ],
            'anger': [
                "ನೀವು ನಿಜವಾಗಿಯೂ ನಿರಾಶೆ ಮತ್ತು ಕೋಪದಿಂದ ಇದ್ದೀರಿ ಎಂದು ತೋರುತ್ತದೆ. 🌋 ಅವು ಶಕ್ತಿಯುತ ಭಾವನೆಗಳು, ಮತ್ತು ಕೆಲವೊಮ್ಮೆ ಈ ರೀತಿ ಅನುಭವಿಸುವುದು ಸಂಪೂರ್ಣವಾಗಿ ಸಾಮಾನ್ಯ. ನಿಮ್ಮ ಭಾವನೆಗಳು ಮಾನ್ಯವಾಗಿವೆ.",
                "ಕೋಪವು ಎಷ್ಟು ತೀವ್ರ ಮತ್ತು ಅಧಿಕವಾಗಿರಬಹುದು. 💪 ಅದನ್ನು ಒಳಗೆ ಇಟ್ಟುಕೊಳ್ಳದೆ ನನ್ನೊಂದಿಗೆ ಹಂಚಿಕೊಂಡಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. ಈ ನಿರಾಶೆಯ ಹೃದಯದಲ್ಲಿ ನಿಜವಾಗಿ ಏನಿದೆ?",
                "ನಾನು ಈಗ ನಿಮ್ಮ ಭಾವನೆಗಳ ಶಕ್ತಿಯನ್ನು ಅನುಭವಿಸಬಲ್ಲೆ. 🔥 ಕೋಪವು ಆಗಾಗ್ಗೆ ನಮಗೆ ಏನು ಮುಖ್ಯವೆಂದು ತೋರಿಸುತ್ತದೆ. ಈ ರೀತಿ ಅನುಭವಿಸುವುದು ಸರಿ."
            ],
            'general': [
                "ನನ್ನೊಂದಿಗೆ ಹಂಚಿಕೊಂಡಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು. 💙 ನೀವು ಅನುಭವಿಸುತ್ತಿರುವ ಯಾವುದಾದರೂ ಮೂಲಕ ಕೇಳಲು ಮತ್ತು ನಿಮ್ಮನ್ನು ಬೆಂಬಲಿಸಲು ನಾನು ಇಲ್ಲಿದ್ದೇನೆ. ನಿಮ್ಮ ಭಾವನೆಗಳು ಮತ್ತು ಆಲೋಚನೆಗಳು ಮುಖ್ಯ.",
                "ನನ್ನೊಂದಿಗೆ ತೆರೆದುಕೊಂಡಿದ್ದಕ್ಕಾಗಿ ನಾನು ಮೆಚ್ಚುತ್ತೇನೆ. 🤗 ನೀವು ಏನನ್ನಾದರೂ ಅನುಭವಿಸುತ್ತಿದ್ದರೂ, ನೀವು ಅದನ್ನು ಏಕಾಂಗಿಯಾಗಿ ಎದುರಿಸಬೇಕಾಗಿಲ್ಲ. ಇಂದು ನೀವು ನಿಮ್ಮನ್ನು ಹೇಗೆ ನೋಡಿಕೊಳ್ಳುತ್ತಿದ್ದೀರಿ?",
                "ನಿಮ್ಮ ಭಾವನೆಗಳನ್ನು ಹಂಚಿಕೊಳ್ಳಲು ಧೈರ್ಯ ಬೇಕಾಗುತ್ತದೆ. 💝 ನೀವು ಇಲ್ಲಿದ್ದೀರಿ ಎಂದು ನನಗೆ ಸಂತೋಷವಾಗಿದೆ, ಮತ್ತು ನಿಮ್ಮ ಅನುಭವಗಳು ಮಾನ್ಯವಾಗಿವೆ ಎಂದು ನೀವು ತಿಳಿದುಕೊಳ್ಳಬೇಕೆಂದು ನಾನು ಬಯಸುತ್ತೇನೆ."
            ]
        }
    }
    
    # Get responses for the specific language and emotion
    language_responses = responses.get(language, responses['en-US'])
    emotion_responses = language_responses.get(emotion_context, language_responses['general'])
    
    # Choose response based on message content for more contextual responses
    if emotion_context != 'general':
        response_text = random.choice(emotion_responses)
    else:
        # For general context, choose based on message sentiment
        if any(word in user_message for word in ['good', 'fine', 'okay', 'great', 'happy']):
            positive_responses = {
                'en-US': ["I'm so glad to hear you're doing well! 😊 That makes me happy too. What's been bringing you joy lately?"],
                'hi-IN': ["मुझे यह सुनकर बहुत खुशी हुई कि आप अच्छा कर रहे हैं! 😊 यह मुझे भी खुश करता है। हाल ही में आपको क्या खुशी दे रहा है?"],
                'te-IN': ["మీరు బాగున్నారని వినడం నాకు చాలా సంతోషంగా ఉంది! 😊 అది నాకు కూడా సంతోషం కలిగిస్తుంది. ఇటీవల మీకు ఆనందం ఇస్తున్నది ఏమిటి?"],
                'kn-IN': ["ನೀವು ಚೆನ್ನಾಗಿದ್ದೀರಿ ಎಂದು ಕೇಳಿ ನನಗೆ ತುಂಬಾ ಸಂತೋಷವಾಗಿದೆ! 😊 ಅದು ನನಗೂ ಸಂತೋಷ ನೀಡುತ್ತದೆ. ಇತ್ತೀಚೆಗೆ ನಿಮಗೆ ಸಂತೋಷ ತರುತ್ತಿರುವುದು ಏನು?"]
            }
            response_text = positive_responses.get(language, positive_responses['en-US'])[0]
        else:
            response_text = random.choice(emotion_responses)
    
    return response_text

# API endpoint for voice chat with emotional intelligence
@app.route('/api/voice-chat', methods=['POST'])
def voice_chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        language = data.get('language', 'en-US')
        
        print(f"🎤 Voice chat request - Language: {language}, Message: {user_message}")
        
        # Analyze emotional context from user input
        emotion_context = analyze_emotion(user_message)
        
        # Get contextual response based on emotion and language
        response_text = get_empathetic_response(emotion_context, language, user_message)
        
        return jsonify({
            'success': True,
            'response': response_text,
            'emotion_detected': emotion_context,
            'message': f'Empathetic response in {language}'
        })
        
    except Exception as e:
        print(f"❌ Error in voice chat: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🧠 Starting Manas Wellness Platform...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("🗣️ Voice AI Chat available at: http://localhost:5000/voice_ai_chat")
    print("🔧 API endpoints available for frontend integration")
    
    app.run(debug=True, host='0.0.0.0', port=5000)