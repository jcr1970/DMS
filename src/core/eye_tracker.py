import dlib
import os
import cv2
import numpy as np

class EyeTracker:
    def __init__(self):
        predictor_path = os.path.join(os.path.dirname(__file__), '../models/shape_predictor_68_face_landmarks_GTX.dat')
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(predictor_path)

    def track_eyes(self, frame, face):
        x, y, w, h = face
        dlib_rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
        landmarks = self.predictor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), dlib_rect)
        left_eye = self.extract_eye_region(landmarks, range(36, 42))
        right_eye = self.extract_eye_region(landmarks, range(42, 48))
        self.draw_eye_contours(frame, left_eye)
        self.draw_eye_contours(frame, right_eye)
        self.draw_iris_cross(frame, left_eye)
        self.draw_iris_cross(frame, right_eye)
        return left_eye, right_eye

    def extract_eye_region(self, landmarks, points):
        eye_region = [(landmarks.part(n).x, landmarks.part(n).y) for n in points]
        eye_region = np.array(eye_region)
        return eye_region

    def draw_eye_contours(self, frame, eye_region):
        cv2.polylines(frame, [eye_region], True, (0, 255, 0), 2)

    def draw_iris_cross(self, frame, eye_region):
        M = cv2.moments(eye_region)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.drawMarker(frame, (cx, cy), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=1, line_type=cv2.LINE_AA)
        else:
            cx, cy = 0, 0
        return cx, cy

    def validate_eyes(self, left_eye, right_eye, frame):
        valid_left = self.is_eye_detected(left_eye)
        valid_right = self.is_eye_detected(right_eye)
        return valid_left and valid_right

    def is_eye_detected(self, eye_region):
        if eye_region is None or len(eye_region) == 0:
            return False
        for point in eye_region:
            if point[0] <= 0 or point[1] <= 0:
                return False
        return True
