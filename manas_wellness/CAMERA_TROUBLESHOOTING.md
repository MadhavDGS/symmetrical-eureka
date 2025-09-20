# 🔧 Camera & Microphone Troubleshooting Guide

## ❗ **CRITICAL ISSUE IDENTIFIED:**
Your Google API key is being rejected because the Generative Language API is disabled for your project.

## 🚨 **IMMEDIATE FIX REQUIRED:**

### Step 1: Enable Google Generative AI API
1. **Go to:** https://console.developers.google.com/apis/api/generativelanguage.googleapis.com/overview?project=822822507354
2. **Click:** "ENABLE API" button
3. **Wait:** 2-3 minutes for the API to activate
4. **Restart** your Flask server after enabling

---

## 🎥 **CAMERA ACCESS TROUBLESHOOTING:**

### Windows Camera Settings:
1. **Press:** `Windows Key + I`
2. **Go to:** Privacy & Security → Camera
3. **Enable:** "Allow apps to access your camera"
4. **Enable:** "Allow desktop apps to access your camera"

### Browser Camera Permissions:
1. **Open:** Chrome/Edge
2. **Go to:** `chrome://settings/content/camera` (Chrome) or `edge://settings/content/camera` (Edge)
3. **Check:** Camera is not blocked
4. **Add:** `http://localhost:5000` to allowed sites

### Test Camera Access:
1. **Open:** `http://localhost:5000/emotion-analysis`
2. **Click:** "Capture Photo" button
3. **Look for:** Camera permission popup
4. **Click:** "Allow" when prompted

---

## 🎤 **MICROPHONE ACCESS TROUBLESHOOTING:**

### Windows Microphone Settings:
1. **Press:** `Windows Key + I`
2. **Go to:** Privacy & Security → Microphone
3. **Enable:** "Allow apps to access your microphone"
4. **Enable:** "Allow desktop apps to access your microphone"

### Browser Microphone Permissions:
1. **Go to:** `chrome://settings/content/microphone` (Chrome)
2. **Check:** Microphone is not blocked
3. **Add:** `http://localhost:5000` to allowed sites

### Test Microphone:
1. **Open:** `http://localhost:5000/emotion-analysis`
2. **Click:** "Record Voice" button
3. **Allow:** microphone access when prompted

---

## 🔍 **DEBUGGING STEPS:**

### 1. Check Browser Console:
1. **Press:** `F12` to open Developer Tools
2. **Go to:** Console tab
3. **Look for:** Red error messages
4. **Common errors:**
   - `NotAllowedError`: Permission denied
   - `NotFoundError`: No camera/microphone found
   - `NotReadableError`: Device in use by another app

### 2. Test Basic Camera:
1. **Open:** Windows Camera app
2. **Verify:** Camera works outside browser
3. **Close:** Camera app completely before testing website

### 3. Browser-Specific Fixes:

#### Chrome:
- Type: `chrome://flags/#unsafely-treat-insecure-origin-as-secure`
- Add: `http://localhost:5000`
- Restart Chrome

#### Edge:
- Type: `edge://flags/#unsafely-treat-insecure-origin-as-secure`
- Add: `http://localhost:5000`
- Restart Edge

### 4. Reset Browser Permissions:
1. **Go to:** `http://localhost:5000`
2. **Click:** Lock icon in address bar
3. **Reset:** Camera and Microphone permissions
4. **Refresh:** page and try again

---

## 🖥️ **SYSTEM-LEVEL FIXES:**

### Update Camera Drivers:
1. **Press:** `Windows Key + X`
2. **Select:** Device Manager
3. **Expand:** Cameras
4. **Right-click:** Your camera
5. **Select:** Update driver

### Check Antivirus/Firewall:
1. **Temporarily disable** antivirus camera protection
2. **Add exception** for Chrome/Edge in firewall
3. **Test** camera access
4. **Re-enable** security after testing

### Windows Camera Privacy Reset:
```powershell
# Run as Administrator in PowerShell
Get-AppxPackage Microsoft.WindowsCamera | Reset-AppxPackage
```

---

## 🧪 **TESTING CHECKLIST:**

### Before Testing:
- [ ] Google Generative AI API is enabled
- [ ] Flask server restarted
- [ ] Windows camera privacy enabled
- [ ] Browser permissions granted
- [ ] No other apps using camera/microphone

### Test Sequence:
1. **Open:** `http://localhost:5000/accessibility`
2. **Test:** Eye tracking camera access
3. **Open:** `http://localhost:5000/emotion-analysis`
4. **Test:** Voice recording
5. **Test:** Camera photo capture
6. **Open:** `http://localhost:5000/therapy-session`
7. **Test:** Quick emotion selection (non-camera)

### Success Indicators:
- ✅ Camera video feed appears
- ✅ Microphone recording works
- ✅ No permission errors in console
- ✅ Emotion analysis returns results

---

## 🆘 **IF STILL NOT WORKING:**

### Try Incognito/Private Mode:
1. **Open:** Browser in incognito/private mode
2. **Test:** camera access
3. **If working:** Clear browser data for localhost

### Alternative Browser Test:
1. **Try:** Different browser (Chrome, Edge, Firefox)
2. **Install:** Latest browser version
3. **Test:** Same functionality

### Hardware Check:
1. **Disconnect/Reconnect:** USB camera
2. **Try:** Different USB port
3. **Test:** Built-in laptop camera vs external
4. **Check:** Camera is not physically covered

---

## 📱 **MOBILE TESTING:**
If on mobile device:
1. **Open:** `http://192.168.1.112:5000` (your network IP)
2. **Allow:** camera/microphone permissions
3. **Note:** Some features work better on mobile

---

## 🔧 **MANUAL CONFIGURATION:**

### Environment Variables:
```powershell
# Set in PowerShell before running
$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

### Camera Access Test Code:
You can test camera access with this simple HTML file:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Camera Test</title>
</head>
<body>
    <video id="video" width="640" height="480" autoplay></video>
    <script>
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                document.getElementById('video').srcObject = stream;
                console.log('Camera access successful!');
            })
            .catch(error => {
                console.error('Camera access failed:', error);
                alert('Camera access failed: ' + error.message);
            });
    </script>
</body>
</html>
```

Save as `camera_test.html` and open in browser to test basic camera access.

---

## 📞 **NEED MORE HELP?**

If none of these solutions work:
1. **Check:** Error messages in browser console (F12)
2. **Note:** Exact error text
3. **Try:** Different device/browser
4. **Provide:** Details about your specific setup

The most critical issue is the Google API - **enable it first** before testing camera features!