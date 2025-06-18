import wx
import wx.richtext as rt
from selenium.webdriver.support.expected_conditions import none_of

from ui import section
from ui import log

class PanelBuilder:
    def __init__(self, parent_panel):
        self.parent_panel = parent_panel

        # 멤버 변수
        self.status_label = None

        self.account_web_panel = None
        self.account_web_sizer = None
        self.web_panel = None  # 현재 들어간 blog_section 또는 cafe_section

        # 버튼 멤버 변수
        self.keyword_button = None
        self.account_button = None
        self.web_button = None
        self.execute_button = None

        # 리스트 멤버 변수
        self.keyword_list = None
        self.account_list = None
        self.web_list = None

    def on_radio_selected(self, event):
        selected = event.GetString()  # '카페' 또는 '블로그'
        if self.status_label:
            self.status_label.SetLabel(selected)
        if self.account_web_panel and self.account_web_sizer and self.web_panel:
            # 새 패널 생성
            new_panel = section.cafe_section(self.account_web_panel) if selected == "카페" \
                else section.blog_section(self.account_web_panel)

            # 패널 교체
            self.account_web_sizer.Replace(self.web_panel, new_panel)
            self.web_panel.Destroy()  # 기존 패널은 수동으로 제거
            self.web_panel = new_panel

            self.account_web_panel.Layout()

    def add_left_up(self, left_panel):
        panel = wx.Panel(left_panel, wx.ID_ANY)
        box = wx.StaticBox(panel)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        # 현재 상태 표시
        status_panel, status_label = section.current_status_label(panel)
        self.status_label = status_label

        # 상태 선택(라디오 박스)
        rb_panel, radio_box = section.platform_radio_box(panel)

        radio_box.Bind(wx.EVT_RADIOBOX, self.on_radio_selected)

        sizer.Add(status_panel, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(rb_panel, 0, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)

        return panel

    def add_left_box(self, left_panel):
        panel = wx.Panel(left_panel, wx.ID_ANY)
        box = wx.StaticBox(panel)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        # 핸드폰 번호 입력 섹션
        phone_panel = section.phone_section(panel)

        # 키워드 섹션 추가
        keyword_panel, keyword_button, keyword_list = section.keyword_section(panel)

        # 계정 + 웹주소 섹션
        account_web = section.account_web_section(panel)
        self.account_web_panel = account_web.parent_panel
        self.account_web_sizer = account_web.parent_sizer
        self.web_panel = account_web.child_panel  # 처음엔 blog_section이 들어가 있음
        self.account_button = account_web.account_button
        self.account_list = account_web.account_list
        self.web_button = account_web.child_button
        self.web_list = account_web.web_list


        sizer.Add(phone_panel, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(keyword_panel, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(account_web_panel, 0, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(sizer)

        return panel

    def add_middle(self):
        panel = wx.Panel(self.parent_panel, wx.ID_ANY)
        box = wx.StaticBox(panel)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        # 안내문
        form_label_sizer = section.inform_section(panel)

        # 본문 작성란
        form_input_sizer = section.content_input_section(panel)

        # 실행 버튼
        task_button_sizer = section.execute_section(panel)

        sizer.Add(form_label_sizer, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        sizer.Add(form_input_sizer, 1, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
        sizer.Add(task_button_sizer, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 3)

        panel.SetSizer(sizer)
        return panel

    def add_right(self):
        panel = wx.Panel(self.parent_panel, wx.ID_ANY)
        box = wx.StaticBox(panel)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        log_label = wx.StaticText(panel, wx.ID_ANY, "로그 화면", size=(80, 20))

        log_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        log_label_sizer.Add(log_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        log_text_widget = rt.RichTextCtrl(
            panel,
            style=wx.TE_MULTILINE | wx.BORDER_THEME | wx.TE_READONLY,
            size=(350, 500)
        )
        log.set_log_widget(log_text_widget)

        sizer.Add(log_label_sizer, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(log_text_widget, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(sizer)
        return panel
