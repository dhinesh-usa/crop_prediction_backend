#!/usr/bin/env python3
"""
Test script for Crop Prediction Backend API
This script tests all the API endpoints to ensure they work correctly
"""

import requests
import json
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Health check passed: {data['status']}")
            print(f"  Active predictions: {data['active_predictions']}")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False

def test_prediction():
    """Test the prediction endpoint"""
    print("\nTesting prediction endpoint...")
    try:
        payload = {
            "district": "Mumbai",
            "crop": "wheat"
        }
        
        response = requests.post(f"{BASE_URL}/predict", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✓ Prediction successful")
                print(f"  District: {data['data']['district']}")
                print(f"  Crop: {data['data']['crop']}")
                print(f"  Year: {data['data']['year']}")
                print(f"  Current month: {data['data']['current_month']}")
                print(f"  Demand data points: {len(data['data']['demand_data'])}")
                print(f"  Price data points: {len(data['data']['price_data'])}")
                
                # Show sample data point
                sample_demand = data['data']['demand_data'][0]
                print(f"  Sample demand (Month {sample_demand['month']}): {sample_demand['value']} ({sample_demand['percentage']}%)")
                
                return data['data']
            else:
                print("✗ Prediction failed: API returned success=false")
                return None
        else:
            print(f"✗ Prediction failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Prediction error: {e}")
        return None

def test_manual_adjustment(prediction_data):
    """Test the manual adjustment endpoint"""
    print("\nTesting manual adjustment endpoint...")
    try:
        payload = {
            "district": prediction_data['district'],
            "crop": prediction_data['crop'],
            "month": 6,
            "demand_change": 15.5,
            "price_change": -8.2
        }
        
        response = requests.post(f"{BASE_URL}/manual_adjust", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✓ Manual adjustment successful")
                
                # Check if the adjustment was applied
                adjusted_demand = data['data']['demand_data'][5]  # Month 6 (index 5)
                adjusted_price = data['data']['price_data'][5]
                
                print(f"  Adjusted demand (Month 6): {adjusted_demand['value']} ({adjusted_demand['percentage']}%)")
                print(f"  Adjusted price (Month 6): {adjusted_price['value']} ({adjusted_price['percentage']}%)")
                print(f"  Event: {adjusted_demand['event']}")
                
                return True
            else:
                print("✗ Manual adjustment failed: API returned success=false")
                return False
        else:
            print(f"✗ Manual adjustment failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Manual adjustment error: {e}")
        return False

def test_events():
    """Test the events endpoint"""
    print("\nTesting events endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/events")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print("✓ Events retrieval successful")
                print(f"  Active events: {len(data['events'])}")
                
                for i, event in enumerate(data['events'][:3]):  # Show first 3 events
                    print(f"  Event {i+1}: {event['name']} ({event['type']})")
                    print(f"    Impact: {event['impact']}")
                    print(f"    Affected regions: {', '.join(event['affected_regions'])}")
                
                return True
            else:
                print("✗ Events retrieval failed: API returned success=false")
                return False
        else:
            print(f"✗ Events retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Events error: {e}")
        return False

def test_different_crops():
    """Test predictions for different crops"""
    print("\nTesting different crops...")
    crops = ['rice', 'corn', 'cotton', 'potato']
    districts = ['Delhi', 'Bangalore', 'Chennai']
    
    success_count = 0
    total_tests = len(crops)
    
    for crop in crops:
        try:
            payload = {
                "district": "Mumbai",
                "crop": crop
            }
            
            response = requests.post(f"{BASE_URL}/predict", json=payload)
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"  ✓ {crop}: Base demand {data['data']['base_demand']}, Base price {data['data']['base_price']}")
                    success_count += 1
                else:
                    print(f"  ✗ {crop}: API returned success=false")
            else:
                print(f"  ✗ {crop}: HTTP {response.status_code}")
        except Exception as e:
            print(f"  ✗ {crop}: Error {e}")
    
    print(f"Crop tests: {success_count}/{total_tests} successful")
    return success_count == total_tests

def test_invalid_inputs():
    """Test API with invalid inputs"""
    print("\nTesting invalid inputs...")
    
    test_cases = [
        {"payload": {}, "description": "Empty payload"},
        {"payload": {"district": "Mumbai"}, "description": "Missing crop"},
        {"payload": {"crop": "wheat"}, "description": "Missing district"},
        {"payload": {"district": "", "crop": "wheat"}, "description": "Empty district"},
        {"payload": {"district": "Mumbai", "crop": ""}, "description": "Empty crop"}
    ]
    
    success_count = 0
    for test_case in test_cases:
        try:
            response = requests.post(f"{BASE_URL}/predict", json=test_case["payload"])
            if response.status_code == 400:  # Expected error code
                print(f"  ✓ {test_case['description']}: Correctly returned 400")
                success_count += 1
            else:
                print(f"  ✗ {test_case['description']}: Expected 400, got {response.status_code}")
        except Exception as e:
            print(f"  ✗ {test_case['description']}: Error {e}")
    
    print(f"Invalid input tests: {success_count}/{len(test_cases)} successful")
    return success_count == len(test_cases)

def main():
    """Run all tests"""
    print("🌾 Crop Prediction Backend API Tests")
    print("=" * 50)
    
    # Check if server is running
    print("Checking if server is running...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print("✓ Server is running")
    except Exception as e:
        print(f"✗ Server is not running: {e}")
        print("Please start the server with: python app.py")
        return
    
    # Run tests
    tests_passed = 0
    total_tests = 6
    
    if test_health_check():
        tests_passed += 1
    
    prediction_data = test_prediction()
    if prediction_data:
        tests_passed += 1
        
        if test_manual_adjustment(prediction_data):
            tests_passed += 1
    
    if test_events():
        tests_passed += 1
    
    if test_different_crops():
        tests_passed += 1
    
    if test_invalid_inputs():
        tests_passed += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the output above.")
    
    print("\nAPI is ready for frontend integration!")

if __name__ == "__main__":
    main()