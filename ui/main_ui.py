# src/ui/main_ui.py
import wx
import cv2
from core.eye_tracking import EyeTracking
from core.engagement_score import calculate_engagement_score, calculate_engagement_percentage
from utils.database import Database

class LoginScreen(wx.Frame):
    def __init__(self, parent, on_login):
        super().__init__(parent, title="Login", size=(400, 300))
        
        self.panel = wx.Panel(self)
        self.on_login = on_login
        
        self.username_label = wx.StaticText(self.panel, label="Username:")
        self.username_input = wx.TextCtrl(self.panel)
        
        self.password_label = wx.StaticText(self.panel, label="Password:")
        self.password_input = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD)
        
        self.login_button = wx.Button(self.panel, label="Login")
        self.login_button.Bind(wx.EVT_BUTTON, self.login)
        
        self.create_profile_button = wx.Button(self.panel, label="Create Profile")
        self.create_profile_button.Bind(wx.EVT_BUTTON, self.create_profile)
        
        self.layout = wx.BoxSizer(wx.VERTICAL)
        self.layout.Add(self.username_label, 0, wx.ALL, 5)
        self.layout.Add(self.username_input, 0, wx.ALL | wx.EXPAND, 5)
        self.layout.Add(self.password_label, 0, wx.ALL, 5)
        self.layout.Add(self.password_input, 0, wx.ALL | wx.EXPAND, 5)
        self.layout.Add(self.login_button, 0, wx.ALL | wx.CENTER, 5)
        self.layout.Add(self.create_profile_button, 0, wx.ALL | wx.CENTER, 5)
        
        self.panel.SetSizerAndFit(self.layout)
        
        self.db = Database()
    
    def login(self, event):
        username = self.username_input.GetValue()
        password = self.password_input.GetValue()
        if self.db.validate_user(username, password):
            self.on_login(username)
            self.Close()
        else:
            wx.MessageBox("Invalid username or password", "Error", wx.OK | wx.ICON_ERROR)
    
    def create_profile(self, event):
        username = self.username_input.GetValue()
        password = self.password_input.GetValue()
        if self.db.create_user(username, password):
            wx.MessageBox("Profile created successfully", "Success", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Profile creation failed. Username may already exist.", "Error", wx.OK | wx.ICON_ERROR)

class CameraApp(wx.Frame):
    def __init__(self, parent, username):
        super().__init__(parent, title=f"Camera App - Logged in as {username}", size=(800, 600))
        
        self.username = username
        self.panel = wx.Panel(self)
        
        self.camera_label = wx.StaticText(self.panel, label="Select Camera:")
        self.camera_choice = wx.Choice(self.panel, choices=["Camera 1", "Camera 2"]) 
        
        self.live_feed_button = wx.Button(self.panel, label="Start Eye-Tracking")
        self.live_feed_button.Bind(wx.EVT_BUTTON, self.start_live_feed)
        
        self.stop_feed_button = wx.Button(self.panel, label="Stop Eye-Tracking")
        self.stop_feed_button.Bind(wx.EVT_BUTTON, self.stop_live_feed)
        self.stop_feed_button.Disable()
        
        self.logout_button = wx.Button(self.panel, label="Logout")
        self.logout_button.Bind(wx.EVT_BUTTON, self.logout)
        
        self.video_display = wx.StaticBitmap(self.panel)
        
        self.layout = wx.BoxSizer(wx.VERTICAL)
        self.layout.Add(self.camera_label, 0, wx.ALL, 5)
        self.layout.Add(self.camera_choice, 0, wx.ALL | wx.EXPAND, 5)
        self.layout.Add(self.live_feed_button, 0, wx.ALL | wx.EXPAND, 5)
        self.layout.Add(self.stop_feed_button, 0, wx.ALL | wx.EXPAND, 5)
        self.layout.Add(self.video_display, 1, wx.ALL | wx.EXPAND, 5)
        self.layout.Add(self.logout_button, 0, wx.ALL | wx.EXPAND, 5)
        
        self.panel.SetSizerAndFit(self.layout)
        
        self.eye_tracking = EyeTracking()
        self.db = Database()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_frame, self.timer)
    
    def start_live_feed(self, event):
        selected_camera_index = self.camera_choice.GetSelection()
        self.eye_tracking.start(selected_camera_index)
        self.live_feed_button.Disable()
        self.stop_feed_button.Enable()
        self.timer.Start(1000 // 30)
    
    def stop_live_feed(self, event):
        self.timer.Stop()
        self.eye_tracking.stop()
        self.live_feed_button.Enable()
        self.stop_feed_button.Disable()
    
    def update_frame(self, event):
        ret, frame = self.eye_tracking.get_frame()
        if ret:
            height, width = frame.shape[:2]
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            bitmap = wx.Bitmap.FromBuffer(width, height, frame_rgb)
            self.video_display.SetBitmap(bitmap)
            
            gaze_data = self.eye_tracking.get_gaze_data(frame)
            self.db.log_gaze_data(self.username, gaze_data)
            engagement_score = calculate_engagement_score(gaze_data)
            engagement_percentage = calculate_engagement_percentage(engagement_score, self.eye_tracking.max_score)
            print(f"Engagement Percentage: {engagement_percentage:.2f}%")
    
    def logout(self, event):
        self.Close()
        self.Parent.Show()
