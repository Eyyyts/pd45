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

face_cam_url = "rtsp://admin:team59cpe@192.168.1.10:554/Streaming/Channels/1"
plate_cam_url = "rtsp://admin:team59cpe@192.168.1.11:554/Streaming/Channels/1"

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp|analyzeduration;10000000|buffer_size;5242880"

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
        
        self.plate_model_2 = YOLO('bestyolov8s(4feature).pt')
        self.reader = easyocr.Reader(['en'])
        self.detected_plates = []
        self.plate_queue = queue.Queue()
        self.detected_plate_counts = {}
        self.recent_plate_times = {}
        self.lock = threading.Lock()
        self.stop_event = threading.Event()

        self.pending_faces = {}  # Store face detections temporarily
        self.pending_plates = {}  # Store plate detections temporarily
        self.face_plate_lock = threading.Lock()  # Lock for synchronized access
        self.pending_timeout = 30  # Seconds to keep pending detections
        self.last_cleanup = time.time()

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
            is_complete_record BOOLEAN DEFAULT FALSE,
            security_match BOOLEAN DEFAULT TRUE
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

        # Face recognition setup
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.face_database_path = r"C:\Users\ESTRADA\.spyder-py3\face_database"  # Path to face images
        self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.face_names = []
        self.names = []
        self.load_face_recognizer()

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
                                labels.append(folder)  # Label is the folder name (person name)

            if labels:  # Only train if we have faces
                self.face_names = label_encoder.fit_transform(labels)
                self.names = label_encoder.classes_
                self.face_recognizer.train(face_images, np.array(self.face_names))
                print(f"✅ Trained face recognizer with {len(self.names)} individuals")
            else:
                print("⚠️ No face images found in database directory")
        else:
            print("⚠️ Face database directory not found")

    def recognize_face(self, gray, face_crop):
        try:
            # Convert the face crop to grayscale if it's not already
            face_crop_gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY) if len(face_crop.shape) == 3 else face_crop
        
            # Resize to a consistent size (recommended for LBPH)
            face_crop_gray = cv2.resize(face_crop_gray, (100, 100))
        
            # Recognize the face
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
        # Simple size-based vehicle type detection (can be improved with a dedicated model)
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

    def confirm_plate(self, plate_text, car_color, location, vehicle_type, face_image_path, face_name):
        # Only confirm if we have all required data
        if (plate_text and car_color != "Unknown" and 
            vehicle_type != "Unknown" and 
            face_name != "Unknown"):
            
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

    def save_to_db(self, plate_text, car_color, location, vehicle_type, face_image_path, face_name, security_match=True):
        try:
            # Ensure a valid database connection
            if not self.ensure_db_connection():
                print("⚠️ Could not save to database: connection error")
                return False
                
            # Check if all required fields are present
            if (plate_text and car_color != "Unknown" and 
                vehicle_type != "Unknown" and 
                face_name != "Unknown"):
                
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
                            security_match
                        ) VALUES (%s, %s, %s, %s, %s, %s, NOW(), TRUE, %s)
                    """, (str(plate_text), str(car_color), str(location), 
                        str(vehicle_type), str(face_image_path), str(face_name), security_match))
                    
                    self.conn.commit()
                    print(f"✅ Complete record saved to DB: {plate_text} | Color: {car_color} | Type: {vehicle_type} | Face: {face_name}")
                    return True
                except mysql.connector.errors.IntegrityError:
                    # If insert fails due to duplicate, try update instead
                    self.cursor.execute("""
                        UPDATE plate_numbers 
                        SET car_color = %s, 
                            location = %s, 
                            vehicle_type = %s, 
                            face_image_path = %s, 
                            face_name = %s, 
                            date_time_scanned = NOW(),
                            is_complete_record = TRUE,
                            security_match = %s
                        WHERE plate_number = %s
                    """, (str(car_color), str(location), str(vehicle_type), 
                        str(face_image_path), str(face_name), security_match, str(plate_text)))
                    
                    self.conn.commit()
                    print(f"✅ Updated record in DB: {plate_text} | Color: {car_color} | Type: {vehicle_type} | Face: {face_name}")
                    return True
            else:
                print("⚠️ Incomplete data - not saved to DB")
                return False
        except Exception as e:
            print(f"❌ DB Error: {e}")
            self.ensure_db_connection()
            return False

    def detect_color(self, frame, x1, y1, x2, y2):
        try:
            vehicle_crop = frame[y1:y2, x1:x2]
            if vehicle_crop.size == 0:
                return "Unknown"

            hsv = cv2.cvtColor(vehicle_crop, cv2.COLOR_BGR2HSV)

            color_ranges = {
                'red': ([0, 100, 100], [10, 255, 255]),
                'green': ([40, 100, 100], [80, 255, 255]),
                'blue': ([100, 100, 100], [140, 255, 255]),
                'yellow': ([15, 100, 100], [30, 255, 255]),
                'black': ([0, 0, 0], [180, 255, 30]),
                'white': ([0, 0, 200], [180, 30, 255]),
                'gray': ([0, 0, 50], [180, 30, 200])
            }

            detected_colors = []
            for color, (lower, upper) in color_ranges.items():
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                if cv2.countNonZero(mask) > 0:
                    detected_colors.append(color)

            return detected_colors[0] if detected_colors else "Unknown"
        except Exception as e:
            print(f"Color detection error: {e}")
            return "Unknown"

    def process_camera_face(self, cam_index, location, cam_name):
        retry_count = 0
        max_retries = 5
        
        while not self.stop_event.is_set() and retry_count < max_retries:
            try:
                print(f"Connecting to face camera at {face_cam_url} (attempt {retry_count+1})")
                cap = cv2.VideoCapture(face_cam_url, cv2.CAP_FFMPEG)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)  
                cap.set(cv2.CAP_PROP_FPS, 10)        
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
            
                if not cap.isOpened():
                    print(f"❌ Error: Could not open connection to face camera at {face_cam_url}")
                    retry_count += 1
                    time.sleep(2)  # Wait before retry
                    continue
                
                print("✅ Face camera connected successfully")
                retry_count = 0  # Reset retry count on successful connection
                
                frame_skip = 2  # Process every Nth frame to reduce load
                frame_count = 0
                last_detection_time = time.time()
                consecutive_failures = 0  # Track consecutive frame read failures

                while not self.stop_event.is_set():
                    ret, frame = cap.read()
                    if not ret:
                        consecutive_failures += 1
                        print(f"⚠️ Failed to get frame from face camera ({consecutive_failures}/5)...")
                        if consecutive_failures >= 5:
                            print("❌ Too many consecutive failures, reconnecting...")
                            break
                        time.sleep(0.5)
                        continue
                    
                    consecutive_failures = 0  # Reset on successful frame read
                    
                    frame_count += 1
                    if frame_count % frame_skip != 0:
                        continue  # Skip this frame

                    current_time = time.time()
                    if current_time - last_detection_time < 1.0:
                        # Just show the frame without processing
                        cv2.imshow(cam_name, frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            self.stop_event.set()
                            break
                        continue

                    last_detection_time = current_time

                    try:
                        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
                        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(15, 15))

                        faces = [(int(x*2), int(y*2), int(w*2), int(h*2)) for (x, y, w, h) in faces]
                        
                        current_face_data = {
                            'face_image_path': "",
                            'face_name': "Unknown"
                        }

                        for (fx, fy, fw, fh) in faces:
                            # Make sure the face coordinates are within the frame bounds
                            if fx < 0 or fy < 0 or fx + fw > frame.shape[1] or fy + fh > frame.shape[0]:
                                continue
                                
                            face_crop = frame[fy:fy + fh, fx:fx + fw]
                            if face_crop.size == 0:
                                continue
                                
                            # Ensure directory exists
                            os.makedirs("faces", exist_ok=True)
                            
                            face_image_path = f"faces/{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                            cv2.imwrite(face_image_path, face_crop)
                            cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)

                            face_name = self.recognize_face(gray, face_crop)
                            current_face_data = {
                                'face_image_path': face_image_path,
                                'face_name': face_name
                            }

                            # Display face name on frame
                            cv2.putText(frame, face_name, (fx, fy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)

                            if face_name != "Unknown":
                                with self.face_plate_lock:
                                    self.pending_faces[face_name] = {
                                        'face_image_path': face_image_path,
                                        'face_name': face_name,
                                        'timestamp': time.time(),
                                        'location': location
                                    }
                                    print(f"✅ Stored face detection for: {face_name}")

                        # Store current face data for potential plate detection
                        """ with self.lock:
                            self.current_face_data = current_face_data """

                        cv2.imshow(cam_name, frame)
                    except Exception as e:
                        print(f"Face processing error: {e}")
                        import traceback
                        traceback.print_exc()

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.stop_event.set()
                        break

                cap.release()
                
            except Exception as e:
                print(f"❌ Face camera error: {e}")
                import traceback
                traceback.print_exc()
                retry_count += 1
                time.sleep(2)  # Wait before retry
                
            finally:
                try:
                    if 'cap' in locals() and cap is not None:
                        cap.release()
                    cv2.destroyWindow(cam_name)
                except cv2.error:
                    print(f"Note: Window '{cam_name}' was already closed")
                except Exception as e:
                    print(f"Error cleaning up face camera: {e}")
        
        print("Face camera thread exiting after max retries")

    def process_camera_plate(self, cam_index, location, cam_name):
        cap = cv2.VideoCapture(plate_cam_url, cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 2) 
        cap.set(cv2.CAP_PROP_FPS, 10)    
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
        """ cap.set(3, 640)
        cap.set(4, 360) """

        if not cap.isOpened():
            print(f"❌ Error: Could not open connection to plate camera at {plate_cam_url}")
            return
        
        frame_skip = 2  # Process every Nth frame to reduce load
        frame_count = 0
        last_detection_time = time.time()

        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Failed to get frame from plate camera. Retrying...")
                time.sleep(1)  # Pause before retrying
                continue

            frame_count += 1
            if frame_count % frame_skip != 0:
                continue  # Skip this frame

            current_time = time.time()
            if current_time - last_detection_time < 1.0:
                # Just show the frame without processing
                cv2.imshow(cam_name, frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop_event.set()
                    break
                continue
                
            last_detection_time = current_time

            results_2 = self.plate_model_2(frame, verbose=False) # Rae: Add verbose=False to suppress loop (for debugging)
            detected_plate = ""
            car_color = "Unknown"
            vehicle_type = "Unknown"
            face_image_path = ""
            face_name = "Unknown"

            for r in results_2:
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
                        car_color = self.detect_color(frame, x1, y1, x2, y2)
                        vehicle_type = self.detect_vehicle_type(frame, x1, y1, x2, y2)
                        
                        # Draw bounding box and info
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, plate_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.6, (0, 255, 0), 2)
                        cv2.putText(frame, f"{car_color} {vehicle_type}", (x1, y1 - 40), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                        
                        # Check if we have all required data
                        if (detected_plate and car_color != "Unknown" and 
                            vehicle_type != "Unknown" and face_name != "Unknown"):
                            cv2.putText(frame, "COMPLETE DATA", (x1, y1 - 70), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        break

            if detected_plate:
                # Store plate data with timestamp in pending_plates
                with self.face_plate_lock:
                    self.pending_plates[detected_plate] = {
                        'plate_text': detected_plate,
                        'car_color': car_color,
                        'location': location,
                        'vehicle_type': vehicle_type,
                        'timestamp': time.time()
                    }
                    print(f"✅ Stored plate detection: {detected_plate}")
                    
                    # Try to match with pending faces
                    self.match_face_and_plate()

            cv2.imshow(cam_name, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_event.set()
                break

        cap.release()
        try:
            cv2.destroyWindow(cam_name)
        except cv2.error:
            print(f"Note: Window '{cam_name}' was already closed")

    def display_results(self):
        while not self.stop_event.is_set():
            display_img = np.zeros((800, 600, 3), dtype=np.uint8)  # Larger display area
            cv2.putText(display_img, "COMPLETE DETECTIONS ONLY", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            y_offset = 80
            with self.lock:
                # Only show complete records
                complete_records = [p for p in self.detected_plates 
                                  if (p['plate_text'] and 
                                      p['car_color'] != "Unknown" and 
                                      p['vehicle_type'] != "Unknown" and 
                                      p['face_name'] != "Unknown")]
                
                for plate in reversed(complete_records[-10:]):  # Show last 10 complete records
                    # Plate number
                    cv2.putText(display_img, f"Plate: {plate['plate_text']}", (20, y_offset),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 100), 2)
                    
                    # Vehicle info
                    cv2.putText(display_img, f"Vehicle: {plate['vehicle_type']} ({plate['car_color']})", 
                                (20, y_offset + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 255), 1)
                    
                    # Face info
                    cv2.putText(display_img, f"Driver: {plate['face_name']}", (20, y_offset + 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 255, 200), 1)
                    
                    # Location and time
                    cv2.putText(display_img, f"location: {plate['location']}", (20, y_offset + 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 180), 1)
                    cv2.putText(display_img, plate['time'], (20, y_offset + 120),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 180), 1)
                    
                    # Separator line
                    cv2.line(display_img, (10, y_offset + 140), (590, y_offset + 140), (100, 100, 100), 1)
                    
                    y_offset += 150

            cv2.imshow("Complete Detections", display_img)

            if cv2.waitKey(100) & 0xFF == ord('q'):
                self.stop_event.set()
                break

        cv2.destroyWindow("Complete Detections")

    def match_face_and_plate(self):
        """Match pending face and plate detections and save complete records"""
        current_time = time.time()
        
        # First clean up old pending items
        if current_time - self.last_cleanup > 10:  # Clean up every 10 seconds
            self.cleanup_pending_items()
            self.last_cleanup = current_time
        
        # Find valid matches
        matches_found = 0
        for plate_text, plate_data in list(self.pending_plates.items()):
            plate_time = plate_data['timestamp']
            
            # Look for matching faces (detected within 15 seconds of the plate)
            for face_name, face_data in list(self.pending_faces.items()):
                face_time = face_data['timestamp']
                
                # If face and plate were detected within 15 seconds of each other
                if abs(face_time - plate_time) < 15:
                    # Check security match before proceeding
                    security_match = self.check_security_match(plate_text, face_name)
                    
                    # Create a complete record
                    complete_record = {
                        'plate_text': plate_text,
                        'car_color': plate_data['car_color'],
                        'location': plate_data['location'],
                        'vehicle_type': plate_data['vehicle_type'],
                        'face_image_path': face_data['face_image_path'],
                        'face_name': face_data['face_name'],
                        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'security_match': security_match
                    }
                    
                    # Add to detected plates for display
                    with self.lock:
                        self.detected_plates.append(complete_record)
                    
                    # Queue for database save
                    self.plate_queue.put(complete_record)
                    
                    # Log appropriately based on security match
                    if security_match:
                        print(f"🎯 MATCH FOUND! Plate: {plate_text} with Face: {face_name}")
                    else:
                        print(f"⚠️ SECURITY ALERT! Plate: {plate_text} with unexpected driver: {face_name}")
                    
                    matches_found += 1
                    
                    # Remove matched items to prevent duplicate processing
                    self.pending_plates.pop(plate_text, None)
                    self.pending_faces.pop(face_name, None)
        
        return matches_found > 0

    def cleanup_pending_items(self):
        """Remove old pending face and plate detections"""
        current_time = time.time()
        
        # Remove faces older than timeout period
        for face_name in list(self.pending_faces.keys()):
            if current_time - self.pending_faces[face_name]['timestamp'] > self.pending_timeout:
                self.pending_faces.pop(face_name)
                print(f"⏲️ Removed stale face detection: {face_name}")
        
        # Remove plates older than timeout period
        for plate_text in list(self.pending_plates.keys()):
            if current_time - self.pending_plates[plate_text]['timestamp'] > self.pending_timeout:
                self.pending_plates.pop(plate_text)
                print(f"⏲️ Removed stale plate detection: {plate_text}")

    def database_worker(self):
        while not self.stop_event.is_set():
            try:
                plate_data = self.plate_queue.get(timeout=1)
                
                for key in plate_data:
                    if isinstance(plate_data[key], (np.str_, np.ndarray)):
                        plate_data[key] = str(plate_data[key])
                
                has_plate = bool(plate_data['plate_text'])
                has_color = plate_data['car_color'] != "Unknown"
                has_vehicle = plate_data['vehicle_type'] != "Unknown"
                has_face = plate_data['face_name'] != "Unknown"
                
                print(f"[DEBUG] Condition checks: plate={has_plate}, color={has_color}, vehicle={has_vehicle}, face={has_face}")
                
                if has_plate and has_color and has_vehicle and has_face:
                    print(f"[DB Queue] Complete record: {plate_data}")
                    self.save_to_db(
                        plate_data['plate_text'],
                        plate_data['car_color'],
                        plate_data['location'],
                        plate_data['vehicle_type'],
                        plate_data['face_image_path'],
                        plate_data['face_name'],
                        plate_data.get('security_match', True)  # allow access by default
                    )
                else:
                    print(f"[DB Queue] Incomplete record - not saved: {plate_data}")
                    
            except queue.Empty:
                pass
            except Exception as e:
                print(f"Database worker error: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(1)
                
    def ensure_db_connection(self):
        """Ensure database connection is active, reconnect if needed."""
        try:
            # Check if connection is still alive
            if not hasattr(self, 'conn') or self.conn is None or not self.conn.is_connected():
                print("Reconnecting to database...")
                # Close existing connection if it exists
                if hasattr(self, 'conn') and self.conn is not None:
                    try:
                        self.conn.close()
                    except:
                        pass
                
                # Create a new connection
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
    
    def shutdown(self):
        self.stop_event.set()
        cv2.destroyAllWindows()
        if self.conn and self.conn.is_connected():
            self.conn.close()
        print("🚦 System shutdown complete")

    def camera_health_check(self):
        """Periodically check camera connections and restart if needed"""
        face_camera_working = True
        plate_camera_working = True
        
        while not self.stop_event.is_set():
            time.sleep(10)  # Check every 10 seconds
            
            # Check if threads are still alive
            face_cam_thread_alive = any(t.name == "FaceCameraThread" and t.is_alive() 
                                        for t in threading.enumerate())
            plate_cam_thread_alive = any(t.name == "PlateCameraThread" and t.is_alive() 
                                        for t in threading.enumerate())
            
            if not face_cam_thread_alive and face_camera_working:
                print("Face camera thread died, restarting...")
                face_camera_working = False
                threading.Thread(target=self.process_camera_face, 
                                args=(None, "Gate 1", "Face Recog Camera"),
                                name="FaceCameraThread").start()
                
            if not plate_cam_thread_alive and plate_camera_working:
                print("Plate camera thread died, restarting...")
                plate_camera_working = False
                threading.Thread(target=self.process_camera_plate, 
                                args=(None, "Gate 1", "Plate/Color Camera"),
                                name="PlateCameraThread").start()
                
    def check_security_match(self, plate_text, face_name):
        """
        verify kung match ang face and plate using security api
        """
        import requests
        
        try:
            response = requests.post(
                'http://localhost:5000/check_plate',
                json={'plate_number': plate_text, 'face_name': face_name},
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('match', True)  # if walang 'match' sa response, allow access by default
            else:
                print(f"Security API error: {response.status_code} - {response.text}")
                return True  # allow access if ever mag fail api
        except Exception as e:
            print(f"Error checking security match: {e}")
            return True  # allow access if ever mag fail api


if __name__ == "__main__":
    recognizer = PlateRecognizer()

    db_thread = threading.Thread(target=recognizer.database_worker, daemon=True, name="DBWorkerThread")
    display_thread = threading.Thread(target=recognizer.display_results, daemon=True, name="DisplayThread")
    health_check_thread = threading.Thread(target=recognizer.camera_health_check, daemon=True, name="HealthCheckThread")

    db_thread.start()
    display_thread.start()
    health_check_thread.start()

    cam1 = threading.Thread(target=recognizer.process_camera_face, args=(None, "Gate 1", "Face Recog Camera"), name="FaceCameraThread")
    cam2 = threading.Thread(target=recognizer.process_camera_plate, args=(None, "Gate 1", "Plate/Color Camera"), name="PlateCameraThread")

    cam1.start()
    cam2.start()

    try:
        cam1.join()
        cam2.join()
        display_thread.join()
    except KeyboardInterrupt:
        recognizer.shutdown()
    finally:
        recognizer.shutdown()