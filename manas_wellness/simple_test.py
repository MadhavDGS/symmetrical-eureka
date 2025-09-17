#!/usr/bin/env python3
"""
Simple test of the voice AI API endpoint
"""
import urllib.request
import urllib.parse
import json

def test_api():
    """Test the API endpoint"""
    url = "http://localhost:5000/api/voice-chat/analyze"
    
    # Test data
    data = {
        "message": "I'm feeling stressed about my exams",
        "timestamp": "2024-01-01T12:00:00Z"
    }
    
    # Convert to JSON
    json_data = json.dumps(data).encode('utf-8')
    
    # Create request
    req = urllib.request.Request(url, data=json_data)
    req.add_header('Content-Type', 'application/json')
    
    try:
        print("Testing Voice AI API...")
        print(f"URL: {url}")
        print(f"Data: {data}")
        
        # Make request
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            status = response.getcode()
            
            print(f"Status: {status}")
            
            if status == 200:
                result_data = json.loads(result)
                print("✅ SUCCESS!")
                print(f"Analysis: {result_data.get('analysis', {})}")
                print(f"Response: {result_data.get('response', 'No response')}")
            else:
                print(f"❌ Error: {status}")
                print(f"Response: {result}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure the server is running at http://localhost:5000")

if __name__ == "__main__":
    test_api()