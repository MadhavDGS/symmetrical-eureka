# 🏃‍♀️ Google Fit Integration Setup Guide

## Quick Setup Overview

Your Manas Wellness Platform now includes comprehensive Google Fit health data integration! This allows users to connect their fitness data for personalized wellness insights.

## What's Been Implemented

### ✅ **Complete Integration**
- **Google Fit API Client** (`integrations/google_fit.py`) - Handles OAuth and data retrieval
- **Flask API Routes** - OAuth flow endpoints and health data APIs  
- **Dashboard Integration** - Real-time health metrics display
- **Comprehensive Data Types** - Steps, heart rate, calories, sleep, activities, and more

### ✅ **Features Available**
- **20+ Health Metrics**: Steps, heart rate, calories, distance, sleep, blood pressure, etc.
- **Smart Health Insights**: AI-generated wellness recommendations based on activity
- **Secure OAuth 2.0**: Complete authorization flow with token management
- **Real-time Dashboard**: Live health data display with refresh capability
- **Privacy-First**: All data processed locally, never shared externally

## API Endpoints Available

| Endpoint | Purpose |
|----------|---------|
| `/api/googlefit/auth` | Initiate OAuth flow |
| `/api/googlefit/callback` | Handle OAuth callback |
| `/api/googlefit/data?days=7` | Get comprehensive health data |
| `/api/googlefit/snapshot?hours=24` | Get recent health snapshot |
| `/api/googlefit/status` | Check connection status |

## Google Cloud Console Setup

To activate the Google Fit integration, you need to:

### 1. **Create Google Cloud Project**
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create a new project or use existing one

### 2. **Enable Fitness API**
- Navigate to "APIs & Services" → "Library"
- Search for "Fitness API" 
- Click "Enable"

### 3. **Create OAuth 2.0 Credentials**
- Go to "APIs & Services" → "Credentials"
- Click "Create Credentials" → "OAuth client ID"
- Choose "Web application"
- Add these **Authorized redirect URIs**:
  ```
  http://127.0.0.1:8000/callback/googlefit
  http://localhost:8000/callback/googlefit
  ```
- Add these **Authorized JavaScript origins**:
  ```
  http://127.0.0.1:8000
  http://localhost:8000
  ```

### 4. **Download Client Secrets**
- Download the JSON credentials file
- Rename it to `google_fit_client_secrets.json`
- Place it in your project root directory

### 5. **Update Environment Variables**
Your `.env` file now includes:
```bash
GOOGLE_FIT_CLIENT_SECRETS=google_fit_client_secrets.json
GOOGLE_FIT_REDIRECT_URI=http://127.0.0.1:8000/callback/googlefit
```

## Health Data Types Supported

The integration retrieves comprehensive health data:

### 📊 **Activity Metrics**
- Daily steps and distance
- Calories burned  
- Active minutes
- Movement speed and power
- Cycling cadence and wheel revolutions

### ❤️ **Vital Signs**
- Heart rate (average, min, max)
- Blood pressure (systolic/diastolic)
- Blood glucose levels
- Oxygen saturation
- Body temperature

### 🏋️ **Body Metrics** 
- Weight tracking
- Height measurements
- Body composition data

### 😴 **Sleep & Recovery**
- Sleep duration and quality
- Sleep phases tracking
- Recovery metrics

### 🥗 **Nutrition & Hydration**
- Water intake tracking
- Nutritional data
- Meal logging information

## Dashboard Integration

The dashboard now includes:

### **Health Snapshot Widget**
- Real-time display of key metrics
- Automatic refresh functionality  
- Visual indicators for each data type

### **Smart Health Insights**
- AI-generated recommendations based on activity levels
- Personalized tips for mental wellness
- Activity-mood correlation insights

### **Connection Management**
- Easy OAuth connection flow
- Status monitoring
- Privacy information and controls

## User Experience Flow

1. **Initial Visit**: Users see "Connect Google Fit" card
2. **OAuth Flow**: Secure popup-based authentication
3. **Data Loading**: Automatic retrieval of health metrics
4. **Insights Display**: Real-time health data with AI insights
5. **Continuous Sync**: Automatic updates and refresh capability

## Privacy & Security

- **OAuth 2.0 Security**: Industry-standard authorization flow
- **Local Processing**: All data analysis happens on your server
- **No Data Sharing**: Health information never leaves your platform
- **User Control**: Users can disconnect anytime
- **Secure Storage**: Encrypted credential storage

## Testing the Integration

1. **Start the app**: `python app.py`
2. **Visit dashboard**: Navigate to the main dashboard
3. **Connect Google Fit**: Click "Connect Google Fit" button
4. **Authorize access**: Complete OAuth flow in popup
5. **View health data**: See real-time metrics and insights

## Troubleshooting

### **"Google Fit integration not available"**
- Check that all dependencies are installed
- Verify the `google_fit_client_secrets.json` file exists
- Ensure environment variables are set correctly

### **OAuth Authorization Errors**
- Verify redirect URIs match Google Cloud Console exactly
- Check that Fitness API is enabled
- Ensure client secrets file is valid JSON

### **No Health Data**
- Users need Google Fit app with existing data
- Data may take 5-15 minutes to sync from devices
- Try different date ranges (1-30 days)

## Advanced Configuration

### **Custom Data Retention**
Modify `days_back` parameter (max 30 days):
```javascript
await fetch('/api/googlefit/data?days=14')
```

### **Specific Health Metrics**
The system automatically handles all available data types and gracefully handles missing data.

### **Health Insights Customization**
Modify the `generateHealthInsight()` function in dashboard.html to customize AI recommendations.

## Production Considerations

- **Rate Limiting**: Google Fit API has usage quotas
- **Credential Security**: Store client secrets securely (not in version control)
- **User Management**: Implement proper user sessions for multi-user apps
- **Data Backup**: Consider caching health data for offline access
- **Compliance**: Ensure HIPAA/privacy law compliance if required

## Integration Complete! 🎉

Your Manas Wellness Platform now includes comprehensive health data integration that:
- Enhances therapy recommendations with physical activity insights
- Provides holistic wellness tracking combining mental and physical health
- Offers personalized insights based on real user data
- Maintains the highest privacy and security standards

The integration is ready for immediate use and testing!