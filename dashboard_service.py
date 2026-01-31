"""
Dashboard Data Service - Provides real-time farm monitoring data
"""
import random
from datetime import datetime, timedelta
import json
from crop_data import TAMIL_NADU_CROP_DATA, STATE_DISTRICT_DATA, CROP_BASE_PRICES

class DashboardService:
    def __init__(self):
        self.market_data = self._generate_market_data()
        self.weather_data = self._generate_weather_data()
        self.crop_health_data = self._generate_crop_health_data()
    
    def get_live_market_rates(self, state=None, district=None):
        """Get current market rates for crops"""
        crops = ['wheat', 'rice', 'corn', 'cotton', 'sugarcane', 'soybean']
        market_rates = []
        
        for crop in crops:
            base_price = {'wheat': 25, 'rice': 30, 'corn': 20, 'cotton': 45, 'sugarcane': 35, 'soybean': 40}[crop]
            current_price = base_price * (0.9 + random.random() * 0.2)
            change = (random.random() - 0.5) * 10
            
            market_rates.append({
                'crop': crop,
                'current_price': round(current_price, 2),
                'price_change': round(change, 2),
                'trend': 'up' if change > 0 else 'down',
                'market': f"{district} Mandi" if district else "Local Mandi",
                'last_updated': datetime.now().isoformat()
            })
        
        return market_rates
    
    def get_crop_health_summary(self, state=None, district=None, city=None):
        """Get crop health data using simulated satellite indices"""
        crops = ['wheat', 'rice', 'corn', 'cotton']
        health_data = []
        
        for crop in crops:
            ndvi_score = 0.3 + random.random() * 0.6  # NDVI typically 0.3-0.9
            health_score = int(ndvi_score * 100)
            
            if health_score >= 80:
                status = 'Excellent'
                color = 'green'
            elif health_score >= 60:
                status = 'Good'
                color = 'lightgreen'
            elif health_score >= 40:
                status = 'Fair'
                color = 'yellow'
            else:
                status = 'Poor'
                color = 'red'
            
            health_data.append({
                'crop': crop,
                'ndvi_score': round(ndvi_score, 3),
                'health_score': health_score,
                'status': status,
                'color': color,
                'area_hectares': random.randint(50, 500),
                'last_satellite_pass': (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat()
            })
        
        return health_data
    
    def get_weather_data(self, state=None, district=None, city=None):
        """Get hyper-local weather data with forecast"""
        current_weather = {
            'temperature': random.randint(20, 35),
            'humidity': random.randint(40, 80),
            'rainfall_today': round(random.random() * 10, 1),
            'wind_speed': random.randint(5, 25),
            'condition': random.choice(['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain']),
            'last_updated': datetime.now().isoformat()
        }
        
        # 7-day forecast
        forecast = []
        for i in range(7):
            date = datetime.now() + timedelta(days=i+1)
            forecast.append({
                'date': date.strftime('%Y-%m-%d'),
                'day': date.strftime('%A'),
                'max_temp': random.randint(25, 38),
                'min_temp': random.randint(15, 25),
                'rainfall_chance': random.randint(0, 100),
                'condition': random.choice(['Sunny', 'Partly Cloudy', 'Cloudy', 'Rain', 'Thunderstorm'])
            })
        
        return {
            'current': current_weather,
            'forecast': forecast,
            'location': f"{city}, {district}, {state}" if all([city, district, state]) else "Local Area"
        }
    
    def get_market_alerts(self):
        """Get current market alerts and notifications"""
        alerts = [
            {
                'id': 'alert_1',
                'type': 'price_surge',
                'crop': 'wheat',
                'message': 'Wheat prices up 15% in local markets',
                'severity': 'high',
                'timestamp': datetime.now().isoformat()
            },
            {
                'id': 'alert_2',
                'type': 'weather_warning',
                'message': 'Heavy rainfall expected in next 48 hours',
                'severity': 'medium',
                'timestamp': (datetime.now() - timedelta(hours=2)).isoformat()
            }
        ]
        return alerts
    
    def _generate_market_data(self):
        """Generate sample market data"""
        return {}
    
    def _generate_weather_data(self):
        """Generate sample weather data"""
        return {}
    
    def _generate_crop_health_data(self):
        """Generate sample crop health data"""
        return {}
    
    def get_top_districts_by_price(self, state, crop):
        """Get top 5 districts with highest prices for a crop in a state"""
        if state not in STATE_DISTRICT_DATA:
            return []
        
        districts = STATE_DISTRICT_DATA[state]['districts']
        base_price = CROP_BASE_PRICES.get(crop, 30)
        
        district_prices = []
        for district in districts:
            price_multiplier = 0.85 + random.random() * 0.4
            current_price = base_price * price_multiplier
            price_change = (random.random() - 0.5) * 15
            
            district_prices.append({
                'district': district,
                'current_price': round(current_price, 2),
                'price_change': round(price_change, 2),
                'trend': 'up' if price_change > 0 else 'down',
                'market_volume': random.randint(200, 1500),
                'last_updated': datetime.now().isoformat()
            })
        
        district_prices.sort(key=lambda x: x['current_price'], reverse=True)
        return district_prices[:5]
        
    def get_tamilnadu_crop_distribution(self):
        """Get Tamil Nadu district-wise crop distribution data"""
        district_data = []
        
        for district, data in TAMIL_NADU_CROP_DATA.items():
            crops = {k: v for k, v in data.items() if k not in ['total_area', 'productivity']}
            dominant_crop = max(crops, key=crops.get)
            dominant_percentage = crops[dominant_crop]
            
            district_data.append({
                'district': district,
                'dominant_crop': dominant_crop,
                'dominant_percentage': dominant_percentage,
                'crop_distribution': crops,
                'total_area': data['total_area'],
                'productivity_score': data['productivity']
            })
        
        return sorted(district_data, key=lambda x: x['dominant_percentage'], reverse=True)