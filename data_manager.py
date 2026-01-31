import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

class DataManager:
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_directory()
        self.historical_data = {}
        self.load_historical_data()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def load_historical_data(self):
        """Load historical data from files or create sample data"""
        historical_file = os.path.join(self.data_dir, "historical_data.json")
        
        if os.path.exists(historical_file):
            with open(historical_file, 'r') as f:
                self.historical_data = json.load(f)
        else:
            self.create_sample_historical_data()
            self.save_historical_data()
    
    def create_sample_historical_data(self):
        """Create sample historical data for different crops and districts"""
        crops = ['wheat', 'rice', 'corn', 'cotton', 'sugarcane', 'potato', 'tomato', 'onion', 'garlic', 'soybean']
        districts = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
        
        current_year = datetime.now().year
        
        for crop in crops:
            for district in districts:
                key = f"{district}_{crop}"
                
                # Generate 3 years of historical data
                yearly_data = []
                for year in range(current_year - 3, current_year):
                    monthly_data = self.generate_monthly_data(crop, district, year)
                    yearly_data.extend(monthly_data)
                
                self.historical_data[key] = yearly_data
    
    def generate_monthly_data(self, crop, district, year):
        """Generate realistic monthly data for a crop in a district"""
        # Base values vary by crop type
        crop_base_values = {
            'wheat': {'demand': 3000, 'price': 25},
            'rice': {'demand': 4000, 'price': 30},
            'corn': {'demand': 2500, 'price': 20},
            'cotton': {'demand': 1500, 'price': 60},
            'sugarcane': {'demand': 5000, 'price': 15},
            'potato': {'demand': 3500, 'price': 12},
            'tomato': {'demand': 2000, 'price': 25},
            'onion': {'demand': 2800, 'price': 18},
            'garlic': {'demand': 800, 'price': 80},
            'soybean': {'demand': 2200, 'price': 45}
        }
        
        base_demand = crop_base_values.get(crop, {'demand': 2500, 'price': 35})['demand']
        base_price = crop_base_values.get(crop, {'demand': 2500, 'price': 35})['price']
        
        monthly_data = []
        
        for month in range(1, 13):
            # Seasonal patterns
            seasonal_demand = 1 + 0.3 * np.sin(2 * np.pi * (month - 3) / 12)
            seasonal_price = 1 + 0.2 * np.cos(2 * np.pi * (month - 6) / 12)
            
            # Random variations
            demand_variation = np.random.uniform(0.8, 1.2)
            price_variation = np.random.uniform(0.9, 1.1)
            
            # Calculate final values
            demand = base_demand * seasonal_demand * demand_variation
            price = base_price * seasonal_price * price_variation
            
            monthly_data.append({
                'year': year,
                'month': month,
                'demand': round(demand, 2),
                'price': round(price, 2),
                'timestamp': datetime(year, month, 15).isoformat()
            })
        
        return monthly_data
    
    def save_historical_data(self):
        """Save historical data to file"""
        historical_file = os.path.join(self.data_dir, "historical_data.json")
        with open(historical_file, 'w') as f:
            json.dump(self.historical_data, f, indent=2)
    
    def get_historical_data(self, district, crop, years=3):
        """Get historical data for a specific crop and district"""
        key = f"{district}_{crop}"
        
        if key in self.historical_data:
            current_year = datetime.now().year
            filtered_data = [
                data for data in self.historical_data[key]
                if data['year'] >= (current_year - years)
            ]
            return filtered_data
        
        return []
    
    def add_real_time_data(self, district, crop, demand, price):
        """Add real-time data point"""
        key = f"{district}_{crop}"
        current_time = datetime.now()
        
        data_point = {
            'year': current_time.year,
            'month': current_time.month,
            'demand': demand,
            'price': price,
            'timestamp': current_time.isoformat(),
            'is_real_time': True
        }
        
        if key not in self.historical_data:
            self.historical_data[key] = []
        
        self.historical_data[key].append(data_point)
        self.save_historical_data()
    
    def get_crop_list(self):
        """Get list of available crops"""
        crops = set()
        for key in self.historical_data.keys():
            district, crop = key.split('_', 1)
            crops.add(crop)
        return sorted(list(crops))
    
    def get_district_list(self):
        """Get list of available districts"""
        districts = set()
        for key in self.historical_data.keys():
            district, crop = key.split('_', 1)
            districts.add(district)
        return sorted(list(districts))
    
    def get_statistics(self, district, crop):
        """Get statistical information for a crop in a district"""
        historical_data = self.get_historical_data(district, crop)
        
        if not historical_data:
            return None
        
        demands = [d['demand'] for d in historical_data]
        prices = [d['price'] for d in historical_data]
        
        return {
            'demand_stats': {
                'mean': np.mean(demands),
                'std': np.std(demands),
                'min': np.min(demands),
                'max': np.max(demands)
            },
            'price_stats': {
                'mean': np.mean(prices),
                'std': np.std(prices),
                'min': np.min(prices),
                'max': np.max(prices)
            },
            'data_points': len(historical_data)
        }