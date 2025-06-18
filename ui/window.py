import wx
from ui.panel_builder import PanelBuilder

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, wx.ID_ANY, "Naver Posting")


        self.separator_left = None
        self.separator_right = None

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.ui = PanelBuilder(self.panel)

        # 좌측 위, 아래 통합 패널
        self.left_panel = wx.Panel(self.panel, wx.ID_ANY)
        self.left_sizer = wx.BoxSizer(wx.VERTICAL)

        # 좌측 위: 현재 상태 표시 & 상태 선택
        self.left_up_panel = self.ui.add_left_up(self.left_panel)
        # 좌측 아래: ID, PW, 업체 업로드 버튼 & 리스트 박스, 웹 주소 업로드 버튼 & 리스트 박스
        self.left_panel_box = self.ui.add_left_box(self.left_panel)


        # 가운데 패널
        self.middle_panel = self.ui.add_middle()
        # 로그 패널
        self.log_panel = self.ui.add_right()

        self.panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.frame_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.init_ui()
        self.set_layout()
        self.set_position_and_show()

    def init_ui(self):
        # 구분선 1
        self.separator_left = wx.Panel(self.panel, size=(2, -1))
        self.separator_left.SetBackgroundColour(wx.Colour(200, 200, 200))

        # 구분선 2
        self.separator_right = wx.Panel(self.panel, size=(2, -1))
        self.separator_right.SetBackgroundColour(wx.Colour(200, 200, 200))

    def set_layout(self):
        self.left_sizer.Add(self.left_up_panel,0, wx.EXPAND | wx.ALL, 5)
        self.left_sizer.Add(self.left_panel_box, 0, wx.EXPAND | wx.ALL, 5)
        self.left_panel.SetSizer(self.left_sizer)

        self.panel_sizer.Add(self.left_panel, 0, wx.EXPAND | wx.ALL, 5)
        self.panel_sizer.Add(self.separator_left, 0, wx.EXPAND | wx.ALL, 10)
        self.panel_sizer.Add(self.middle_panel, 0, wx.EXPAND | wx.ALL, 5)
        self.panel_sizer.Add(self.separator_right, 0, wx.EXPAND | wx.ALL, 10)
        self.panel_sizer.Add(self.log_panel, 0, wx.EXPAND | wx.ALL, 10)

        self.panel.SetSizer(self.panel_sizer)
        self.frame_sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizerAndFit(self.frame_sizer)

    def set_position_and_show(self):
        display_width, display_height = wx.GetDisplaySize()
        frame_width, frame_height = self.GetSize()

        x = (display_width - frame_width) // 2
        y = 30  # 위에서 약간 띄우기

        self.SetPosition(wx.Point(x, y))
        self.Show()
