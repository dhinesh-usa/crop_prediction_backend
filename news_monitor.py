import requests
import random
from datetime import datetime, timedelta
import json

class NewsMonitor:
    def __init__(self):
        self.current_events = []
        self.event_history = []
        self.last_check = datetime.now()
        
        # Simulate some initial events for demonstration
        self.initialize_sample_events()
    
    def initialize_sample_events(self):
        """Initialize with sample events for demonstration"""
        sample_events = [
            {
                'id': 'drought_2024_1',
                'name': 'Drought in Western Region',
                'type': 'disaster',
                'impact': 1.3,
                'start_date': datetime.now() - timedelta(days=10),
                'end_date': datetime.now() + timedelta(days=30),
                'affected_regions': ['Mumbai', 'Pune', 'Ahmedabad'],
                'affected_crops': ['wheat', 'cotton', 'sugarcane'],
                'description': 'Severe drought conditions affecting crop yields'
            },
            {
                'id': 'flood_2024_1',
                'name': 'Flooding in Eastern States',
                'type': 'disaster',
                'impact': 1.4,
                'start_date': datetime.now() - timedelta(days=5),
                'end_date': datetime.now() + timedelta(days=15),
                'affected_regions': ['Kolkata', 'Hyderabad'],
                'affected_crops': ['rice', 'potato', 'tomato'],
                'description': 'Heavy flooding damaging standing crops'
            },
            {
                'id': 'economic_2024_1',
                'name': 'Fuel Price Increase',
                'type': 'economic',
                'impact': 1.15,
                'start_date': datetime.now() - timedelta(days=3),
                'end_date': datetime.now() + timedelta(days=60),
                'affected_regions': ['all'],
                'affected_crops': ['all'],
                'description': 'Rising fuel costs affecting transportation and farming costs'
            }
        ]
        
        # Add active events
        for event in sample_events:
            if event['start_date'] <= datetime.now() <= event['end_date']:
                self.current_events.append(event)
    
    def check_events(self):
        """Check for new events (simulated for prototype)"""
        current_time = datetime.now()
        
        # Remove expired events
        self.current_events = [
            event for event in self.current_events
            if event['end_date'] > current_time
        ]
        
        # Simulate random new events (for demonstration)
        if random.random() < 0.1:  # 10% chance of new event
            new_event = self.generate_random_event()
            self.current_events.append(new_event)
        
        self.last_check = current_time
        return self.current_events
    
    def generate_random_event(self):
        """Generate a random event for demonstration"""
        event_types = [
            {
                'type': 'disaster',
                'names': ['Unexpected Hailstorm', 'Pest Attack', 'Disease Outbreak', 'Water Shortage'],
                'impact_range': (1.2, 1.5)
            },
            {
                'type': 'economic',
                'names': ['Market Volatility', 'Export Demand Surge', 'Currency Fluctuation', 'Policy Change'],
                'impact_range': (1.1, 1.3)
            },
            {
                'type': 'positive',
                'names': ['Good Weather Forecast', 'New Farming Technology', 'Government Subsidy', 'Improved Seeds'],
                'impact_range': (0.8, 0.95)
            }
        ]
        
        event_type = random.choice(event_types)
        regions = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune', 'Ahmedabad']
        crops = ['wheat', 'rice', 'corn', 'cotton', 'sugarcane', 'potato', 'tomato', 'onion']
        
        event = {
            'id': f"{event_type['type']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'name': random.choice(event_type['names']),
            'type': event_type['type'],
            'impact': round(random.uniform(*event_type['impact_range']), 2),
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=random.randint(7, 45)),
            'affected_regions': random.sample(regions, random.randint(1, 3)),
            'affected_crops': random.sample(crops, random.randint(2, 5)),
            'description': f"Simulated {event_type['type']} event affecting crop predictions"
        }
        
        return event
    
    def get_current_events(self):
        """Get all current active events"""
        current_time = datetime.now()
        
        # Filter active events
        active_events = []
        for event in self.current_events:
            if event['start_date'] <= current_time <= event['end_date']:
                # Convert datetime objects to strings for JSON serialization
                event_copy = event.copy()
                event_copy['start_date'] = event['start_date'].isoformat()
                event_copy['end_date'] = event['end_date'].isoformat()
                active_events.append(event_copy)
        
        return active_events
    
    def get_events_for_region_crop(self, district, crop):
        """Get events affecting specific region and crop"""
        relevant_events = []
        
        for event in self.current_events:
            # Check if event affects this region
            if ('all' in event['affected_regions'] or 
                district in event['affected_regions']):
                
                # Check if event affects this crop
                if ('all' in event['affected_crops'] or 
                    crop in event['affected_crops']):
                    
                    relevant_events.append(event)
        
        return relevant_events
    
    def add_manual_event(self, event_data):
        """Add a manual event for testing purposes"""
        event = {
            'id': f"manual_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'name': event_data.get('name', 'Manual Event'),
            'type': event_data.get('type', 'manual'),
            'impact': event_data.get('impact', 1.1),
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=event_data.get('duration', 30)),
            'affected_regions': event_data.get('regions', ['all']),
            'affected_crops': event_data.get('crops', ['all']),
            'description': event_data.get('description', 'Manually added event for testing')
        }
        
        self.current_events.append(event)
        return event
    
    def simulate_news_api_call(self):
        """Simulate calling a news API (placeholder for real implementation)"""
        # In a real implementation, this would call actual news APIs
        # like NewsAPI, Google News API, or agricultural news sources
        
        # For now, return simulated news data
        simulated_news = [
            {
                'title': 'Weather Alert: Heavy Rains Expected',
                'content': 'Meteorological department predicts heavy rainfall in coming weeks',
                'relevance_score': 0.8,
                'event_type': 'weather'
            },
            {
                'title': 'Market Update: Crop Prices Fluctuate',
                'content': 'Agricultural commodity prices showing volatility due to global factors',
                'relevance_score': 0.7,
                'event_type': 'economic'
            }
        ]
        
        return simulated_news
    
    def analyze_news_for_events(self, news_data):
        """Analyze news data to extract relevant events"""
        # This would use NLP/AI to analyze news and extract relevant events
        # For prototype, we'll simulate this process
        
        events = []
        for news_item in news_data:
            if news_item['relevance_score'] > 0.7:
                event = self.convert_news_to_event(news_item)
                events.append(event)
        
        return events
    
    def convert_news_to_event(self, news_item):
        """Convert news item to event format"""
        return {
            'id': f"news_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'name': news_item['title'],
            'type': news_item['event_type'],
            'impact': 1.1,  # Default impact
            'start_date': datetime.now(),
            'end_date': datetime.now() + timedelta(days=14),
            'affected_regions': ['all'],
            'affected_crops': ['all'],
            'description': news_item['content'],
            'source': 'news_api'
        }