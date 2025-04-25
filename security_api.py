from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import time
from datetime import datetime

app = Flask(__name__)

try:
    cred = credentials.Certificate("findmyspot-ecac4-firebase-adminsdk-fbsvc-a75400238f.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://findmyspot-ecac4-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })
    print("firebase init success")
except Exception as e:
    print(f"firebase init failed: {e}")

@app.route('/check_plate', methods=['POST'])
def check_plate():
    """
    checking kung valid face and plate number
    
    JSON format:
    {
        "plate_number": "PLATE000",
        "face_name": "Mark"
    }
    """
    data = request.get_json()
    
    if not data or 'plate_number' not in data or 'face_name' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    plate_number = data['plate_number']
    face_name = data['face_name']
    
    print(f"Checking security match for plate {plate_number}, driver: {face_name}")
    
    try:
        users_ref = db.reference('/users')
        users = users_ref.get() or {}
        
        plate_found = False
        registered_driver = None
        vehicle_type = None
        vehicle_color = None
        
        for user_id, user_info in users.items():
            if 'plateNumber' in user_info and user_info['plateNumber'].strip().upper() == plate_number.strip().upper():
                plate_found = True
                registered_driver = user_info.get('fullName', 'Unknown')
                vehicle_type = user_info.get('vehicleType', 'Unknown')
                vehicle_color = user_info.get('vehicleColor', 'Unknown')
                break
        
        if plate_found:
            is_match = face_name.strip().upper() == registered_driver.strip().upper()
            
            if not is_match:
                try:
                    alerts_ref = db.reference('/security_alerts')
                    alerts_ref.push({
                        'plate_number': plate_number,
                        'registered_driver': registered_driver,
                        'detected_driver': face_name,
                        'timestamp': datetime.now().isoformat(),
                        'vehicle_type': vehicle_type,
                        'vehicle_color': vehicle_color,
                        'resolved': False
                    })
                    print(f"Plate {plate_number} registered to {registered_driver} but driven by {face_name}")
                except Exception as e:
                    print(f"Failed: {e}")
            
            return jsonify({
                'match': is_match,
                'registered_driver': registered_driver,
                'vehicle_details': {
                    'type': vehicle_type,
                    'color': vehicle_color
                }
            })
        else:
            return jsonify({
                'match': False,
                'error': 'Plate not registered in system'
            })
    except Exception as e:
        print(f"Error checking plate: {e}")
        return jsonify({
            'error': f"Internal server error: {str(e)}"
        }), 500

@app.route('/vehicles', methods=['GET'])
def list_vehicles():
    """
    list all vehicles info
    """
    try:
        users_ref = db.reference('/users')
        users = users_ref.get() or {}
        
        vehicles = []
        for user_id, user_info in users.items():
            if 'plateNumber' in user_info:
                vehicles.append({
                    'plate_number': user_info.get('plateNumber', ''),
                    'driver_name': user_info.get('fullName', ''),
                    'vehicle_type': user_info.get('vehicleType', ''),
                    'vehicle_color': user_info.get('vehicleColor', ''),
                    'contact': user_info.get('contactNumber', '')
                })
        
        return jsonify({'vehicles': vehicles})
    except Exception as e:
        print(f"Error fetching vehicles: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/alerts', methods=['GET'])
def list_alerts():
    """
    list security alerts
    """
    try:
        alerts_ref = db.reference('/security_alerts')
        alerts = alerts_ref.get() or {}
        
        formatted_alerts = []
        for alert_id, alert in alerts.items():
            alert_copy = alert.copy() if alert else {}
            alert_copy['id'] = alert_id
            formatted_alerts.append(alert_copy)
            
        return jsonify({'alerts': formatted_alerts})
    except Exception as e:
        print(f"Error fetching alerts: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/alerts/<alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    """
    mark alert as resolved
    """
    try:
        alert_ref = db.reference(f'/security_alerts/{alert_id}')
        alert = alert_ref.get()
        
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        
        alert_ref.update({
            'resolved': True,
            'resolved_at': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'message': 'Alert marked as resolved'
        })
    except Exception as e:
        print(f"Error resolving alert: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting Security API Server...")
    app.run(debug=True, host='0.0.0.0', port=5000)