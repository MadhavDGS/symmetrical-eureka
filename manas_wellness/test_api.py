#!/usr/bin/env python3
"""
Test the voice AI API endpoint
"""
import requests
import json

def test_voice_api():
    """Test the voice chat API endpoint"""
    url = "http://localhost:5000/api/voice-chat/analyze"
    
    # Test data
    test_cases = [
        {
            "message": "I'm feeling really stressed about my upcoming exams",
            "timestamp": "2024-01-01T12:00:00Z"
        },
        {
            "message": "How can I manage my anxiety?",
            "timestamp": "2024-01-01T12:01:00Z"
        },
        {
            "message": "I'm having a great day and feeling very positive",
            "timestamp": "2024-01-01T12:02:00Z"
        }
    ]
    
    for i, test_data in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Message: {test_data['message']}")
        
        try:
            response = requests.post(url, json=test_data, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success: {response.status_code}")
                print(f"Analysis: {data.get('analysis', {})}")
                print(f"Response: {data.get('response', 'No response')}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Server not running")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing Voice AI API...")
    test_voice_api()