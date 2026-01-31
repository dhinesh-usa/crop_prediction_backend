from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import threading
import time
import schedule
from data_manager import DataManager
from ai_predictor import AIPredictor
from news_monitor import NewsMonitor
from location_data import get_states, get_districts, get_cities, get_all_locations
from dashboard_service import DashboardService

app = Flask(__name__)
CORS(app)

# Initialize components
data_manager = DataManager()
ai_predictor = AIPredictor()
news_monitor = NewsMonitor()
dashboard_service = DashboardService()

# Global variables for real-time updates
current_data = {}
last_update = datetime.now()

def update_predictions():
    """Update predictions every 5 minutes"""
    global current_data, last_update
    print(f"Updating predictions at {datetime.now()}")
    
    # Check for news events that might affect predictions
    events = news_monitor.check_events()
    
    # Update all active predictions
    for key in current_data:
        district, crop = key.split('_')
        current_data[key] = ai_predictor.get_updated_prediction(district, crop, events)
    
    last_update = datetime.now()

def run_scheduler():
    """Run the scheduler in a separate thread"""
    schedule.every(5).minutes.do(update_predictions)
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start scheduler thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

@app.route('/api/locations/states', methods=['GET'])
def get_states_list():
    """Get all Indian states"""
    return jsonify({'states': get_states()})

@app.route('/api/locations/districts/<string:state>', methods=['GET'])
def get_districts_list(state):
    """Get districts for a state"""
    districts = get_districts(state)
    return jsonify({'districts': districts})

@app.route('/api/locations/cities/<string:state>/<string:district>', methods=['GET'])
def get_cities_list(state, district):
    """Get cities for a state and district"""
    cities = get_cities(state, district)
    return jsonify({'cities': cities})

@app.route('/api/locations/all', methods=['GET'])
def get_all_locations_data():
    """Get all locations in hierarchical format"""
    return jsonify({'locations': get_all_locations()})

@app.route('/api/dashboard/market-rates', methods=['GET'])
def get_market_rates():
    """Get live market rates"""
    state = request.args.get('state')
    district = request.args.get('district')
    rates = dashboard_service.get_live_market_rates(state, district)
    return jsonify({'market_rates': rates})

@app.route('/api/dashboard/crop-health', methods=['GET'])
def get_crop_health():
    """Get crop health summary"""
    state = request.args.get('state')
    district = request.args.get('district')
    city = request.args.get('city')
    health_data = dashboard_service.get_crop_health_summary(state, district, city)
    return jsonify({'crop_health': health_data})

@app.route('/api/dashboard/weather', methods=['GET'])
def get_weather():
    """Get weather data and forecast"""
    state = request.args.get('state')
    district = request.args.get('district')
    city = request.args.get('city')
    weather_data = dashboard_service.get_weather_data(state, district, city)
    return jsonify({'weather': weather_data})

@app.route('/api/dashboard/alerts', methods=['GET'])
def get_alerts():
    """Get market alerts"""
    alerts = dashboard_service.get_market_alerts()
    return jsonify({'alerts': alerts})

@app.route('/api/dashboard/top-districts', methods=['GET'])
def get_top_districts():
    """Get top 5 districts with highest prices for a crop in a state"""
    state = request.args.get('state')
    crop = request.args.get('crop')
    
    if not state or not crop:
        return jsonify({'error': 'State and crop are required'}), 400
    
    top_districts = dashboard_service.get_top_districts_by_price(state, crop)
    return jsonify({'top_districts': top_districts})

@app.route('/api/dashboard/tamilnadu-crops', methods=['GET'])
def get_tamilnadu_crops():
    """Get Tamil Nadu district-wise crop distribution"""
    crop_data = dashboard_service.get_tamilnadu_crop_distribution()
    return jsonify({'tamilnadu_crops': crop_data})

@app.route('/api/predict', methods=['POST'])
def predict_crop():
    """Main prediction endpoint"""
    try:
        data = request.get_json()
        state = data.get('state')
        district = data.get('district')
        city = data.get('city')
        crop = data.get('crop')
        
        if not all([state, district, city, crop]):
            return jsonify({'error': 'State, district, city and crop are required'}), 400
        
        # Generate prediction using city as location identifier
        location_key = f"{state}-{district}-{city}"
        prediction_data = ai_predictor.predict(location_key, crop)
        prediction_data['state'] = state
        prediction_data['district'] = district
        prediction_data['city'] = city
        
        # Store in global data for updates
        key = f"{location_key}_{crop}"
        current_data[key] = prediction_data
        
        return jsonify({
            'success': True,
            'data': prediction_data,
            'last_update': last_update.isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/manual_adjust', methods=['POST'])
def manual_adjust():
    """Manual adjustment for prototype demonstration"""
    try:
        data = request.get_json()
        state = data.get('state')
        district = data.get('district')
        city = data.get('city')
        crop = data.get('crop')
        month = data.get('month')
        demand_change = data.get('demand_change', 0)
        price_change = data.get('price_change', 0)
        
        location_key = f"{state}-{district}-{city}"
        key = f"{location_key}_{crop}"
        if key in current_data:
            current_data[key] = ai_predictor.apply_manual_adjustment(
                current_data[key], month, demand_change, price_change
            )
            
            return jsonify({
                'success': True,
                'data': current_data[key]
            })
        else:
            return jsonify({'error': 'No active prediction found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get current events affecting predictions"""
    try:
        events = news_monitor.get_current_events()
        return jsonify({
            'success': True,
            'events': events
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'last_update': last_update.isoformat(),
        'active_predictions': len(current_data)
    })

if __name__ == '__main__':
    print("Starting Crop Prediction Backend...")
    print("Scheduler will update predictions every 5 minutes")
    app.run(debug=True, host='0.0.0.0', port=5000)