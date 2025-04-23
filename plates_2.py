import cv2
import easyocr
import time
import os
import re
import numpy as np
import threading
import queue
import mysql.connector
from datetime import datetime
from ultralytics import YOLO
from sklearn.preprocessing import LabelEncoder


def correct_perspective(image, license_plate_corners):
    if len(license_plate_corners) != 4:
        return image

    pts1 = np.float32(license_plate_corners)
    pts2 = np.float32([[0, 0], [300, 0], [300, 100], [0, 100]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    warped = cv2.warpPerspective(image, matrix, (300, 100))
    return warped


class PlateRecognizer:
    def __init__(self):
        # Plate detection model
        self.plate_model = YOLO('bestyolov8s(4feature).pt')

        self.reader = easyocr.Reader(['en'])
        self.detected_plates = []
        self.plate_queue = queue.Queue()
        self.detected_plate_counts = {}
        self.recent_plate_times = {}
        self.lock = threading.Lock()
        self.stop_event = threading.Event()
        self.vehicle_face_log_status = {}  
        self.vehicle_face_last_seen = {}
        self.vehicle_face_driver = {}  

        # Database Connection
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="plate_recognition", autocommit=True
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS plate_numbers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            plate_number VARCHAR(255) NOT NULL,
            vehicle_image VARCHAR(191),
            scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            date_time_scanned TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            detected TINYINT(1),
            car_color VARCHAR(50),
            location VARCHAR(100),
            vehicle_type VARCHAR(50),
            face_image_path VARCHAR(255),
            face_name VARCHAR(255),
            login_status VARCHAR(255),
            is_complete_record BOOLEAN DEFAULT FALSE
        )''')
        self.conn.commit()

        self.plate_patterns = [
            re.compile(r'^[0-9]{3}\s?[A-Z]{3}$'),
            re.compile(r'^[0-9]{6}$'),
            re.compile(r'^[0-9]{4}-[0-9]{7}$'),
            re.compile(r'^[0-9]{3}[A-Z]{3}$'),
            re.compile(r'^[0-9]{4}\s?[A-Z]{2}$'),
            re.compile(r'^[A-Z][0-9]{4}[A-Z]$'),
            re.compile(r'^[0-9]{2}-[A-Z]{4}$'),
            re.compile(r'^[0-9]{2}[A-Z]{4}$'),
            re.compile(r'^[A-Z]{3}\s?[0-9]{4}$'),
            re.compile(r'^[A-Z]{2}[0-9]{4}$'),
            re.compile(r'^[0-9]{1}$'),
            re.compile(r'^[0-9]{2}$')
        ]

        # Face recognition 
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.face_database_path = r"C:\Users\ESTRADA\.spyder-py3\face_database"  
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_names = []
        self.names = []
        self.load_face_recognizer()

        # Shared data between threads
        self.current_face_data = {'face_image_path': "", 'face_name': "Unknown"}
        self.current_plate_data = {'plate_text': "", 'plate_image': None}
        self.current_vehicle_data = {'vehicle_type': "Unknown", 'car_color': "Unknown"}
        self.current_face_frame = None
        self.current_plate_frame = None
        self.current_vehicle_frame = None

    def load_face_recognizer(self):
        face_images = []
        labels = []
        label_encoder = LabelEncoder()

        if os.path.exists(self.face_database_path):
            for folder in os.listdir(self.face_database_path):
                person_folder = os.path.join(self.face_database_path, folder)
                if os.path.isdir(person_folder):
                    for image_name in os.listdir(person_folder):
                        image_path = os.path.join(person_folder, image_name)
                        if image_name.endswith(".jpg") or image_name.endswith(".png"):
                            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                            if img is not None:
                                face_images.append(img)
                                labels.append(folder)  

            if labels:  
                self.face_names = label_encoder.fit_transform(labels)
                self.names = label_encoder.classes_
                self.face_recognizer.train(face_images, np.array(self.face_names))
                print(f" Trained face recognizer with {len(self.names)} individuals")
            else:
                print(" No face images found in database directory")
        else:
            print(" Face database directory not found")

    def recognize_face(self, gray, face_crop):
        try:
            face_crop_gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY) if len(face_crop.shape) == 3 else face_crop
            face_crop_gray = cv2.resize(face_crop_gray, (100, 100))
            label, confidence = self.face_recognizer.predict(face_crop_gray)
            if confidence < 100 and len(self.names) > 0:
                face_name = self.names[label]
            else:
                face_name = "Unknown"
            return face_name
        except Exception as e:
            print(f"Face recognition error: {e}")
            return "Unknown"

    def extract_plate_text(self, image):
        try:
            results = self.reader.readtext(image, detail=0)
            for text in results:
                text = re.sub(r'[^A-Z0-9-]', '', text.upper())
                if self.validate_plate(text):
                    return text
            return ""
        except Exception as e:
            print(f"Plate text extraction error: {e}")
            return ""

    def validate_plate(self, plate_text):
        return any(pattern.match(plate_text) for pattern in self.plate_patterns)

    def detect_vehicle_type(self, frame, x1, y1, x2, y2):
        try:
            vehicle_crop = frame[y1:y2, x1:x2]
            results = self.plate_model(vehicle_crop)

            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    if conf > 0.5:
                        vehicle_type = self.plate_model.names[cls_id]
                        return vehicle_type.capitalize()
            return "Unknown"
        except Exception as e:
            print(f"Vehicle type detection error: {e}")
            height = y2 - y1
            width = x2 - x1
            area = height * width
            if area < 5000:
                return "Motorcycle"
            elif 5000 <= area < 15000:
                return "Car"
            elif 15000 <= area < 30000:
                return "SUV/Truck"
            else:
                return "Large Vehicle"

    def detect_color(self, image, x1, y1, x2, y2):
        """Detect the dominant color of the vehicle in the region defined by the coordinates."""
        vehicle_region = image[y1:y2, x1:x2]
        
        # Convert the image to HSV (Hue, Saturation, Value) color space
        hsv = cv2.cvtColor(vehicle_region, cv2.COLOR_BGR2HSV)
        
        # Define color ranges for common car colors
        colors = {
            "Red": [(0, 120, 70), (10, 255, 255)],
            #"Green": [(36, 50, 70), (89, 255, 255)],
            "Blue": [(90, 50, 70), (128, 255, 255)],
            #"Yellow": [(25, 50, 70), (35, 255, 255)],
            "Black": [(0, 0, 0), (180, 255, 50)],
            "White": [(0, 0, 200), (180, 60, 255)],
            "Gray": [(0, 0, 100), (180, 20, 190)],
            "Silver": [(0, 0, 150), (180, 20, 230)]
        }
        
        # Iterate through the color ranges and check if the dominant color is present
        for color_name, (lower, upper) in colors.items():
            lower_bound = np.array(lower)
            upper_bound = np.array(upper)
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            color_region = cv2.bitwise_and(vehicle_region, vehicle_region, mask=mask)
            
            # Check the percentage of pixels in the region that match the color
            color_percentage = np.sum(mask) / (mask.shape[0] * mask.shape[1])
            if color_percentage > 0.1:  # If more than 10% of the region matches the color
                return color_name
        
        return "Unknown"  # If no dominant color was found

    def confirm_plate(self, plate_text, car_color, location, vehicle_type, face_image_path, face_name):
        if (plate_text and car_color != "Unknown" and vehicle_type != "Unknown" and face_name != "Unknown"):
            if plate_text not in self.detected_plate_counts:
                self.detected_plate_counts[plate_text] = 1
            else:
                self.detected_plate_counts[plate_text] += 1
            if self.detected_plate_counts[plate_text] >= 3:
                last_seen = self.recent_plate_times.get(plate_text)
                now = datetime.now()
                if not last_seen or (now - last_seen).total_seconds() > 60:
                    self.recent_plate_times[plate_text] = now
                    return True
        return False

    def update_log_status(self, plate_text, face_name):
        # Create a unique ID for vehicle-face pair
        vehicle_face_id = f"{plate_text}_{face_name}"

        # First check for vehicle-face pair (vehicle + face)
        if plate_text not in self.vehicle_face_driver:
            # If vehicle is detected for the first time, log it with the associated face
            self.vehicle_face_driver[plate_text] = face_name
            self.vehicle_face_log_status[vehicle_face_id] = 'logged in'  # First time seen, logged in
            print(f"Vehicle {plate_text} with face {face_name} logged in (status: logged in).")
        else:
            # No time limit, just check for any subsequent detections
            stored_face_name = self.vehicle_face_driver[plate_text]
            if stored_face_name != face_name:
                # If face doesn't match the stored face, flag as wrong driver
                print(f"🚫 Wrong Driver! Vehicle {plate_text} is being driven by {face_name}, but the registered driver is {stored_face_name}.")
                self.vehicle_face_log_status[vehicle_face_id] = 'wrong driver'
                return

            self.vehicle_face_log_status[vehicle_face_id] = 'logged out'  # Mark as logged out (car out)
            print(f"Vehicle {plate_text} with face {face_name} logged out (status: logged out).")

    def save_login_logout_data(self, plate_text, face_name, car_color, location, vehicle_type):
        """Saves login/logout and relevant vehicle info to the database."""
        vehicle_face_id = f"{plate_text}_{face_name}"
        vehicle_status = self.vehicle_face_log_status.get(vehicle_face_id, 'Unknown')

        # Check if it's the correct driver before saving
        if vehicle_status == 'wrong driver':
            print(f"🚫 Not saving data. Wrong driver detected for vehicle {plate_text}.")
            return False  # Do not save if the wrong driver is detected

        print(f"Saving log status for {plate_text} with face {face_name} - Status: {vehicle_status}")
        return True

    def save_to_db(self, plate_text, car_color, location, vehicle_type, face_image_path, face_name):
        try:
            if not self.ensure_db_connection():
                print("⚠️ Could not save to database: connection error")
                return False
                
            vehicle_status = self.vehicle_face_log_status.get(f"{plate_text}_{face_name}", "Unknown")
            
            if (plate_text and car_color != "Unknown" and vehicle_type != "Unknown" and face_name != "Unknown"):
                try:
                    self.cursor.execute(""" 
                        INSERT INTO plate_numbers (
                            plate_number, 
                            car_color, 
                            location, 
                            vehicle_type, 
                            face_image_path, 
                            face_name, 
                            date_time_scanned,
                            is_complete_record,
                            login_status
                        ) VALUES (%s, %s, %s, %s, %s, %s, NOW(), TRUE, %s)
                    """, (str(plate_text), str(car_color), str(location), str(vehicle_type), 
                          str(face_image_path), str(face_name), str(vehicle_status)))
                    self.conn.commit()
                    print(f"✅ Complete record saved to DB: {plate_text} | Color: {car_color} | Type: {vehicle_type} | Face: {face_name} | Status: {vehicle_status}")
                    return True
                except mysql.connector.errors.IntegrityError:
                    self.cursor.execute(""" 
                        UPDATE plate_numbers 
                        SET car_color = %s, 
                            location = %s, 
                            vehicle_type = %s, 
                            face_image_path = %s, 
                            face_name = %s, 
                            date_time_scanned = NOW(),
                            is_complete_record = TRUE,
                            login_status = %s
                        WHERE plate_number = %s
                    """, (str(car_color), str(location), str(vehicle_type), 
                        str(face_image_path), str(face_name), str(vehicle_status), str(plate_text)))
                    self.conn.commit()
                    print(f"✅ Updated record in DB: {plate_text} | Color: {car_color} | Type: {vehicle_type} | Face: {face_name} | Status: {vehicle_status}")
                    return True
            else:
                print("⚠️ Incomplete data - not saved to DB")
                return False
        except mysql.connector.Error as e:
            print(f"❌ DB Error: {e}")
            self.ensure_db_connection()
            return False

    def ensure_db_connection(self):
        try:
            if not hasattr(self, 'conn') or self.conn is None or not self.conn.is_connected():
                print("Reconnecting to database...")
                if hasattr(self, 'conn') and self.conn is not None:
                    try:
                        self.conn.close()
                    except:
                        pass

                self.conn = mysql.connector.connect(
                    host="localhost", 
                    user="root", 
                    password="", 
                    database="plate_recognition",
                    autocommit=True
                )
                self.cursor = self.conn.cursor(buffered=True)
                print("Database connection restored")
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False

    def database_worker(self):
        try:
            while not self.stop_event.is_set():
                # Check for new plates to save
                with self.lock:
                    if self.detected_plates:
                        plate_data = self.detected_plates.pop(0)
                        self.save_to_db(
                            plate_data['plate_text'],
                            plate_data['car_color'],
                            plate_data['location'],
                            plate_data['vehicle_type'],
                            plate_data['face_image_path'],
                            plate_data['face_name']
                        )
                time.sleep(1)
        except Exception as e:
            print(f"Error in database worker: {e}")

    def shutdown(self):
        self.stop_event.set()
        if hasattr(self, 'db_thread') and self.db_thread.is_alive():
            self.db_thread.join(timeout=2.0)
        if hasattr(self, 'display_thread') and self.display_thread.is_alive():
            self.display_thread.join(timeout=2.0)
        cv2.destroyAllWindows()
        if hasattr(self, 'conn') and self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
        print("🚦 System shutdown complete")

    def process_camera_face(self, cam_index, location, cam_name):
        cap = cv2.VideoCapture(cam_index)
        cap.set(3, 640)
        cap.set(4, 360)

        # Create faces directory if it doesn't exist
        if not os.path.exists("faces"):
            os.makedirs("faces")

        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Initialize with default values
            face_image_path = ""
            face_name = "Unknown"

            for (fx, fy, fw, fh) in faces:
                face_crop = frame[fy:fy + fh, fx:fx + fw]
                face_image_path = f"faces/{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                cv2.imwrite(face_image_path, face_crop)
                cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)

                face_name = self.recognize_face(gray, face_crop)
                cv2.putText(frame, face_name, (fx, fy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            with self.lock:
                self.current_face_data = {'face_image_path': face_image_path, 'face_name': face_name}
                self.current_face_frame = frame.copy()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_event.set()
                break

        cap.release()

    def process_camera_plate(self, cam_index, location, cam_name):
        cap = cv2.VideoCapture(cam_index)
        cap.set(3, 640)
        cap.set(4, 360)

        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                break

            results = self.plate_model(frame, verbose=False) 
            detected_plate = ""

            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    plate_crop = frame[y1:y2, x1:x2]
                    if plate_crop.size == 0:
                        continue

                    if hasattr(box, 'pts') and len(box.pts) == 4:
                        corners = box.pts
                        plate_crop = correct_perspective(frame, corners)

                    plate_text = self.extract_plate_text(plate_crop)
                    if plate_text:
                        detected_plate = plate_text
                        
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, plate_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.6, (0, 255, 0), 2)
                        break

            with self.lock:
                self.current_plate_data = {
                    'plate_text': detected_plate,
                    'plate_image': frame.copy() if detected_plate else None
                }
                self.current_plate_frame = frame.copy()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_event.set()
                break

        cap.release()

    def process_camera_vehicle(self, cam_index, location, cam_name):
        cap = cv2.VideoCapture(cam_index)
        cap.set(3, 640)
        cap.set(4, 360)

        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                break

            vehicle_type = "Unknown"
            car_color = "Unknown"

            # Get plate position from plate camera
            with self.lock:
                plate_data = self.current_plate_data
                plate_text = plate_data.get('plate_text', "")
                plate_image = plate_data.get('plate_image', None)

            if plate_image is not None:
                # Find vehicle region (assuming plate is at bottom of vehicle)
                height, width = frame.shape[:2]
                vehicle_region = frame[0:int(height*0.8), 0:width]  # Top 80% of frame
                
                # Detect vehicle type
                results = self.plate_model(vehicle_region)
                for r in results:
                    for box in r.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cls_id = int(box.cls[0])
                        vehicle_type = self.plate_model.names[cls_id]
                        
                        # Detect color from vehicle region
                        car_color = self.detect_color(vehicle_region, x1, y1, x2, y2)
                        
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
                        cv2.putText(frame, f"{vehicle_type} ({car_color})", (x1, y1-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
                        break

            with self.lock:
                self.current_vehicle_data = {
                    'vehicle_type': vehicle_type,
                    'car_color': car_color
                }
                self.current_vehicle_frame = frame.copy()

                # Combine all data when we have plate detection
                if plate_text:
                    face_data = self.current_face_data
                    vehicle_data = self.current_vehicle_data
                    
                    plate_data = {
                        'plate_text': plate_text,
                        'car_color': vehicle_data['car_color'],
                        'location': location,
                        'vehicle_type': vehicle_data['vehicle_type'],
                        'face_image_path': face_data['face_image_path'],
                        'face_name': face_data['face_name']
                    }
                    
                    confirmed = self.confirm_plate(plate_text, 
                                                 vehicle_data['car_color'], 
                                                 location, 
                                                 vehicle_data['vehicle_type'],
                                                 face_data['face_image_path'],
                                                 face_data['face_name'])
                    
                    if confirmed:
                        self.detected_plates.append({
                            **plate_data,
                            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_event.set()
                break

        cap.release()
