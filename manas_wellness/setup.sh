#!/bin/bash

# 🚀 Manas Wellness - Complete Setup Script
# Sets up the entire application for GenAI hackathon

echo "🚀 Manas Wellness Platform - Complete Setup"
echo "=============================================="
echo "Setting up your mental wellness platform for GenAI hackathon..."
echo

# Step 1: Check Python version
echo "🐍 Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python check passed"
echo

# Step 2: Create virtual environment if it doesn't exist
if [ ! -d "manas_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv manas_env
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo

# Step 3: Activate virtual environment
echo "🔄 Activating virtual environment..."
source manas_env/bin/activate
echo "✅ Virtual environment activated"
echo

# Step 4: Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip
echo "✅ Pip upgraded"
echo

# Step 5: Install requirements
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo

# Step 6: Set up environment file
if [ ! -f ".env" ]; then
    echo "⚙️ Setting up environment configuration..."
    cp .env.example .env
    echo "✅ Environment file created (.env)"
    echo "📝 IMPORTANT: Edit .env file to add your API keys!"
else
    echo "✅ Environment file already exists"
fi
echo

# Step 7: Create necessary directories
echo "📁 Creating required directories..."
mkdir -p logs
mkdir -p uploads
mkdir -p data_migration
mkdir -p test_data
mkdir -p config
echo "✅ Directories created"
echo

# Step 8: Set permissions
echo "🔐 Setting file permissions..."
chmod +x utils/*.py
chmod +x test_complete_system.py
echo "✅ Permissions set"
echo

# Step 9: Run system test
echo "🧪 Running system test..."
python test_complete_system.py
echo

# Step 10: Display final instructions
echo "🎉 Setup Complete!"
echo "=================="
echo
echo "🔧 Next Steps to Complete Your Setup:"
echo "1. 📝 Edit the .env file with your API keys:"
echo "   - Add your existing Gemini API key"
echo "   - Get Spotify API keys from developer.spotify.com" 
echo "   - Get MongoDB URI from mongodb.com/atlas"
echo "   - Get Google Cloud credentials from console.cloud.google.com"
echo "   - Get Supabase keys from supabase.com"
echo
echo "2. 🧪 Test API connections:"
echo "   python utils/test_spotify_integration.py"
echo "   python utils/test_mongodb_integration.py"
echo
echo "3. 🚀 Start your application:"
echo "   python app.py"
echo
echo "4. 🌐 Open your browser to:"
echo "   http://localhost:5000"
echo
echo "📊 Your Manas Wellness Platform Features:"
echo "✅ AI-powered therapeutic analysis (Gemini)"
echo "✅ Comprehensive mental health dashboard"
echo "✅ Journal with emotion analysis"
echo "✅ Eye tracking accessibility"
echo "✅ Anti-bullying detection"
echo "✅ Peer support system"
echo "⚠️  Music therapy (needs Spotify API keys)"
echo "⚠️  Scalable database (needs MongoDB)"
echo "⚠️  Real-time chat (needs Supabase)"
echo
echo "🏆 Ready for GenAI Hackathon Success!"
echo "Good luck with your presentation! 🚀"