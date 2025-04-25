import requests
import json
import os
from datetime import datetime

def test_security_api():
    """
    unit test for the security API
    """
    print("Testing Security API...\n")
    
    test_cases = [
        {"plate_number": "NJJZ 678", "face_name": "SHUA", "expected_match": True, "desc": "Matching plate and face"},
        {"plate_number": "NJJZ 678", "face_name": "Magnanakaw", "expected_match": False, "desc": "Plate with different face"},
        {"plate_number": "NJJZ 420", "face_name": "SHUA", "expected_match": False, "desc": "Face with different plate"},
    ]
    
    api_url = "http://localhost:5000/check_plate"
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['desc']}")
        print(f"Checking plate '{test['plate_number']}' with driver '{test['face_name']}'")
        
        try:
            response = requests.post(
                api_url,
                json={"plate_number": test["plate_number"], "face_name": test["face_name"]},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                is_match = result.get("match", None)
                
                print(f"API Response: {json.dumps(result, indent=2)}")
                print(f"Security Match: {'pass' if is_match else 'fail'}")
                
                if is_match == test["expected_match"]:
                    print(f"PASSED: Expected match={test['expected_match']}, got match={is_match}")
                else:
                    print(f"FAILED: Expected match={test['expected_match']}, got match={is_match}")
            else:
                print(f"API Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Connection error: {e}")
    
    print("\n\ntest list vehicles info endpoint")
    try:
        response = requests.get("http://localhost:5000/vehicles")
        if response.status_code == 200:
            vehicles = response.json().get("vehicles", [])
            print(f"Found {len(vehicles)} registered vehicles:")
            for v in vehicles:
                print(f"- Plate: {v['plate_number']} | Driver: {v['driver_name']} | {v['vehicle_color']} {v['vehicle_type']}")
        else:
            print(f"API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection error: {e}")
    
    print("\n\ntest list security alerts endpoint")
    try:
        response = requests.get("http://localhost:5000/alerts")
        if response.status_code == 200:
            alerts = response.json().get("alerts", [])
            print(f"Found {len(alerts)} security alerts:")
            for a in alerts:
                print(f"- Plate: {a.get('plate_number')} | Registered to: {a.get('registered_driver')} | Detected: {a.get('detected_driver')}")
        else:
            print(f"API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection error: {e}")

def test_resolve_alert():
    """
    unit test for the alert resolution endpoint
    """

    try:
        response = requests.get("http://localhost:5000/alerts")
        
        if response.status_code == 200:
            alerts = response.json().get('alerts', [])
            
            if not alerts:
                print("No alerts to resolve. Creating a test alert first...")
                test_response = requests.post(
                    "http://localhost:5000/check_plate",
                    json={"plate_number": "NJJZ 678", "face_name": "Unauthorized User"},
                    headers={"Content-Type": "application/json"}
                )
                
                if test_response.status_code != 200:
                    print(f"Failed to create test alert: {test_response.text}")
                    return
                
                response = requests.get("http://localhost:5000/alerts")
                if response.status_code == 200:
                    alerts = response.json().get('alerts', [])
                else:
                    print(f"Failed to get alerts after creating test alert: {response.text}")
                    return
            
            unresolved_alerts = [alert for alert in alerts if not alert.get('resolved', False)]
            
            if unresolved_alerts:
                alert_to_resolve = unresolved_alerts[0]
                alert_id = alert_to_resolve.get('id')
                
                print(f"Attempting to resolve alert {alert_id}...")
                
                resolve_response = requests.post(f"http://localhost:5000/alerts/{alert_id}/resolve")
                
                if resolve_response.status_code == 200:
                    result = resolve_response.json()
                    print(f"✅ Success: {result.get('message')}")
                    
                    verify_response = requests.get("http://localhost:5000/alerts")
                    if verify_response.status_code == 200:
                        updated_alerts = verify_response.json().get('alerts', [])
                        updated_alert = next((a for a in updated_alerts if a.get('id') == alert_id), None)
                        
                        if updated_alert and updated_alert.get('resolved') == True:
                            print("Alert was successfully marked as resolved in database")
                        else:
                            print("Alert may not have been updated correctly")
                    else:
                        print(f"Could not verify update: {verify_response.text}")
                else:
                    print(f"Failed to resolve alert: {resolve_response.status_code} - {resolve_response.text}")
            else:
                print("No unresolved alerts found to test with")
        else:
            print(f"Failed to get alerts: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error testing alert resolution: {e}")

if __name__ == "__main__":
    test_security_api()
    test_resolve_alert()