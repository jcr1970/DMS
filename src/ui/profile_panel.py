# src/ui/profile_panel.py

import wx
from utils.user_database import UserDatabase

class ProfilePanel(wx.Panel):
    def __init__(self, parent, username):
        super(ProfilePanel, self).__init__(parent, style=wx.TRANSPARENT_WINDOW)
        self.username = username
        self.user_db = UserDatabase()
        self.init_ui()

    def init_ui(self):
        self.SetBackgroundColour(wx.Colour(255, 255, 255, 0))  # Transparent background

        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        vbox = wx.BoxSizer(wx.VERTICAL)

        user_info = self.user_db.get_user_info(self.username)

        self.profile_username_label = wx.StaticText(self, label=f"Username: {self.username}")
        self.profile_username_label.SetFont(font)
        vbox.Add(self.profile_username_label, flag=wx.ALL, border=10)

        self.profile_first_name_label = wx.StaticText(self, label=f"First Name: {user_info[0]}")
        self.profile_first_name_label.SetFont(font)
        vbox.Add(self.profile_first_name_label, flag=wx.ALL, border=10)

        self.profile_last_name_label = wx.StaticText(self, label=f"Last Name: {user_info[1]}")
        self.profile_last_name_label.SetFont(font)
        vbox.Add(self.profile_last_name_label, flag=wx.ALL, border=10)

        self.profile_email_label = wx.StaticText(self, label=f"Email: {user_info[2]}")
        self.profile_email_label.SetFont(font)
        vbox.Add(self.profile_email_label, flag=wx.ALL, border=10)

        self.profile_password_label = wx.StaticText(self, label="Password: ****")
        self.profile_password_label.SetFont(font)
        vbox.Add(self.profile_password_label, flag=wx.ALL, border=10)

        self.change_password_button = wx.Button(self, label="Change Password")
        self.change_password_button.SetFont(font)
        self.change_password_button.SetBackgroundColour("#FF9800")  # Orange
        self.change_password_button.SetForegroundColour(wx.WHITE)
        self.change_password_button.Bind(wx.EVT_BUTTON, self.change_password)
        vbox.Add(self.change_password_button, flag=wx.ALL, border=10)

        self.delete_profile_button = wx.Button(self, label="Delete Profile")
        self.delete_profile_button.SetFont(font)
        self.delete_profile_button.SetBackgroundColour("#FF0000")  # Red
        self.delete_profile_button.SetForegroundColour(wx.WHITE)
        self.delete_profile_button.Bind(wx.EVT_BUTTON, self.delete_profile)
        vbox.Add(self.delete_profile_button, flag=wx.ALL, border=10)

        self.SetSizerAndFit(vbox)

    def change_password(self, event):
        dlg = wx.TextEntryDialog(self, 'Enter new password:', 'Change Password')
        if dlg.ShowModal() == wx.ID_OK:
            new_password = dlg.GetValue()
            self.user_db.change_password(self.username, new_password)
            wx.MessageBox('Password changed successfully', 'Info', wx.OK | wx.ICON_INFORMATION)
        dlg.Destroy()

    def delete_profile(self, event):
        dlg = wx.MessageDialog(self, 'Are you sure you want to delete your profile?', 'Confirm Delete', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)
        if dlg.ShowModal() == wx.ID_YES:
            self.user_db.delete_user(self.username)
            wx.MessageBox('Profile deleted successfully', 'Info', wx.OK | wx.ICON_INFORMATION)
            self.GetParent().logout(event)
        dlg.Destroy()
