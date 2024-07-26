# src/ui/home_panel.py

import wx
import datetime
import cv2
import logging
from core.car_calibration import calibrate
from core.camera import Camera
from core.face_detector import FaceDetector
from core.eye_tracker import EyeTracker
from core.main_core import DriverMonitoringSystem

class HomePanel(wx.Panel):
    def __init__(self, parent, username, gaze_detection, db):
        super(HomePanel, self).__init__(parent, style=wx.TRANSPARENT_WINDOW)
        self.username = username
        self.gaze_detection = gaze_detection
        self.db = db
        self.video_writer = None
        self.timer = wx.Timer(self)
        self.driver_monitoring_system = DriverMonitoringSystem()
        self.Bind(wx.EVT_TIMER, self.update_frame, self.timer)
        self.init_ui()

    def init_ui(self):
        self.SetBackgroundColour(wx.Colour(255, 255, 255, 0))  # Transparent background

        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        hbox_camera = wx.BoxSizer(wx.HORIZONTAL)
        self.camera_label = wx.StaticText(self, label="Select Camera:")
        self.camera_label.SetFont(font)
        self.camera_label.SetForegroundColour(wx.BLACK)
        self.camera_choice = wx.Choice(self, choices=["Camera 1", "Camera 2"])  # Add more camera options as needed
        self.camera_choice.SetBackgroundColour("#FFD700")  # Gold
        self.camera_choice.SetForegroundColour(wx.BLACK)
        hbox_camera.Add(self.camera_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        hbox_camera.Add(self.camera_choice, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.live_feed_button = wx.Button(self, label="Start Eye-Tracking")
        self.live_feed_button.SetFont(font)
        self.live_feed_button.SetBackgroundColour("#4CAF50")  # Green
        self.live_feed_button.SetForegroundColour(wx.WHITE)
        self.live_feed_button.Bind(wx.EVT_BUTTON, self.start_live_feed)

        self.stop_feed_button = wx.Button(self, label="Stop Eye-Tracking")
        self.stop_feed_button.SetFont(font)
        self.stop_feed_button.SetBackgroundColour("#F44336")  # Red
        self.stop_feed_button.SetForegroundColour(wx.WHITE)
        self.stop_feed_button.Bind(wx.EVT_BUTTON, self.stop_live_feed)
        self.stop_feed_button.Disable()  # Initially disabled until live feed is started
        hbox_buttons.Add(self.live_feed_button, 1, wx.ALL | wx.EXPAND, 5)
        hbox_buttons.Add(self.stop_feed_button, 1, wx.ALL | wx.EXPAND, 5)

        # Car Calibration button
        self.car_clibrate_button = wx.Button(self, label="Calibration")
        self.car_clibrate_button.SetFont(font)
        self.car_clibrate_button.SetBackgroundColour("#E69138") #orange
        self.car_clibrate_button.SetForegroundColour(wx.WHITE)
        self.car_clibrate_button.Bind(wx.EVT_BUTTON, self.start_car_calibration)
        hbox_buttons.Add(self.car_clibrate_button, 0, wx.ALL | wx.EXPAND, 5)

        hbox_main = wx.BoxSizer(wx.HORIZONTAL)
        hbox_main.Add(hbox_camera, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        hbox_main.Add(hbox_buttons, 1, wx.ALL | wx.EXPAND, 5)

        self.username_label = wx.StaticText(self, label=f"Logged in as: {self.username}")
        self.username_label.SetFont(font)
        self.username_label.SetForegroundColour(wx.BLACK)

        self.logout_button = wx.Button(self, label="↪️ Logout")
        self.logout_button.SetFont(font)
        self.logout_button.SetBackgroundColour("#FFD700")  # Gold
        self.logout_button.Bind(wx.EVT_BUTTON, self.logout)

        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(hbox_main, 0, wx.ALL | wx.EXPAND, 5)
        layout.AddStretchSpacer()
        layout.Add(self.username_label, 0, wx.ALL | wx.ALIGN_LEFT, 5)  # Align to the left
        layout.Add(self.logout_button, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizerAndFit(layout)

    def start_live_feed(self, event):
        self.live_feed_button.Disable()
        self.stop_feed_button.Enable()
        self.driver_monitoring_system.start_tracking()

        self.timer.Start(1000 // 30)  # Update frame 30 times per second

    def stop_live_feed(self, event):
        self.timer.Stop()
        self.driver_monitoring_system.stop_tracking()
        self.live_feed_button.Enable()
        self.stop_feed_button.Disable()

    def start_car_calibration(self, event):
        camera = Camera()  # Replace with actual camera object
        face_detector = FaceDetector()  # Replace with actual face detector object
        eye_tracker =  EyeTracker() # Use existing eye tracker
        calibrate(camera, face_detector, eye_tracker)
        camera.release()

    def update_frame(self, event):
        self.driver_monitoring_system.update_tracking()

    def flatten_gaze_data(self, data):
        flat_data = []
        if isinstance(data, list):
            return data
        try:
            for key in data:
                if isinstance(data[key], list):
                    flat_data.extend([float(x) for x in data[key]])
                else:
                    flat_data.append(float(data[key]))
        except TypeError as e:
            logging.error(f"Error flattening data: {e}")
        return flat_data

    def logout(self, event):
        parent = self.GetParent()
        parent.Hide()
        from ui.login_frame import LoginFrame  # Lazy import to avoid circular dependency
        login_frame = LoginFrame(None, "Login")
        login_frame.Show()
