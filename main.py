import ui.window as window
import wx
from auth.auth_window import AuthDialog

def open_auth_dialog():
    auth_dialog = AuthDialog()
    auth_dialog.ShowModal()
    result = auth_dialog.auth_success
    auth_dialog.Destroy()
    return result


if __name__ == "__main__":
    app = wx.App(False)
    frame = window.MainFrame()
    frame.Show()
    app.MainLoop()

