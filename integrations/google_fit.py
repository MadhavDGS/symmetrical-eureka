# 🏃‍♀️ Google Fit Integration for Manas Wellness Platform
# Retrieves comprehensive health and fitness data for mood correlation

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime, timezone, timedelta
import json
import os
import logging

# Allow insecure transport for local development (OAuth over HTTP)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

logger = logging.getLogger(__name__)

class GoogleFitIntegration:
    """
    Google Fit API integration for retrieving comprehensive health data
    Supports OAuth 2.0 flow and health data aggregation
    """
    
    # Comprehensive fitness data scopes
    SCOPES = [
        'https://www.googleapis.com/auth/fitness.activity.read',
        'https://www.googleapis.com/auth/fitness.heart_rate.read',
        'https://www.googleapis.com/auth/fitness.body.read',
        'https://www.googleapis.com/auth/fitness.location.read',
        'https://www.googleapis.com/auth/fitness.nutrition.read',
        'https://www.googleapis.com/auth/fitness.oxygen_saturation.read',
        'https://www.googleapis.com/auth/fitness.reproductive_health.read',
        'https://www.googleapis.com/auth/fitness.sleep.read'
    ]
    
    # All available data types for comprehensive health tracking
    DATA_TYPES = [
        {"name": "Steps", "type": "com.google.step_count.delta", "unit": "steps"},
        {"name": "Heart Rate", "type": "com.google.heart_rate.bpm", "unit": "bpm"},
        {"name": "Calories", "type": "com.google.calories.expended", "unit": "kcal"},
        {"name": "Distance", "type": "com.google.distance.delta", "unit": "meters"},
        {"name": "Activity", "type": "com.google.activity.segment", "unit": "minutes"},
        {"name": "Weight", "type": "com.google.weight", "unit": "kg"},
        {"name": "Height", "type": "com.google.height", "unit": "meters"},
        {"name": "Sleep", "type": "com.google.sleep.segment", "unit": "minutes"},
        {"name": "Blood Pressure Systolic", "type": "com.google.blood_pressure.systolic", "unit": "mmHg"},
        {"name": "Blood Pressure Diastolic", "type": "com.google.blood_pressure.diastolic", "unit": "mmHg"},
        {"name": "Body Temperature", "type": "com.google.body.temperature", "unit": "celsius"},
        {"name": "Blood Glucose", "type": "com.google.blood_glucose", "unit": "mmol/L"},
        {"name": "Oxygen Saturation", "type": "com.google.oxygen_saturation", "unit": "%"},
        {"name": "Hydration", "type": "com.google.hydration", "unit": "liters"},
        {"name": "Nutrition", "type": "com.google.nutrition", "unit": "various"},
        {"name": "Move Minutes", "type": "com.google.active_minutes", "unit": "minutes"},
        {"name": "Speed", "type": "com.google.speed", "unit": "m/s"},
        {"name": "Power", "type": "com.google.power.sample", "unit": "watts"},
        {"name": "Cycling Wheel Revolution", "type": "com.google.cycling.wheel_revolution.rpm", "unit": "rpm"},
        {"name": "Cycling Pedaling Cadence", "type": "com.google.cycling.pedaling.cadence", "unit": "rpm"}
    ]
    
    def __init__(self, client_secrets_path=None, redirect_uri=None):
        """
        Initialize Google Fit integration
        
        Args:
            client_secrets_path: Path to Google OAuth client secrets JSON file
            redirect_uri: OAuth redirect URI (for web app flow)
        """
        self.client_secrets_path = client_secrets_path or os.getenv('GOOGLE_FIT_CLIENT_SECRETS')
        self.redirect_uri = redirect_uri or os.getenv('GOOGLE_FIT_REDIRECT_URI', 'http://127.0.0.1:8000/callback/googlefit')
        self.credentials_cache = {}
        
    def create_oauth_flow(self):
        """Create OAuth 2.0 flow for web application"""
        try:
            if not self.client_secrets_path or not os.path.exists(self.client_secrets_path):
                raise ValueError(f"Client secrets file not found: {self.client_secrets_path}")
                
            flow = Flow.from_client_secrets_file(
                self.client_secrets_path,
                scopes=self.SCOPES,
                redirect_uri=self.redirect_uri
            )
            return flow
        except Exception as e:
            logger.error(f"Failed to create OAuth flow: {e}")
            raise
    
    def get_auth_url(self, state=None):
        """Get authorization URL for OAuth flow"""
        try:
            flow = self.create_oauth_flow()
            auth_url, _ = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                state=state
            )
            return auth_url
        except Exception as e:
            logger.error(f"Failed to get auth URL: {e}")
            raise
    
    def handle_oauth_callback(self, authorization_response):
        """Handle OAuth callback and get credentials"""
        try:
            flow = self.create_oauth_flow()
            flow.fetch_token(authorization_response=authorization_response)
            return flow.credentials
        except Exception as e:
            logger.error(f"OAuth callback error: {e}")
            raise
    
    def save_credentials(self, user_id, credentials):
        """Save user credentials (implement secure storage)"""
        # In production, store encrypted in database
        self.credentials_cache[user_id] = credentials
        logger.info(f"Credentials cached for user {user_id}")
    
    def get_credentials(self, user_id):
        """Retrieve user credentials"""
        return self.credentials_cache.get(user_id)
    
    def clear_credentials(self, user_id):
        """Clear credentials for a user"""
        if user_id in self.credentials_cache:
            del self.credentials_cache[user_id]
            logger.info(f"Cleared credentials for user {user_id}")
            return True
        return False
    
    def refresh_credentials(self, credentials):
        """Refresh expired credentials"""
        try:
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                logger.info("Credentials refreshed successfully")
            return credentials
        except Exception as e:
            logger.error(f"Failed to refresh credentials: {e}")
            raise
    
    def build_service(self, credentials):
        """Build Google Fit API service"""
        try:
            credentials = self.refresh_credentials(credentials)
            return build('fitness', 'v1', credentials=credentials)
        except Exception as e:
            logger.error(f"Failed to build service: {e}")
            raise
    
    def get_fitness_data(self, user_id, days_back=7):
        """
        Retrieve comprehensive fitness data for a user
        
        Args:
            user_id: User identifier
            days_back: Number of days to retrieve data for
            
        Returns:
            Dictionary containing all available health data
        """
        try:
            credentials = self.get_credentials(user_id)
            if not credentials:
                return {"error": "No credentials found for user"}
            
            service = self.build_service(credentials)
            
            # Set time range
            end_time = datetime.now(timezone.utc)
            start_time = end_time - timedelta(days=days_back)
            
            logger.info(f"Fetching {days_back} days of data from {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}")
            
            health_data = {
                "user_id": user_id,
                "data_period": {
                    "start_date": start_time.isoformat(),
                    "end_date": end_time.isoformat(),
                    "days": days_back
                },
                "data": {},
                "summary": {},
                "last_updated": datetime.now(timezone.utc).isoformat()
            }
            
            # Fetch data for each type
            for data_type in self.DATA_TYPES:
                try:
                    data = self._fetch_data_type(
                        service, 
                        data_type, 
                        start_time, 
                        end_time
                    )
                    health_data["data"][data_type["name"].lower().replace(" ", "_")] = data
                    
                    # Generate summary statistics
                    if data and data.get("points"):
                        health_data["summary"][data_type["name"].lower().replace(" ", "_")] = self._generate_summary(data, data_type)
                        
                except Exception as e:
                    logger.warning(f"Failed to fetch {data_type['name']}: {e}")
                    health_data["data"][data_type["name"].lower().replace(" ", "_")] = {
                        "error": str(e),
                        "points": [],
                        "total_points": 0
                    }
            
            return health_data
            
        except Exception as e:
            logger.error(f"Failed to get fitness data: {e}")
            return {"error": str(e)}
    
    def _fetch_data_type(self, service, data_type, start_time, end_time):
        """Fetch data for a specific data type"""
        try:
            # Calculate time difference in days
            time_diff = end_time - start_time
            days_diff = time_diff.days
            
            # Adjust bucket size based on time range to avoid "aggregate duration too large" error
            if days_diff > 90:  # More than 3 months
                bucket_duration = 7 * 86400000  # Weekly buckets (7 days)
            elif days_diff > 30:  # More than 1 month
                bucket_duration = 86400000  # Daily buckets
            else:
                bucket_duration = 3600000  # Hourly buckets for shorter periods
            
            # Limit maximum time range to 90 days to avoid API errors
            if days_diff > 90:
                start_time = end_time - timedelta(days=90)
                logger.info(f"Limiting time range to 90 days for {data_type['name']}")
            
            body = {
                "aggregateBy": [{
                    "dataTypeName": data_type["type"]
                }],
                "bucketByTime": {"durationMillis": bucket_duration},
                "startTimeMillis": int(start_time.timestamp() * 1000),
                "endTimeMillis": int(end_time.timestamp() * 1000)
            }
            
            response = service.users().dataset().aggregate(
                userId="me",
                body=body
            ).execute()
            
            points = []
            for bucket in response.get("bucket", []):
                bucket_time = datetime.fromtimestamp(
                    int(bucket['startTimeMillis'])/1000, 
                    timezone.utc
                )
                
                for dataset in bucket.get("dataset", []):
                    for point in dataset.get("point", []):
                        formatted_point = self._format_data_point(
                            point, 
                            data_type, 
                            bucket_time
                        )
                        if formatted_point:
                            points.append(formatted_point)
            
            return {
                "type": data_type["name"],
                "unit": data_type["unit"],
                "points": points,
                "total_points": len(points)
            }
            
        except Exception as e:
            logger.warning(f"Failed to fetch {data_type['name']}: {e}")
            return {
                "type": data_type["name"],
                "unit": data_type["unit"],
                "points": [],
                "total_points": 0,
                "error": str(e)
            }
    
    def _format_data_point(self, point, data_type, bucket_time):
        """Format a data point based on its type"""
        try:
            values = point.get("value", [])
            if not values:
                return None
            
            formatted = {
                "date": bucket_time.strftime('%Y-%m-%d'),
                "timestamp": bucket_time.isoformat(),
                "data_type": data_type["name"],
                "unit": data_type["unit"]
            }
            
            # Format based on data type
            if data_type["type"] == "com.google.heart_rate.bpm":
                formatted.update({
                    "average": round(values[0].get('fpVal', 0), 1),
                    "maximum": round(values[1].get('fpVal', 0), 1),
                    "minimum": round(values[2].get('fpVal', 0), 1)
                })
            elif data_type["type"] == "com.google.step_count.delta":
                formatted["steps"] = values[0].get('intVal', 0)
            elif data_type["type"] == "com.google.calories.expended":
                formatted["calories"] = round(values[0].get('fpVal', 0), 1)
            elif data_type["type"] == "com.google.distance.delta":
                distance_m = values[0].get('fpVal', 0)
                formatted.update({
                    "distance_meters": round(distance_m, 2),
                    "distance_km": round(distance_m / 1000, 2)
                })
            elif data_type["type"] == "com.google.activity.segment":
                duration = (point.get('endTimeNanos', 0) - point.get('startTimeNanos', 0)) / (1000000000 * 60)
                formatted.update({
                    "activity_type": values[0].get('intVal', 0),
                    "duration_minutes": round(duration, 1)
                })
            elif data_type["type"] == "com.google.sleep.segment":
                duration = (point.get('endTimeNanos', 0) - point.get('startTimeNanos', 0)) / (1000000000 * 60)
                formatted.update({
                    "sleep_type": values[0].get('intVal', 0),
                    "duration_minutes": round(duration, 1)
                })
            elif data_type["type"] == "com.google.weight":
                formatted["weight_kg"] = round(values[0].get('fpVal', 0), 2)
            elif data_type["type"] == "com.google.height":
                formatted["height_m"] = round(values[0].get('fpVal', 0), 3)
            else:
                # Generic handling for other data types
                formatted["value"] = values[0].get('fpVal') or values[0].get('intVal', 0)
            
            return formatted
            
        except Exception as e:
            logger.warning(f"Failed to format data point: {e}")
            return None
    
    def _generate_summary(self, data, data_type):
        """Generate summary statistics for a data type"""
        try:
            points = data.get("points", [])
            if not points:
                return {"total_days": 0, "no_data": True}
            
            summary = {
                "total_days": len(points),
                "data_type": data_type["name"],
                "unit": data_type["unit"]
            }
            
            # Generate type-specific summaries
            if data_type["type"] == "com.google.step_count.delta":
                steps = [p["steps"] for p in points if "steps" in p]
                if steps:
                    summary.update({
                        "total_steps": sum(steps),
                        "avg_daily_steps": round(sum(steps) / len(steps), 0),
                        "max_daily_steps": max(steps),
                        "min_daily_steps": min(steps)
                    })
            
            elif data_type["type"] == "com.google.heart_rate.bpm":
                averages = [p["average"] for p in points if "average" in p]
                if averages:
                    summary.update({
                        "overall_avg_hr": round(sum(averages) / len(averages), 1),
                        "highest_avg_hr": max(averages),
                        "lowest_avg_hr": min(averages)
                    })
            
            elif data_type["type"] == "com.google.calories.expended":
                calories = [p["calories"] for p in points if "calories" in p]
                if calories:
                    summary.update({
                        "total_calories": round(sum(calories), 1),
                        "avg_daily_calories": round(sum(calories) / len(calories), 1),
                        "max_daily_calories": max(calories)
                    })
            
            elif data_type["type"] == "com.google.distance.delta":
                distances = [p["distance_km"] for p in points if "distance_km" in p]
                if distances:
                    summary.update({
                        "total_distance_km": round(sum(distances), 2),
                        "avg_daily_distance_km": round(sum(distances) / len(distances), 2),
                        "max_daily_distance_km": max(distances)
                    })
            
            return summary
            
        except Exception as e:
            logger.warning(f"Failed to generate summary: {e}")
            return {"error": str(e)}
    
    def get_recent_health_snapshot(self, user_id, hours_back=24):
        """Get a quick health snapshot for dashboard display"""
        try:
            credentials = self.get_credentials(user_id)
            if not credentials:
                return {"error": "No credentials found"}
            
            service = self.build_service(credentials)
            
            # Get recent data
            end_time = datetime.now(timezone.utc)
            start_time = end_time - timedelta(hours=hours_back)
            
            # Priority data types for quick snapshot
            priority_types = [
                {"name": "Steps", "type": "com.google.step_count.delta", "unit": "steps"},
                {"name": "Heart Rate", "type": "com.google.heart_rate.bpm", "unit": "bpm"},
                {"name": "Calories", "type": "com.google.calories.expended", "unit": "kcal"},
                {"name": "Active Minutes", "type": "com.google.active_minutes", "unit": "minutes"}
            ]
            
            snapshot = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "period_hours": hours_back,
                "health_metrics": {}
            }
            
            for data_type in priority_types:
                try:
                    data = self._fetch_data_type(service, data_type, start_time, end_time)
                    if data and data.get("points"):
                        # Get most recent point
                        latest_point = data["points"][-1] if data["points"] else None
                        if latest_point:
                            snapshot["health_metrics"][data_type["name"].lower().replace(" ", "_")] = latest_point
                except Exception as e:
                    logger.warning(f"Failed to get {data_type['name']} for snapshot: {e}")
            
            return snapshot
            
        except Exception as e:
            logger.error(f"Failed to get health snapshot: {e}")
            return {"error": str(e)}

# Global instance
google_fit = GoogleFitIntegration()