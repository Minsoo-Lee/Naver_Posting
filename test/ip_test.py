import wx
from ip import ip

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="IP 우회 테스트", size=(300, 200))

        panel = wx.Panel(self)

        # 버튼 2개 생성
        self.top_button = wx.Button(panel, label="현재 IP 확인")
        self.bottom_button = wx.Button(panel, label="비행기모드 on/off")

        # 이벤트 바인딩
        self.top_button.Bind(wx.EVT_BUTTON, ip.get_current_ip)
        self.bottom_button.Bind(wx.EVT_BUTTON, ip.toggle_airplane_mode())

        # 수직 정렬을 위한 sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.top_button, 0, wx.ALIGN_CENTER | wx.TOP, 30)     # 위 버튼, 위쪽에 여백
        sizer.AddStretchSpacer()                                       # 중간 공간
        sizer.Add(self.bottom_button, 0, wx.ALIGN_CENTER | wx.BOTTOM, 30)  # 아래 버튼, 아래쪽 여백

        panel.SetSizer(sizer)

        self.Centre()
        self.Show()

    def on_top_click(self, event):
        wx.MessageBox("위쪽 버튼이 클릭되었습니다!", "알림")

    def on_bottom_click(self, event):
        wx.MessageBox("아래쪽 버튼이 클릭되었습니다!", "알림")

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()