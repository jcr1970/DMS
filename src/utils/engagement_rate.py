import numpy as np

def calculate_engagement_rate(eye_positions, calibration_points):
    if eye_positions is None or calibration_points is None:
        return None

    left_eye, right_eye = eye_positions
    gaze_center = (np.mean(left_eye, axis=0) + np.mean(right_eye, axis=0)) / 2

    min_distance = float('inf')
    closest_point = None
    for point, positions in calibration_points.items():
        if point == 'road':
            for road_point in positions:
                road_center = (np.mean(road_point[0], axis=0) + np.mean(road_point[1], axis=0)) / 2
                distance = np.linalg.norm(gaze_center - road_center)
                if distance < min_distance:
                    min_distance = distance
                    closest_point = point
        else:
            if positions is not None:
                point_center = (np.mean(positions[0], axis=0) + np.mean(positions[1], axis=0)) / 2
                distance = np.linalg.norm(gaze_center - point_center)
                if distance < min_distance:
                    min_distance = distance
                    closest_point = point

    return closest_point
