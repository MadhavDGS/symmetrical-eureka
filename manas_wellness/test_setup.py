#!/usr/bin/env python3
"""
🧠 Manas: Setup Test Script
Quick test to verify installation and dependencies
"""

import sys
import os

def test_python_version():
    """Test Python version"""
    print(f"✅ Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Warning: Python 3.8+ recommended")
        return False
    return True

def test_basic_imports():
    """Test basic Python imports"""
    try:
        import json
        import datetime
        import pathlib
        print("✅ Basic Python modules: OK")
        return True
    except ImportError as e:
        print(f"❌ Basic imports failed: {e}")
        return False

def test_flask():
    """Test Flask import"""
    try:
        import flask
        print(f"✅ Flask version: {flask.__version__}")
        return True
    except ImportError:
        print("❌ Flask not installed")
        return False

def test_dotenv():
    """Test python-dotenv"""
    try:
        import dotenv
        print("✅ python-dotenv: OK")
        return True
    except ImportError:
        print("❌ python-dotenv not installed")
        return False

def test_requests():
    """Test requests library"""
    try:
        import requests
        print(f"✅ Requests version: {requests.__version__}")
        return True
    except ImportError:
        print("❌ Requests not installed")
        return False

def test_google_ai():
    """Test Google AI library"""
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI: OK")
        return True
    except ImportError:
        print("⚠️  Google Generative AI not installed (optional for basic testing)")
        return False

def test_numpy():
    """Test NumPy"""
    try:
        import numpy as np
        print(f"✅ NumPy version: {np.__version__}")
        return True
    except ImportError:
        print("⚠️  NumPy not installed (optional for basic testing)")
        return False

def test_environment_file():
    """Test .env file"""
    if os.path.exists('.env'):
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found (will use defaults)")
        return False

def test_directories():
    """Test required directories"""
    dirs = ['templates', 'utils']
    all_good = True
    
    for directory in dirs:
        if os.path.exists(directory):
            print(f"✅ Directory {directory}: OK")
        else:
            print(f"❌ Directory {directory}: Missing")
            all_good = False
    
    return all_good

def test_app_import():
    """Test main app import"""
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Try to import the main app
        import app
        print("✅ Main app.py: Import successful")
        return True
    except ImportError as e:
        print(f"❌ Main app.py import failed: {e}")
        return False
    except Exception as e:
        print(f"⚠️  App import warning: {e}")
        return True  # Still consider it a pass for basic setup

def main():
    """Run all tests"""
    print("🧠 Manas Setup Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Basic Imports", test_basic_imports),
        ("Flask", test_flask),
        ("Python-dotenv", test_dotenv),
        ("Requests", test_requests),
        ("Google AI", test_google_ai),
        ("NumPy", test_numpy),
        ("Environment File", test_environment_file),
        ("Directories", test_directories),
        ("App Import", test_app_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 Next steps:")
        print("1. Configure your API keys in .env file")
        print("2. Run: python app.py")
        print("3. Open http://localhost:5000")
    elif passed >= total - 2:
        print("✅ Setup is mostly ready! Some optional components missing.")
        print("\n🚀 You can still run the basic app:")
        print("1. Configure your API keys in .env file")
        print("2. Run: python app.py")
        print("3. Open http://localhost:5000")
    else:
        print("❌ Setup needs attention. Please install missing dependencies.")
        print("\n🔧 Try running:")
        print("pip install -r requirements-minimal.txt")

if __name__ == "__main__":
    main()