# import ui.window as window
import wx
from ui import window  # 위에서 만든 프레임 불러오기
from cache import upload_cache

if __name__ == "__main__":
    app = wx.App(False)
    frame = window.MainFrame()
    app.MainLoop()