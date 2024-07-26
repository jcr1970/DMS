# src/ui/main_ui.py

import wx
from ui.login_frame import LoginFrame

class MainApp(wx.App):
    def OnInit(self):
        frame = LoginFrame(None, "Login")
        frame.Show()
        return True

