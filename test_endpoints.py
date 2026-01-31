"""
Test script to verify backend endpoints are working
"""
import requests
import json

BASE_URL = 'http://localhost:5000'

def test_endpoints():
    print("Testing Backend Endpoints...")
    
    # Test Tamil Nadu crops
    print("\n1. Testing Tamil Nadu Crops:")
    try:
        response = requests.get(f'{BASE_URL}/api/dashboard/tamilnadu-crops')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Districts found: {len(data.get('tamilnadu_crops', []))}")
            if data.get('tamilnadu_crops'):
                print(f"Sample district: {data['tamilnadu_crops'][0]}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test Top Districts
    print("\n2. Testing Top Districts:")
    try:
        response = requests.get(f'{BASE_URL}/api/dashboard/top-districts?state=Maharashtra&crop=wheat')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Top districts found: {len(data.get('top_districts', []))}")
            if data.get('top_districts'):
                print(f"Sample district: {data['top_districts'][0]}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test Market Rates
    print("\n3. Testing Market Rates:")
    try:
        response = requests.get(f'{BASE_URL}/api/dashboard/market-rates')
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Market rates found: {len(data.get('market_rates', []))}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_endpoints()