# src/ui/report_panel.py

import wx
import os
import subprocess
from core.main_core import DriverMonitoringSystem

class ReportPanel(wx.Panel):
    def __init__(self, parent):
        super(ReportPanel, self).__init__(parent, style=wx.TRANSPARENT_WINDOW)
        self.init_ui()
        self.driver_monitoring_system = DriverMonitoringSystem()

    def init_ui(self):
        self.SetBackgroundColour(wx.Colour(255, 255, 255, 0))  # Transparent background

        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.generate_report_button = wx.Button(self, label="Generate Report")
        self.generate_report_button.SetFont(font)
        self.generate_report_button.SetBackgroundColour("#2196F3")  # Blue
        self.generate_report_button.SetForegroundColour(wx.WHITE)
        self.generate_report_button.Bind(wx.EVT_BUTTON, self.generate_report)
        vbox.Add(self.generate_report_button, flag=wx.LEFT | wx.TOP, border=10)

        self.SetSizerAndFit(vbox)

    def generate_report(self, event):
        # Generate the report using real data

        # Get the absolute path of the Streamlit app
        current_dir = os.path.dirname(os.path.abspath(__file__))
        streamlit_app_path = os.path.join(current_dir, 'streamlit_app.py')

        if os.path.exists(streamlit_app_path):
            subprocess.Popen(['streamlit', 'run', streamlit_app_path])
        else:
            wx.MessageBox(f"Error: File does not exist: {streamlit_app_path}", 'Error', wx.OK | wx.ICON_ERROR)
