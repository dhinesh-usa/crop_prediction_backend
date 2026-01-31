import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import random

class AIPredictor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.demand_model = LinearRegression()
        self.price_model = LinearRegression()
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        
        # Initialize with some base data for different crops and districts
        self.base_data = self._initialize_base_data()
        self._train_models()
    
    def _initialize_base_data(self):
        """Initialize base historical data for training"""
        crops = ['wheat', 'rice', 'corn', 'cotton', 'sugarcane', 'potato', 'tomato']
        districts = ['district1', 'district2', 'district3', 'district4', 'district5']
        
        data = {}
        for crop in crops:
            for district in districts:
                # Generate realistic seasonal patterns
                base_demand = random.uniform(1000, 5000)
                base_price = random.uniform(20, 100)
                
                monthly_data = []
                for month in range(1, 13):
                    # Seasonal variations
                    seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * month / 12)
                    
                    demand = base_demand * seasonal_factor * random.uniform(0.8, 1.2)
                    price = base_price * (2 - seasonal_factor) * random.uniform(0.9, 1.1)
                    
                    monthly_data.append({
                        'month': month,
                        'demand': demand,
                        'price': price,
                        'year': self.current_year - 1
                    })
                
                data[f"{district}_{crop}"] = monthly_data
        
        return data
    
    def _train_models(self):
        """Train the AI models with historical data"""
        all_features = []
        all_demands = []
        all_prices = []
        
        for key, monthly_data in self.base_data.items():
            for data_point in monthly_data:
                # Features: month, seasonal patterns, trend
                features = [
                    data_point['month'],
                    np.sin(2 * np.pi * data_point['month'] / 12),
                    np.cos(2 * np.pi * data_point['month'] / 12),
                    data_point['year']
                ]
                
                all_features.append(features)
                all_demands.append(data_point['demand'])
                all_prices.append(data_point['price'])
        
        X = np.array(all_features)
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        
        self.demand_model.fit(X_scaled, all_demands)
        self.price_model.fit(X_scaled, all_prices)
    
    def predict(self, district, crop):
        """Generate full year prediction for demand and price"""
        key = f"{district}_{crop}"
        
        # Get base data if available, otherwise use average
        if key in self.base_data:
            base_data = self.base_data[key]
            base_demand = np.mean([d['demand'] for d in base_data])
            base_price = np.mean([d['price'] for d in base_data])
        else:
            base_demand = 2500
            base_price = 50
        
        demand_data = []
        price_data = []
        events = []
        
        for month in range(1, 13):
            # Prepare features for prediction
            features = np.array([[
                month,
                np.sin(2 * np.pi * month / 12),
                np.cos(2 * np.pi * month / 12),
                self.current_year
            ]])
            
            features_scaled = self.scaler.transform(features)
            
            # Predict using AI models
            predicted_demand = self.demand_model.predict(features_scaled)[0]
            predicted_price = self.price_model.predict(features_scaled)[0]
            
            # Add some realistic variations
            demand_variation = random.uniform(0.95, 1.05)
            price_variation = random.uniform(0.95, 1.05)
            
            final_demand = predicted_demand * demand_variation
            final_price = predicted_price * price_variation
            
            # Determine if this is historical or predicted
            is_historical = month < self.current_month
            
            demand_data.append({
                'month': month,
                'value': round(final_demand, 2),
                'percentage': round((final_demand / base_demand) * 100, 2),
                'is_historical': is_historical,
                'event': None
            })
            
            price_data.append({
                'month': month,
                'value': round(final_price, 2),
                'percentage': round((final_price / base_price) * 100, 2),
                'is_historical': is_historical,
                'event': None
            })
        
        return {
            'district': district,
            'crop': crop,
            'year': self.current_year,
            'current_month': self.current_month,
            'demand_data': demand_data,
            'price_data': price_data,
            'base_demand': base_demand,
            'base_price': base_price,
            'last_updated': datetime.now().isoformat()
        }
    
    def get_updated_prediction(self, district, crop, events):
        """Update prediction with new events and data"""
        prediction = self.predict(district, crop)
        
        # Apply event-based adjustments
        for event in events:
            if event['type'] == 'disaster':
                # Increase demand, increase price
                for i in range(self.current_month - 1, 12):
                    if not prediction['demand_data'][i]['is_historical']:
                        prediction['demand_data'][i]['value'] *= 1.2
                        prediction['demand_data'][i]['percentage'] *= 1.2
                        prediction['demand_data'][i]['event'] = event['name']
                        
                        prediction['price_data'][i]['value'] *= 1.3
                        prediction['price_data'][i]['percentage'] *= 1.3
                        prediction['price_data'][i]['event'] = event['name']
            
            elif event['type'] == 'economic':
                # Affect prices more than demand
                for i in range(self.current_month - 1, 12):
                    if not prediction['price_data'][i]['is_historical']:
                        prediction['price_data'][i]['value'] *= event.get('impact', 1.1)
                        prediction['price_data'][i]['percentage'] *= event.get('impact', 1.1)
                        prediction['price_data'][i]['event'] = event['name']
        
        prediction['last_updated'] = datetime.now().isoformat()
        return prediction
    
    def apply_manual_adjustment(self, prediction_data, month, demand_change, price_change):
        """Apply manual adjustments for prototype demonstration"""
        month_idx = month - 1
        
        if 0 <= month_idx < 12:
            # Apply demand change
            if demand_change != 0:
                old_demand = prediction_data['demand_data'][month_idx]['value']
                new_demand = old_demand * (1 + demand_change / 100)
                prediction_data['demand_data'][month_idx]['value'] = round(new_demand, 2)
                prediction_data['demand_data'][month_idx]['percentage'] = round(
                    (new_demand / prediction_data['base_demand']) * 100, 2
                )
                prediction_data['demand_data'][month_idx]['event'] = 'Manual Adjustment'
            
            # Apply price change
            if price_change != 0:
                old_price = prediction_data['price_data'][month_idx]['value']
                new_price = old_price * (1 + price_change / 100)
                prediction_data['price_data'][month_idx]['value'] = round(new_price, 2)
                prediction_data['price_data'][month_idx]['percentage'] = round(
                    (new_price / prediction_data['base_price']) * 100, 2
                )
                prediction_data['price_data'][month_idx]['event'] = 'Manual Adjustment'
        
        prediction_data['last_updated'] = datetime.now().isoformat()
        return prediction_data