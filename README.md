# Crop Prediction Backend 🌾

An AI-based crop demand forecasting and price prediction system with comprehensive Indian agricultural data, real-time market monitoring, and state-wise crop analysis.

## Features

- **AI-Powered Predictions**: Uses machine learning models to predict crop demand and prices
- **Real-time Dashboard**: Live market rates, crop health monitoring, and alerts
- **Hierarchical Location Data**: State → District → City selection with 10+ Indian states
- **Tamil Nadu Crop Analysis**: District-wise crop distribution with cultivation percentages
- **Top Districts by Price**: Compare crop prices across districts in any state
- **Market Monitoring**: Live price tracking for 25+ crops with trend analysis
- **Event-based Adjustments**: Automatically adjusts predictions based on disasters and market changes
- **RESTful API**: Clean API endpoints for frontend integration

## Project Structure

```
crop_prediction_backend/
├── app.py                 # Main Flask application with dashboard endpoints
├── ai_predictor.py        # AI prediction models and logic
├── data_manager.py        # Data storage and management
├── news_monitor.py        # Event monitoring and news analysis
├── dashboard_service.py   # Real-time dashboard data service
├── location_data.py       # Indian states, districts, and cities data
├── crop_data.py          # Comprehensive crop and price data
├── setup.py              # Project setup script
├── requirements.txt       # Python dependencies
├── test_endpoints.py      # API testing script
├── README.md             # This file
└── data/                 # Data storage directory (created automatically)
```

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**
2. **Navigate to the project directory**
   ```bash
   cd crop_prediction_backend
   ```

3. **Run the setup script**
   ```bash
   python setup.py
   ```
   This will:
   - Check Python version
   - Create virtual environment
   - Install all dependencies
   - Create necessary directories

4. **Activate the virtual environment**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

5. **Start the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## API Endpoints

### Dashboard Endpoints

#### 1. Get Live Market Rates
**GET** `/api/dashboard/market-rates`

Get current market prices for major crops.

**Response:**
```json
{
  "market_rates": [
    {
      "crop": "wheat",
      "current_price": 26.50,
      "price_change": 2.3,
      "trend": "up",
      "market": "Local Mandi",
      "last_updated": "2024-12-19T10:30:00"
    }
  ]
}
```

#### 2. Get Crop Health Summary
**GET** `/api/dashboard/crop-health`

Get satellite-based crop health data with NDVI scores.

**Response:**
```json
{
  "crop_health": [
    {
      "crop": "wheat",
      "ndvi_score": 0.75,
      "health_score": 85,
      "status": "Excellent",
      "color": "green",
      "area_hectares": 250,
      "last_satellite_pass": "2024-12-19T08:00:00"
    }
  ]
}
```

#### 3. Get Top Districts by Price
**GET** `/api/dashboard/top-districts?state={state}&crop={crop}`

Get top 5 districts with highest prices for a specific crop in a state.

**Parameters:**
- `state`: State name (e.g., "Maharashtra")
- `crop`: Crop name (e.g., "wheat")

**Response:**
```json
{
  "top_districts": [
    {
      "district": "Mumbai",
      "current_price": 28.50,
      "price_change": 5.2,
      "trend": "up",
      "market_volume": 850,
      "last_updated": "2024-12-19T10:30:00"
    }
  ]
}
```

#### 4. Get Tamil Nadu Crop Distribution
**GET** `/api/dashboard/tamilnadu-crops`

Get district-wise crop distribution data for Tamil Nadu.

**Response:**
```json
{
  "tamilnadu_crops": [
    {
      "district": "Thanjavur",
      "dominant_crop": "rice",
      "dominant_percentage": 65,
      "crop_distribution": {
        "rice": 65,
        "sugarcane": 20,
        "banana": 10,
        "coconut": 5
      },
      "total_area": 180000,
      "productivity_score": 92
    }
  ]
}
```

#### 5. Get Market Alerts
**GET** `/api/dashboard/alerts`

Get current market alerts and notifications.

### Location Endpoints

#### 6. Get States List
**GET** `/api/locations/states`

#### 7. Get Districts by State
**GET** `/api/locations/districts/{state}`

#### 8. Get Cities by State and District
**GET** `/api/locations/cities/{state}/{district}`

### Prediction Endpoints

### Prediction Endpoints

#### 9. Get Crop Predictions
**POST** `/api/predict`

Get demand and price predictions for a specific crop in a location.

**Request Body:**
```json
{
  "state": "Maharashtra",
  "district": "Mumbai",
  "city": "Mumbai City",
  "crop": "wheat"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "state": "Maharashtra",
    "district": "Mumbai",
    "city": "Mumbai City",
    "crop": "wheat",
    "year": 2024,
    "current_month": 12,
    "demand_data": [
      {
        "month": 1,
        "value": 2847.32,
        "percentage": 94.91,
        "is_historical": true,
        "event": null
      }
    ],
    "price_data": [
      {
        "month": 1,
        "value": 28.45,
        "percentage": 113.8,
        "is_historical": true,
        "event": null
      }
    ],
    "base_demand": 3000,
    "base_price": 25,
    "last_updated": "2024-12-19T10:30:00"
  }
}
```

#### 10. Manual Adjustment
**POST** `/api/manual_adjust`

Manually adjust demand or price values for demonstration purposes.

**Request Body:**
```json
{
  "state": "Maharashtra",
  "district": "Mumbai",
  "city": "Mumbai City",
  "crop": "wheat",
  "month": 6,
  "demand_change": 15.5,
  "price_change": -8.2
}
```

#### 11. Health Check
**GET** `/api/health`

Check API health and status.

## Data Structure Explanation

### Demand/Price Data Points
Each month contains:
- `month`: Month number (1-12)
- `value`: Actual demand/price value
- `percentage`: Percentage relative to base value
- `is_historical`: Whether this is historical data or prediction
- `event`: Name of event affecting this month (if any)

### Event Types
- **disaster**: Natural disasters (drought, flood, pest attacks)
- **economic**: Economic factors (fuel prices, market changes)
- **positive**: Positive events (good weather, subsidies)

## Key Components

### 1. Dashboard Service (`dashboard_service.py`)
- Real-time market rate monitoring for 25+ crops
- Satellite-based crop health analysis with NDVI scores
- Tamil Nadu district-wise crop distribution data
- Top districts price comparison across Indian states
- Market alerts and notifications system

### 2. Location Data (`location_data.py` & `crop_data.py`)
- Comprehensive Indian geographical data (10 states, 80+ districts, 250+ cities)
- Real agricultural statistics for Tamil Nadu (15 districts)
- Current market prices for 30+ crops
- State-wise major crop information

### 3. AI Predictor (`ai_predictor.py`)
- Uses scikit-learn for machine learning models
- Implements seasonal patterns and trend analysis
- Handles event-based adjustments
- Provides manual adjustment capabilities

### 4. Data Manager (`data_manager.py`)
- Manages historical data storage
- Creates realistic sample data
- Handles data persistence
- Provides statistical analysis

### 5. News Monitor (`news_monitor.py`)
- Simulates event monitoring
- Manages current events
- Provides event impact analysis
- Supports manual event addition

## Customization

### Adding New Crops
Edit the `crops` list in `data_manager.py` and `ai_predictor.py`:
```python
crops = ['wheat', 'rice', 'corn', 'your_new_crop']
```

### Adding New Districts
Edit the `districts` list in `data_manager.py`:
```python
districts = ['Mumbai', 'Delhi', 'your_new_district']
```

### Adjusting Update Frequency
Change the schedule in `app.py`:
```python
schedule.every(5).minutes.do(update_predictions)  # Change 5 to desired minutes
```

## Frontend Integration

The API is designed to work with React.js frontend. Key integration points:

1. **CORS enabled** for cross-origin requests
2. **JSON responses** for easy parsing
3. **Real-time updates** via polling or WebSocket (can be added)
4. **Event information** for displaying alerts

### Sample Frontend Usage
```javascript
// Get predictions
const response = await fetch('http://localhost:5000/api/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ district: 'Mumbai', crop: 'wheat' })
});
const data = await response.json();

// Use data.demand_data and data.price_data for graphs
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change port in `app.py`: `app.run(port=5001)`

2. **Dependencies not installing**
   - Ensure Python 3.8+ is installed
   - Try: `pip install --upgrade pip`

3. **Virtual environment issues**
   - Delete `venv` folder and run setup again

4. **Data not persisting**
   - Check if `data` directory has write permissions

## Development

### Adding New Features
1. Create new modules following the existing pattern
2. Add API endpoints in `app.py`
3. Update this README with new endpoints

### Testing
```bash
# Test API endpoints
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"district":"Mumbai","crop":"wheat"}'
```

## Production Deployment

For production deployment:
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up proper database (PostgreSQL, MongoDB)
3. Implement real news API integration
4. Add authentication and rate limiting
5. Use environment variables for configuration

## License

This project is created for educational and prototype purposes.

## Support

For questions or issues, please check the troubleshooting section or create an issue in the project repository.