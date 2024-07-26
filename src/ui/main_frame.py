# src/ui/main_frame.py

import wx
import logging
from ui.home_panel import HomePanel
from ui.profile_panel import ProfilePanel
from ui.report_panel import ReportPanel
from ui.settings_panel import SettingsPanel
from ui.background_panel import BackgroundPanel
from core.main_core import DriverMonitoringSystem
from utils.database import Database
from utils.user_database import UserDatabase

logging.basicConfig(level=logging.DEBUG)

class MainFrame(wx.Frame):
    def __init__(self, parent, title, username):
        super(MainFrame, self).__init__(parent, title=f"{title} - Logged in as {username}", size=(800, 600))

        self.username = username
        self.user_db = UserDatabase()
        self.panel = BackgroundPanel(self, "src/utils/fiulogo.png")

        # Create top button panel
        top_button_panel = wx.Panel(self.panel, style=wx.TRANSPARENT_WINDOW)
        top_button_panel.SetBackgroundColour("#333333")  # Dark background for the top panel
        top_button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        self.home_button = wx.Button(top_button_panel, label="🏠 Home ")
        self.home_button.SetFont(font)
        self.home_button.SetBackgroundColour("#FFD700")  # Gold

        self.profile_button = wx.Button(top_button_panel, label="👤 Profile ")
        self.profile_button.SetFont(font)
        self.profile_button.SetBackgroundColour("#FFD700")  # Gold

        self.dashboard_button = wx.Button(top_button_panel, label="📊 Report ")
        self.dashboard_button.SetFont(font)
        self.dashboard_button.SetBackgroundColour("#FFD700")  # Gold

        self.settings_button = wx.Button(top_button_panel, label="⚙️ Settings")
        self.settings_button.SetFont(font)
        self.settings_button.SetBackgroundColour("#FFD700")  # Gold

        top_button_sizer.Add(self.home_button, 1, wx.EXPAND | wx.ALL, 5)
        top_button_sizer.Add(self.profile_button, 1, wx.EXPAND | wx.ALL, 5)
        top_button_sizer.Add(self.dashboard_button, 1, wx.EXPAND | wx.ALL, 5)
        top_button_sizer.Add(self.settings_button, 1, wx.EXPAND | wx.ALL, 5)

        top_button_panel.SetSizer(top_button_sizer)

        # Bind button events
        self.home_button.Bind(wx.EVT_BUTTON, self.show_home)
        self.profile_button.Bind(wx.EVT_BUTTON, self.show_profile)
        self.dashboard_button.Bind(wx.EVT_BUTTON, self.show_dashboard)
        self.settings_button.Bind(wx.EVT_BUTTON, self.show_settings)

        self.eye_tracking = DriverMonitoringSystem()
        self.db = Database()

        self.home_panel = HomePanel(self.panel, self.username, self.eye_tracking, self.db)
        self.profile_panel = ProfilePanel(self.panel, self.username)
        self.report_panel = ReportPanel(self.panel)
        self.settings_panel = SettingsPanel(self.panel)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(top_button_panel, 0, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.home_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.profile_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.report_panel, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Add(self.settings_panel, 1, wx.EXPAND | wx.ALL, 5)

        self.profile_panel.Hide()
        self.report_panel.Hide()
        self.settings_panel.Hide()

        self.panel.SetSizerAndFit(self.sizer)
        self.Bind(wx.EVT_CLOSE, self.on_close)  # Bind the close event

    def show_home(self, event):
        self.profile_panel.Hide()
        self.report_panel.Hide()
        self.settings_panel.Hide()
        self.home_panel.Show()
        self.panel.Layout()

    def show_profile(self, event):
        self.home_panel.Hide()
        self.report_panel.Hide()
        self.settings_panel.Hide()
        self.profile_panel.Show()
        self.panel.Layout()

    def show_dashboard(self, event):
        self.home_panel.Hide()
        self.profile_panel.Hide()
        self.settings_panel.Hide()
        self.report_panel.Show()
        self.panel.Layout()

    def show_settings(self, event):
        self.home_panel.Hide()
        self.profile_panel.Hide()
        self.report_panel.Hide()
        self.settings_panel.Show()
        self.panel.Layout()

    def on_close(self, event):
        # Stop video recording if active
        if self.home_panel.video_writer:
            self.home_panel.video_writer.release()
            self.home_panel.video_writer = None

        # Close the database connection
        self.db.close()

        self.Destroy()
