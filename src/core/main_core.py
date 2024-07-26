# src/core/main_core.py

from core.camera import Camera
from core.face_detector import FaceDetector
from core.eye_tracker import EyeTracker
from utils.engagement_rate import calculate_engagement_rate
from core.car_calibration import get_calibration_data
from utils.metrics_report import generate_metrics_report
import time
import os
import cv2
from playsound import playsound
import numpy as np

class DriverMonitoringSystem:
    def __init__(self):
        self.camera = Camera()
        self.face_detector = FaceDetector()
        self.eye_tracker = EyeTracker()
        self.calibration_points = None
        self.alert_sound_path = os.path.join(os.path.dirname(__file__), '..', 'utils', 'alert_sound.wav')
        self.engagement_data = {
            'rearview_mirror': 0,
            'left_side_mirror': 0,
            'right_side_mirror': 0,
            'dashboard': 0,
            'road': 0,
            'other': 0
        }
        self.start_time = None
        self.frame_count = 0
        self.missing_eye_start_time = None
        self.total_time = 0
        self.is_tracking = False

        # Load user face descriptor
        user_calibration_path = 'src/data/user_calibration.npz'
        if os.path.exists(user_calibration_path):
            self.user_face_descriptor = np.load(user_calibration_path)['face_descriptor']
        else:
            self.user_face_descriptor = None
            print("User calibration data not found. Please perform calibration first.")

    def play_alert_sound(self):
        playsound(self.alert_sound_path)

    def start_tracking(self):
        if self.user_face_descriptor is None:
            print("User face descriptor not loaded. Exiting.")
            return

        self.is_tracking = True
        self.start_time = time.time()
        self.frame_count = 0
        self.engagement_data = {
            'rearview_mirror': 0,
            'left_side_mirror': 0,
            'right_side_mirror': 0,
            'dashboard': 0,
            'road': 0,
            'other': 0
        }

        print("Starting calibration...")
        self.calibration_points = get_calibration_data(self.camera, self.face_detector, self.eye_tracker)
        print("Calibration completed. Starting monitoring...")

    def update_tracking(self):
        if not self.is_tracking:
            return

        frame = self.camera.get_frame()
        if frame is None:
            return

        face = self.face_detector.detect_face(frame)
        self.face_detector.draw_detected_face(frame, face)
        eye_positions = None
        if face is not None and self.face_detector.recognize_user_face(frame, face, self.user_face_descriptor):
            left_eye, right_eye = self.eye_tracker.track_eyes(frame, face)
            if self.eye_tracker.validate_eyes(left_eye, right_eye, frame):
                eye_positions = [left_eye, right_eye]
                engagement_point = calculate_engagement_rate(eye_positions, self.calibration_points)
                if engagement_point:
                    self.engagement_data[engagement_point] += 1
                else:
                    self.engagement_data['other'] += 1

                # Display engagement point on the frame
                self.camera.display_engagement(frame, engagement_point)
            else:
                eye_positions = None

        if eye_positions is None:
            if self.missing_eye_start_time is None:
                self.missing_eye_start_time = time.time()
            elif time.time() - self.missing_eye_start_time >= 3:
                cv2.putText(frame, "LOOK AT THE ROAD", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                if time.time() - self.missing_eye_start_time >= 5:
                    self.play_alert_sound()
        else:
            self.missing_eye_start_time = None

        self.frame_count += 1
        cv2.imshow("Driver Monitoring System", frame)
        cv2.waitKey(1)

    def stop_tracking(self):
        if not self.is_tracking:
            return

        self.is_tracking = False
        self.total_time = time.time() - self.start_time
        generate_metrics_report(self.engagement_data, self.total_time, self.frame_count)
        self.camera.release()
        cv2.destroyAllWindows()

    
