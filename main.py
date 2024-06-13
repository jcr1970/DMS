# main.py
import wx
from ui.main_ui import LoginScreen, CameraApp

class MainApp(wx.App):
    def OnInit(self):
        login_screen = LoginScreen(None, self.on_login)
        login_screen.Show(True)
        return True
    
    def on_login(self, username):
        camera_app = CameraApp(None, username)
        camera_app.Show(True)

if __name__ == "__main__":
    app = MainApp(False)
    app.MainLoop()
