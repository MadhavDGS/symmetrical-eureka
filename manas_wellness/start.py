#!/usr/bin/env python3
"""
🧠 Manas: Youth Mental Wellness Platform
Startup Script for Development

This script helps set up and start the Manas platform for development.
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def print_banner():
    """Print the Manas banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║                    🧠 MANAS WELLNESS PLATFORM                ║
    ║                                                              ║
    ║              AI-Powered Mental Health for Indian Youth       ║
    ║                                                              ║
    ║              Google GenAI Exchange Hackathon 2025           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python version: {sys.version.split()[0]}")

def check_environment():
    """Check if environment is properly set up"""
    print("\n🔍 Checking environment setup...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found")
        print("   Please copy .env.example to .env and configure your API keys")
        
        # Create basic .env file
        with open('.env', 'w') as f:
            f.write("# Manas Environment Configuration\n")
            f.write("SECRET_KEY=dev_secret_key_change_in_production\n")
            f.write("FLASK_ENV=development\n")
            f.write("FLASK_DEBUG=True\n")
            f.write("\n# Add your API keys here:\n")
            f.write("# GEMINI_API_KEY=your_gemini_api_key_here\n")
            f.write("# GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json\n")
        
        print("   Created basic .env file - please add your API keys")
    else:
        print("✅ .env file found")

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        print("   Please run: pip install -r requirements.txt")
        return False
    
    return True

def setup_database():
    """Set up the SQLite database"""
    print("\n🗄️  Setting up database...")
    
    try:
        # Import and initialize database
        from app import init_db
        init_db()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ['uploads', 'static', 'templates', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created/verified directory: {directory}")

def check_api_keys():
    """Check if API keys are configured"""
    print("\n🔑 Checking API configuration...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    google_creds = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    if not gemini_key:
        print("⚠️  Warning: GEMINI_API_KEY not configured")
        print("   Some AI features may not work without this key")
    else:
        print("✅ Gemini API key configured")
    
    if not google_creds:
        print("⚠️  Warning: GOOGLE_APPLICATION_CREDENTIALS not configured")
        print("   Google Cloud services may not work without credentials")
    else:
        if os.path.exists(google_creds):
            print("✅ Google Cloud credentials file found")
        else:
            print("⚠️  Warning: Google Cloud credentials file not found")

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting Manas platform...")
    print("   Access the platform at: http://localhost:5000")
    print("   Press Ctrl+C to stop the server")
    print("\n" + "="*60)
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Manas platform stopped. Thank you for using our platform!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("   Please check the logs for more details")

def main():
    """Main startup function"""
    print_banner()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("🔧 Setting up Manas platform for development...")
    
    # Run setup checks
    check_python_version()
    check_environment()
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed. Please resolve dependency issues and try again.")
        sys.exit(1)
    
    # Set up database
    if not setup_database():
        print("\n❌ Database setup failed. Please check the error and try again.")
        sys.exit(1)
    
    # Check API configuration
    check_api_keys()
    
    print("\n✅ Setup completed successfully!")
    print("\n📋 Quick Start Guide:")
    print("   1. Configure your API keys in the .env file")
    print("   2. The platform will start automatically")
    print("   3. Open http://localhost:5000 in your browser")
    print("   4. Create an account and start your wellness journey")
    
    print("\n🌟 Features to try:")
    print("   • Emotion Analysis - Analyze your feelings through text, voice, or camera")
    print("   • Therapy Sessions - Get personalized therapy content")
    print("   • Accessibility - Try eye tracking and voice control")
    print("   • Crisis Support - Access immediate help resources")
    
    # Start the application
    input("\nPress Enter to start the platform...")
    start_application()

if __name__ == "__main__":
    main()