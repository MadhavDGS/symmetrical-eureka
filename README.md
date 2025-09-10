# Manas Wellness Platform

A comprehensive mental health and wellness platform built with Flask, featuring AI-powered emotional analysis, therapy sessions, and crisis support.

## Features

- **Emotional Analysis**: AI-powered emotion detection and analysis
- **Therapy Sessions**: Personalized therapy recommendations
- **Crisis Support**: Emergency mental health support features
- **Multi-language Support**: Accessible in multiple languages
- **Offline Mode**: Works without internet connectivity
- **Accessibility**: Built with accessibility features for all users

## Project Structure

```
manas_wellness/
├── app.py                 # Main Flask application
├── start.py              # Application starter
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
├── static/              # Static assets (CSS, JS, images)
├── utils/               # Utility modules
├── svgicons/            # SVG icon collection
└── uploads/             # User uploads (not tracked in git)
```

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/MadhavDGS/symmetrical-eureka.git
   cd symmetrical-eureka/manas_wellness
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv manas_env
   source manas_env/bin/activate  # On Windows: manas_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python start.py
   ```

## Key Components

- **Emotion Detection**: Advanced AI models for emotional state analysis
- **Crisis Detection**: Real-time monitoring for mental health emergencies
- **Therapy Generator**: AI-powered personalized therapy recommendations
- **Multi-language Processor**: Support for multiple languages
- **Accessibility Engine**: Enhanced accessibility features
- **Offline Manager**: Functionality for offline usage

## Technologies Used

- **Backend**: Flask (Python)
- **AI/ML**: Google Gemini API
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Icons**: Custom SVG icon set

## Contributing

This project is part of a mental health hackathon initiative. Contributions are welcome to improve mental health support features.

## License

This project is developed for educational and hackathon purposes.
