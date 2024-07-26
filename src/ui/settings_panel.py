# src/ui/settings_panel.py

import wx

class SettingsPanel(wx.Panel):
    def __init__(self, parent):
        super(SettingsPanel, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.SetBackgroundColour(wx.Colour(255, 255, 255))  # Solid white background

        notebook = wx.Notebook(self)

        calibrate_panel = wx.Panel(notebook)
        help_panel = wx.Panel(notebook)
        about_us_panel = wx.Panel(notebook)
        privacy_panel = wx.Panel(notebook)

        notebook.AddPage(calibrate_panel, "Calibrate")
        notebook.AddPage(help_panel, "Help")
        notebook.AddPage(about_us_panel, "About Us")
        notebook.AddPage(privacy_panel, "Privacy")

        # Calibrate panel
        calibrate_sizer = wx.BoxSizer(wx.VERTICAL)
        calibrate_text = wx.StaticText(calibrate_panel, label="Calibration settings go here.")
        calibrate_sizer.Add(calibrate_text, 0, wx.ALL, 10)
        calibrate_panel.SetSizer(calibrate_sizer)

        # Help panel
        help_sizer = wx.BoxSizer(wx.VERTICAL)
        help_text = wx.StaticText(help_panel, label="Help information goes here.")
        help_sizer.Add(help_text, 0, wx.ALL, 10)
        help_panel.SetSizer(help_sizer)

        # About Us panel
        about_us_sizer = wx.BoxSizer(wx.VERTICAL)
        mission_text = wx.StaticText(about_us_panel, label="We are a team of 4 from FIU who aim to use this app to help combat driver drowsiness.")
        about_us_sizer.Add(mission_text, 0, wx.ALL, 10)
        contact_text = wx.StaticText(about_us_panel, label=
            "Santiago Cuartas\nPhone: 555-1234\nEmail: santiago@example.com\n\n"
            "Johann Cardentey\nPhone: 555-5678\nEmail: johann@example.com\n\n"
            "Carlos Quintanilla\nPhone: 555-8765\nEmail: carlos@example.com\n\n"
            "Flavio Leguen\nPhone: 555-4321\nEmail: flavio@example.com")
        about_us_sizer.Add(contact_text, 0, wx.ALL, 10)
        about_us_panel.SetSizer(about_us_sizer)

        # Privacy panel
        privacy_sizer = wx.BoxSizer(wx.VERTICAL)
        privacy_text = wx.StaticText(privacy_panel, label="Privacy policy information goes here.")
        privacy_sizer.Add(privacy_text, 0, wx.ALL, 10)
        privacy_panel.SetSizer(privacy_sizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)
