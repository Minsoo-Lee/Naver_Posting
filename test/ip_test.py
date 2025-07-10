import wx
from ip import ip_trans

# 앱 초기화
app = wx.App(False)
frame = wx.Frame(None, title="IP 우회 테스트", size=(300, 200))
panel = wx.Panel(frame)

# 버튼 생성
top_button = wx.Button(panel, label="현재 IP 확인")
bottom_button = wx.Button(panel, label="비행기모드 on/off")

def current_ip():
    print(ip_trans.get_current_ip())

# 이벤트 바인딩
top_button.Bind(wx.EVT_BUTTON, current_ip)
bottom_button.Bind(wx.EVT_BUTTON, lambda event: ip_trans.toggle_airplane_mode())

# 수직 정렬
sizer = wx.BoxSizer(wx.VERTICAL)
sizer.Add(top_button, 0, wx.ALIGN_CENTER | wx.TOP, 30)
sizer.AddStretchSpacer()
sizer.Add(bottom_button, 0, wx.ALIGN_CENTER | wx.BOTTOM, 30)
panel.SetSizer(sizer)

# 창 중앙에 표시
frame.Centre()
frame.Show()

# 앱 루프 실행
app.MainLoop()