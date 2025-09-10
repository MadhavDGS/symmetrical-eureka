# 🧠 Manas: Youth Mental Wellness Platform

**AI-Powered Mental Health Support for Indian Youth**

Built for Google GenAI Exchange Hackathon 2025

## 🌟 Overview

Manas is a comprehensive mental wellness platform specifically designed for Indian youth, featuring:

- **Multi-modal Emotion Detection**: Analyze emotions through voice, facial expressions, and text
- **Accessibility-First Design**: Eye tracking, sign language support, and adaptive interfaces
- **Cultural Sensitivity**: Content adapted for Indian cultural contexts and regional languages
- **Crisis Detection**: Advanced AI monitoring with immediate intervention capabilities
- **Offline Support**: Therapy exercises and coping strategies available without internet
- **Personalized Therapy**: AI-generated content tailored to individual needs

## 🚀 Key Features

### 🎭 Multi-Modal AI
- **Facial Emotion Recognition** using MediaPipe
- **Voice Emotion Analysis** with audio processing
- **Text Sentiment Analysis** powered by Gemini AI
- **Multi-modal Fusion** for higher accuracy

### ♿ Accessibility Engine
- **Eye Tracking Navigation** for hands-free control
- **Gesture Recognition** for intuitive interaction
- **Sign Language Support** (ASL/ISL)
- **Voice Control** with wake word detection
- **Adaptive UI** based on user needs

### 🇮🇳 Cultural Intelligence
- **10+ Indian Languages** supported
- **Cultural Context Awareness** in therapy content
- **Family-Oriented Approach** respecting Indian values
- **Regional Customization** for different states

### 🚨 Crisis Detection
- **Behavioral Pattern Analysis** for early warning
- **Risk Level Assessment** with AI monitoring
- **Immediate Intervention** protocols
- **Professional Support** connection

### 📱 Offline Capabilities
- **Offline Therapy Exercises** cached locally
- **Crisis Support Resources** available without internet
- **Data Synchronization** when connection returns
- **Progressive Web App** functionality

## 🛠️ Technical Architecture

### Backend
- **Flask** (Python 3.12+) - Web framework
- **SQLite** - Local database
- **Google Gemini 2.5 Flash** - Primary AI model
- **MediaPipe** - Computer vision processing
- **Librosa** - Audio analysis

### AI/ML Stack
- **Google Cloud AI Platform** - ML services
- **Speech-to-Text & Text-to-Speech** - Voice processing
- **Computer Vision** - Facial emotion detection
- **Natural Language Processing** - Text analysis

### Frontend
- **HTML5/CSS3** - Modern web standards
- **Tailwind CSS** - Utility-first styling
- **JavaScript** - Interactive functionality
- **Progressive Web App** - Offline capabilities

## 📦 Installation

### Prerequisites
- Python 3.12+
- Google Cloud Account with AI services enabled
- Gemini API key

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd manas_wellness
   ```

2. **Create virtual environment**
   ```bash
   python -m venv manas_env
   source manas_env/bin/activate  # On macOS/Linux
   # manas_env\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Set up Google Cloud credentials**
   - Download service account JSON file
   - Set GOOGLE_APPLICATION_CREDENTIALS in .env

6. **Initialize database**
   ```bash
   python -c "from app import init_db; init_db()"
   ```

7. **Run the application**
   ```bash
   python app.py
   ```

8. **Access the platform**
   - Open http://localhost:5000 in your browser

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```env
# Core Configuration
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
SECRET_KEY=your_secret_key

# Feature Toggles
EYE_TRACKING_ENABLED=True
VOICE_CONTROL_ENABLED=True
CRISIS_DETECTION_ENABLED=True

# Language Support
DEFAULT_LANGUAGE=english
SUPPORTED_LANGUAGES=english,hindi,telugu,tamil,bengali
```

### Google Cloud Services Setup

1. **Enable APIs**:
   - AI Platform API
   - Speech-to-Text API
   - Text-to-Speech API
   - Translation API

2. **Create Service Account**:
   - Download JSON credentials
   - Grant necessary permissions

3. **Configure Gemini API**:
   - Get API key from Google AI Studio
   - Add to environment variables

## 🎯 Usage

### For Users

1. **Registration**: Create account with accessibility preferences
2. **Emotion Analysis**: Share feelings through text, voice, or camera
3. **Therapy Sessions**: Receive personalized therapy content
4. **Crisis Support**: Access immediate help when needed
5. **Progress Tracking**: Monitor wellness journey over time

### For Developers

1. **API Endpoints**: RESTful APIs for all functionality
2. **Modular Architecture**: Easy to extend and customize
3. **Accessibility APIs**: Built-in accessibility features
4. **Multi-language Support**: Easy to add new languages

## 🔒 Privacy & Security

- **Data Encryption**: All sensitive data encrypted
- **Local Processing**: Emotion analysis can run locally
- **Minimal Data Collection**: Only essential data stored
- **User Control**: Full control over data sharing
- **GDPR Compliant**: Privacy by design

## 🌍 Supported Languages

- **English** - Primary language
- **हिंदी (Hindi)** - National language
- **తెలుగు (Telugu)** - Regional language
- **தமிழ் (Tamil)** - Regional language
- **বাংলা (Bengali)** - Regional language
- **ગુજરાતી (Gujarati)** - Regional language
- **मराठी (Marathi)** - Regional language
- **ಕನ್ನಡ (Kannada)** - Regional language
- **മലയാളം (Malayalam)** - Regional language
- **ਪੰਜਾਬੀ (Punjabi)** - Regional language

## 🚨 Crisis Resources

### National Helplines
- **AASRA**: 91-22-27546669 (24/7)
- **Sneha**: 044-24640050 (24/7)
- **Vandrevala Foundation**: 1860-2662-345 (24/7)
- **Emergency Services**: 112

### Features
- **Automatic Crisis Detection** using AI
- **Immediate Intervention** protocols
- **Professional Referrals** when needed
- **24/7 Support** availability

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork the repository**
2. **Create feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Add tests for new features
- Update documentation
- Ensure accessibility compliance

## 📊 Performance

- **Sub-30s Response Times** for AI analysis
- **Offline-First Architecture** for reliability
- **Progressive Loading** for better UX
- **Optimized for Mobile** devices

## 🏆 Hackathon Highlights

### Innovation
- **First mental health platform** with comprehensive accessibility
- **Multi-modal emotion detection** beyond simple chatbots
- **Cultural intelligence** for Indian context
- **Offline-first approach** for low-connectivity areas

### Technical Excellence
- **Production-ready architecture** with 70% existing codebase leverage
- **Advanced AI integration** with multiple Google Cloud services
- **Accessibility compliance** with WCAG 2.1 standards
- **Scalable design** for millions of users

### Social Impact
- **350+ million Indian youth** addressable market
- **Mental health stigma reduction** through technology
- **Inclusive design** for users with disabilities
- **Crisis prevention** through early detection

## 📈 Roadmap

### Phase 1 (Current)
- ✅ Core platform development
- ✅ Multi-modal emotion detection
- ✅ Basic accessibility features
- ✅ Crisis detection system

### Phase 2 (Next 3 months)
- 🔄 Advanced therapy modules
- 🔄 Professional therapist integration
- 🔄 Enhanced offline capabilities
- 🔄 Mobile app development

### Phase 3 (6 months)
- 📋 School partnership program
- 📋 Government healthcare integration
- 📋 Advanced analytics dashboard
- 📋 International expansion

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Cloud AI** for powerful AI services
- **MediaPipe** for computer vision capabilities
- **Indian mental health organizations** for guidance
- **Accessibility community** for inclusive design principles
- **Open source community** for foundational tools

## 📞 Support

For support, email support@manas-wellness.com or join our community:

- **Documentation**: [docs.manas-wellness.com](https://docs.manas-wellness.com)
- **Community Forum**: [community.manas-wellness.com](https://community.manas-wellness.com)
- **Bug Reports**: [GitHub Issues](https://github.com/manas-wellness/issues)

---

**Built with ❤️ for Indian youth mental wellness**

*Manas - Where technology meets compassion*