# src/ui/login_frame.py

import wx
from ui.registration_dialog import RegistrationDialog
from ui.background_panel import BackgroundPanel  # Correct import path
from core.cam_calibration import perform_calibration  # Ensure these are correctly imported
from utils.user_database import UserDatabase  # Ensure these are correctly imported


class LoginFrame(wx.Frame):
    def __init__(self, parent, title):
        super(LoginFrame, self).__init__(parent, title=title, size=(600, 600))
        self.user_db = UserDatabase()
        self.init_ui()

    def init_ui(self):
        panel = BackgroundPanel(self, "src/utils/fiulogo.png")
        vbox = wx.BoxSizer(wx.VERTICAL)

        inner_panel = wx.Panel(panel, style=wx.TRANSPARENT_WINDOW)
        inner_panel.SetBackgroundColour(wx.Colour(255, 255, 255, 150))  # semi-transparent white background

        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        label_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        inner_vbox = wx.BoxSizer(wx.VERTICAL)
        self.username_label = wx.StaticText(inner_panel, label="Username:")
        self.username_label.SetFont(label_font)
        inner_vbox.Add(self.username_label, flag=wx.LEFT | wx.TOP, border=10)

        self.username_text = wx.TextCtrl(inner_panel, style=wx.BORDER_SIMPLE)
        inner_vbox.Add(self.username_text, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.password_label = wx.StaticText(inner_panel, label="Password:")
        self.password_label.SetFont(label_font)
        inner_vbox.Add(self.password_label, flag=wx.LEFT | wx.TOP, border=10)

        self.password_text = wx.TextCtrl(inner_panel, style=wx.TE_PASSWORD | wx.BORDER_SIMPLE)
        inner_vbox.Add(self.password_text, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.login_button = wx.Button(inner_panel, label="Login")
        self.login_button.SetFont(font)
        self.login_button.SetBackgroundColour("#4CAF50")  # Green
        self.login_button.SetForegroundColour(wx.WHITE)
        self.login_button.Bind(wx.EVT_BUTTON, self.on_login)
        inner_vbox.Add(self.login_button, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        self.register_button = wx.Button(inner_panel, label="Register")
        self.register_button.SetFont(font)
        self.register_button.SetBackgroundColour("#2196F3")  # Blue
        self.register_button.SetForegroundColour(wx.WHITE)
        self.register_button.Bind(wx.EVT_BUTTON, self.on_register)
        inner_vbox.Add(self.register_button, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        inner_panel.SetSizer(inner_vbox)
        vbox.Add(inner_panel, flag=wx.EXPAND | wx.ALL, border=20)
        panel.SetSizer(vbox)

    def on_login(self, event):
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()
        if self.user_db.validate_user(username, password):
            if perform_calibration():
                wx.MessageBox('Calibration successful', 'Info', wx.OK | wx.ICON_INFORMATION)
                self.Hide()
                from ui.main_frame import MainFrame  # Lazy import to avoid circular dependency
                frame = MainFrame(None, "Main App", username)
                frame.Show()
            else:
                wx.MessageBox('Calibration failed', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox('Invalid username or password', 'Error', wx.OK | wx.ICON_ERROR)

    def on_register(self, event):
        dlg = RegistrationDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
