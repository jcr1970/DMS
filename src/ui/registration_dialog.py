# src/ui/registration_dialog.py

import wx

class RegistrationDialog(wx.Dialog):
    def __init__(self, parent):
        super(RegistrationDialog, self).__init__(parent, title="Register", size=(400, 400))

        vbox = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        label_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        self.first_name_label = wx.StaticText(self, label="First Name:")
        self.first_name_label.SetFont(label_font)
        vbox.Add(self.first_name_label, flag=wx.LEFT | wx.TOP, border=10)
        self.first_name_text = wx.TextCtrl(self, style=wx.BORDER_SIMPLE)
        vbox.Add(self.first_name_text, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.last_name_label = wx.StaticText(self, label="Last Name:")
        self.last_name_label.SetFont(label_font)
        vbox.Add(self.last_name_label, flag=wx.LEFT | wx.TOP, border=10)
        self.last_name_text = wx.TextCtrl(self, style=wx.BORDER_SIMPLE)
        vbox.Add(self.last_name_text, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.email_label = wx.StaticText(self, label="Email:")
        self.email_label.SetFont(label_font)
        vbox.Add(self.email_label, flag=wx.LEFT | wx.TOP, border=10)
        self.email_text = wx.TextCtrl(self, style=wx.BORDER_SIMPLE)
        vbox.Add(self.email_text, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.username_label = wx.StaticText(self, label="Username:")
        self.username_label.SetFont(label_font)
        vbox.Add(self.username_label, flag=wx.LEFT | wx.TOP, border=10)
        self.username_text = wx.TextCtrl(self, style=wx.BORDER_SIMPLE)
        vbox.Add(self.username_text, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.password_label = wx.StaticText(self, label="Password:")
        self.password_label.SetFont(label_font)
        vbox.Add(self.password_label, flag=wx.LEFT | wx.TOP, border=10)
        self.password_text = wx.TextCtrl(self, style=wx.TE_PASSWORD | wx.BORDER_SIMPLE)
        vbox.Add(self.password_text, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.register_button = wx.Button(self, label="Register")
        self.register_button.SetFont(font)
        self.register_button.SetBackgroundColour("#2196F3")  # Blue
        self.register_button.SetForegroundColour(wx.WHITE)
        self.register_button.Bind(wx.EVT_BUTTON, self.on_register)
        vbox.Add(self.register_button, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        self.SetSizerAndFit(vbox)

    def on_register(self, event):
        first_name = self.first_name_text.GetValue()
        last_name = self.last_name_text.GetValue()
        email = self.email_text.GetValue()
        username = self.username_text.GetValue()
        password = self.password_text.GetValue()

        if first_name and last_name and email and username and password:
            if self.GetParent().user_db.create_user(username, password, first_name, last_name, email):
                wx.MessageBox('User registered successfully', 'Info', wx.OK | wx.ICON_INFORMATION)
                self.Close()
            else:
                wx.MessageBox('Username already exists', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox('Please fill in all fields', 'Error', wx.OK | wx.ICON_ERROR)
