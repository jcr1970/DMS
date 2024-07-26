import cv2
import os
import dlib
import numpy as np

class FaceDetector:
    def __init__(self):
        haarcascade_path = os.path.join(os.path.dirname(__file__), '../data/haarcascade_frontalface_default.xml')
        self.face_cascade = cv2.CascadeClassifier(haarcascade_path)
        self.face_recognition_model = dlib.face_recognition_model_v1('src/models/dlib_face_recognition_resnet_model_v1.dat')
        self.shape_predictor = dlib.shape_predictor('src/models/shape_predictor_68_face_landmarks_GTX.dat')
        self.known_face_descriptor = None

    def detect_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50), flags=cv2.CASCADE_SCALE_IMAGE)
        
        if len(faces) == 0:
            return None
        
        # Select the largest face detected
        face = max(faces, key=lambda rect: rect[2] * rect[3])
        return face  # Return the largest detected face

    def draw_detected_face(self, frame, face):
        if face is not None:
            x, y, w, h = face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    def get_face_descriptor(self, frame, face):
        x, y, w, h = face
        rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))
        shape = self.shape_predictor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), rect)
        return np.array(self.face_recognition_model.compute_face_descriptor(frame, shape))

    def save_user_face(self, frame, face):
        self.known_face_descriptor = self.get_face_descriptor(frame, face)
        save_path = 'src/data/user_calibration.npz'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        np.savez(save_path, face_descriptor=self.known_face_descriptor)

    def recognize_user_face(self, frame, face, user_face_descriptor):
        if user_face_descriptor is None:
            return False
        
        face_descriptor = self.get_face_descriptor(frame, face)
        distance = np.linalg.norm(face_descriptor - user_face_descriptor)
        return distance < 0.6  # Adjust the threshold as necessary
