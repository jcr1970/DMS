import os
import numpy as np
import cv2

calibration_file = 'src/data/calibration_data.npz'

def calibrate(camera, face_detector, eye_tracker):
    calibration_points = {
        'rearview_mirror': None,
        'left_side_mirror': None,
        'right_side_mirror': None,
        'dashboard': None,
        'road': []
    }

    instructions = {
        'rearview_mirror': "Please look at the rearview mirror and press 'C'.",
        'left_side_mirror': "Please look at the left side mirror and press 'C'.",
        'right_side_mirror': "Please look at the right side mirror and press 'C'.",
        'dashboard': "Please look at the dashboard and press 'C'.",
        'road': ["Please look at the top-left corner of the road and press 'C'.",
                 "Please look at the top-right corner of the road and press 'C'.",
                 "Please look at the bottom-left corner of the road and press 'C'.",
                 "Please look at the bottom-right corner of the road and press 'C'."]
    }

    def display_instruction(frame, text):
        font = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10, 30)
        fontScale = 1
        fontColor = (255, 0, 0)
        lineType = 2

        cv2.putText(frame, text,
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)
        camera.display_frame(frame)

    for point, instruction in instructions.items():
        if point == 'road':
            for sub_instruction in instruction:
                print(sub_instruction)

                while True:
                    frame = camera.get_frame()
                    if frame is None:
                        continue

                    face = face_detector.detect_face(frame)
                    if face is not None:
                        eye_positions = eye_tracker.track_eyes(frame, face)
                        display_instruction(frame, sub_instruction)

                        if cv2.waitKey(1) & 0xFF == ord('c'):
                            calibration_points[point].append(eye_positions)
                            print(f"{sub_instruction.split()[2]} calibrated")
                            break
        else:
            print(instruction)

            while True:
                frame = camera.get_frame()
                if frame is None:
                    continue

                face = face_detector.detect_face(frame)
                if face is not None:
                    eye_positions = eye_tracker.track_eyes(frame, face)
                    display_instruction(frame, instruction)

                    if cv2.waitKey(1) & 0xFF == ord('c'):
                        calibration_points[point] = eye_positions
                        print(f"{instruction.split()[2]} calibrated")
                        break

    # Ensure calibration points are correctly populated before saving
    valid = all(value is not None for key, value in calibration_points.items() if key != 'road')
    valid = valid and all(calibration_points['road'])

    if valid:
        try:
            # Save calibration data as .npz file
            np.savez(calibration_file, **calibration_points)
            print("Calibration data saved successfully.")
        except Exception as e:
            print(f"Error saving calibration data: {e}")
    else:
        print("Calibration data is incomplete and will not be saved.")

    return calibration_points

def load_calibration_data():
    try:
        # Load calibration data from .npz file
        with np.load(calibration_file, allow_pickle=True) as data:
            calibration_data = {key: data[key] for key in data}
        if calibration_data:
            print("Calibration data loaded successfully.")
        else:
            raise ValueError("Calibration data is empty.")
    except Exception as e:
        print(f"Error loading calibration data: {e}")
        return None
    return calibration_data

def get_calibration_data(camera, face_detector, eye_tracker):

    if os.path.exists(calibration_file):
        print("Loading existing calibration data.")
        calibration_data = load_calibration_data()
        if calibration_data is not None:
            return calibration_data
        else:
            print("Calibration data is invalid. Performing calibration again.")
            return calibrate(camera, face_detector, eye_tracker)
    else:
        print("Performing calibration.")
        return calibrate(camera, face_detector, eye_tracker)
