import cv2

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cv2.namedWindow("Driver Monitoring System")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def display_frame(self, frame):
        cv2.imshow("Driver Monitoring System", frame)

    def display_engagement(self, frame, engagement_point):
        if engagement_point:
            cv2.putText(frame, f"Engagement: {engagement_point}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow("Driver Monitoring System", frame)

    def quit_requested(self):
        return cv2.waitKey(1) & 0xFF == ord('q')

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
