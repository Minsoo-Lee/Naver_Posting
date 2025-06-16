import wx
from wx import Button
import wx.richtext as rt
from ui import log
from task.task_thread import make_thread_task

app = wx.App(False)
frame = wx.Frame(None, wx.ID_ANY, "Naver Posting")

panel = wx.Panel(frame, wx.ID_ANY)
# panel.SetBackgroundColour(wx.Colour(160, 30, 240))
panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
frame_sizer = wx.BoxSizer(wx.HORIZONTAL)

# ========================================================================================================
# 좌측: ID, PW, 업체 업로드 버튼 & 리스트 박스, 웹 주소 업로드 버튼 & 리스트 박스
left_panel = wx.Panel(panel, wx.ID_ANY)
left_box = wx.StaticBox(left_panel)
left_sizer = wx.StaticBoxSizer(left_box, wx.VERTICAL)

data_panel = wx.Panel(left_panel, wx.ID_ANY)
data_box = wx.StaticBox(data_panel)
data_sizer = wx.StaticBoxSizer(data_box, wx.VERTICAL)

# button_panel = wx.Panel(panel, wx.ID_ANY)
# button_sizer = wx.BoxSizer(wx.HORIZONTAL)

# ID, PW 받아 오기
id_input_label = wx.StaticText(data_panel, wx.ID_ANY, "ID", size=(80, 20))
id_input = wx.TextCtrl(data_panel, wx.ID_ANY, size=(150, 20))

id_sizer = wx.BoxSizer(wx.HORIZONTAL)
id_sizer.Add(id_input_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)  # wx.ALIGN_CENTER_VERTICAL로 수직 가운데 정렬
id_sizer.Add(id_input, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

pw_input_label = wx.StaticText(data_panel, wx.ID_ANY, "PW", size=(80, 20))
pw_input = wx.TextCtrl(data_panel, wx.ID_ANY, size=(150, 20), style=wx.TE_PASSWORD)

pw_sizer = wx.BoxSizer(wx.HORIZONTAL)
pw_sizer.Add(pw_input_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)  # wx.ALIGN_CENTER_VERTICAL로 수직 가운데 정렬
pw_sizer.Add(pw_input, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

data_sizer.Add(id_sizer, 0, wx.ALL, 5)
data_sizer.Add(pw_sizer, 0, wx.ALL, 5)
data_panel.SetSizer(data_sizer)

# 버튼 설정 (업체 업로드)
company_panel = wx.Panel(left_panel, wx.ID_ANY)
company_box = wx.StaticBox(company_panel)
company_sizer = wx.StaticBoxSizer(company_box, wx.VERTICAL)

# 업체 버튼 설정
company_button: Button = wx.Button(company_panel, wx.ID_ANY, "업체 업로드", size=wx.Size(250, 50))
# server_button.Bind(wx.EVT_BUTTON,)
company_button.Enable(True)

company_list = wx.ListCtrl(company_panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=wx.Size(250, 200))
company_list.InsertColumn(0, "주소", width=120)
company_list.InsertColumn(1, "업체", width=130)

company_sizer.Add(company_button, 0, wx.TOP, 3)
company_sizer.Add(company_list, 0, wx.ALL, 5)
company_panel.SetSizer(company_sizer)

# 버튼 설정 (웹 주소 업로드)
web_panel = wx.Panel(left_panel, wx.ID_ANY)
web_box = wx.StaticBox(web_panel)
web_sizer = wx.StaticBoxSizer(web_box, wx.VERTICAL)

# 업체 버튼 설정
web_button: Button = wx.Button(web_panel, wx.ID_ANY, "웹주소 및 카테고리 업로드", size=wx.Size(250, 50))
# server_button.Bind(wx.EVT_BUTTON,)
web_button.Enable(True)

web_list = wx.ListCtrl(web_panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=wx.Size(250, 200))
web_list.InsertColumn(0, "이름", width=120)
web_list.InsertColumn(1, "카테고리", width=130)

web_sizer.Add(web_button, 0, wx.ALL, 5)
web_sizer.Add(web_list, 0, wx.ALL, 5)
web_panel.SetSizer(web_sizer)

# panel_sizer에 추가할 때 반드시 wx.EXPAND
left_sizer.Add(data_panel, 0, wx.EXPAND | wx.ALL, 5)
left_sizer.Add(company_panel, 0, wx.EXPAND | wx.ALL, 5)
left_sizer.Add(web_panel, 0, wx.EXPAND | wx.ALL, 5)
left_panel.SetSizer(left_sizer)

# ====================================================================
# 구분선1 추가
separator_left = wx.Panel(panel, size=(2, -1))  # 너비 2픽셀, 높이는 자동 확장
separator_left.SetBackgroundColour(wx.Colour(200, 200, 200))  # 연한 회색

# ====================================================================
# 가운데 패널: 본문 텍스트 형식 지정
middle_panel = wx.Panel(panel, wx.ID_ANY)
middle_box = wx.StaticBox(middle_panel)
middle_sizer = wx.StaticBoxSizer(middle_box, wx.VERTICAL)

# 안내글 표시
form_label = wx.StaticText(middle_panel, wx.ID_ANY, "폼 형식 지정 안내글 - 추후에 채울 예정", size=(300, 200))
form_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
form_label_sizer.Add(form_label, 0, wx.ALL, 5)

# 텍스트 형식 입력
from_input = wx.TextCtrl(middle_panel, style=wx.TE_MULTILINE, size=(300, 370))
form_input_sizer = wx.BoxSizer(wx.VERTICAL)
form_input_sizer.Add(from_input, 1, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 3)

# 작업 수행 버튼
task_button: Button = wx.Button(middle_panel, wx.ID_ANY, "작업 수행", size=wx.Size(300, 50))
task_button.Bind(wx.EVT_BUTTON, lambda event: make_thread_task(id_input.Value, pw_input.Value))
task_button.Enable(True)
task_button_sizer = wx.BoxSizer(wx.VERTICAL)
task_button_sizer.Add(task_button, 0)

middle_sizer.Add(form_label_sizer, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
middle_sizer.Add(form_input_sizer, 1, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
middle_sizer.Add(task_button_sizer, 0, wx.TOP | wx.LEFT | wx.RIGHT | wx.EXPAND, 3)
middle_panel.SetSizer(middle_sizer)

# ====================================================================
# 구분선2 추가
separator_right = wx.Panel(panel, size=(2, -1))  # 너비 2픽셀, 높이는 자동 확장
separator_right.SetBackgroundColour(wx.Colour(200, 200, 200))  # 연한 회색

# ====================================================================
# 로그 창 설정
log_panel = wx.Panel(panel, wx.ID_ANY)
log_box = wx.StaticBox(log_panel, wx.ID_ANY)
log_sizer = wx.StaticBoxSizer(log_box, wx.VERTICAL)

log_label = wx.StaticText(log_panel, wx.ID_ANY, "로그 화면", size=(80, 20))

log_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
log_label_sizer.Add(log_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)  # wx.ALIGN_CENTER_VERTICAL로 수직 가운데 정렬

log_text_widget = rt.RichTextCtrl(log_panel, style=wx.TE_MULTILINE | wx.BORDER_THEME | wx.TE_READONLY, size=(350, 500))
log.set_log_widget(log_text_widget)  # 여기서 위젯 연결

log_sizer.Add(log_label_sizer, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
log_sizer.Add(log_text_widget, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
log_panel.SetSizer(log_sizer)

panel_sizer.Add(left_panel, 0, wx.EXPAND | wx.ALL, 5)
panel_sizer.Add(separator_left, 0, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT | wx.RIGHT, 10)
panel_sizer.Add(middle_panel, 0, wx.EXPAND | wx.ALL, 5)
panel_sizer.Add(separator_right, 0, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT | wx.RIGHT, 10)
panel_sizer.Add(log_panel, 0, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT | wx.RIGHT, 10)
panel.SetSizer(panel_sizer)

frame_sizer.Add(panel, 1, wx.EXPAND)
frame.SetSizerAndFit(frame_sizer)

frame.Show()
app.MainLoop()


#
# # 버튼 설정 (업체 업로드, 웹 주소 업로드)
# button_panel = wx.Panel(panel, wx.ID_ANY)
# button_sizer = wx.BoxSizer(wx.HORIZONTAL)
#
# # 업체 버튼 설정
# server_button: Button = wx.Button(data_panel, wx.ID_ANY, "서버 시작", size=wx.Size(170, 30))
# # server_button.Bind(wx.EVT_BUTTON,)
# server_button.Enable(True)
#
# # task 버튼 설정
# task_button: Button = wx.Button(data_panel, wx.ID_ANY, "작업 수행", size=wx.Size(170, 30))
# # task_button.Bind(wx.EVT_BUTTON,)
# task_button.Enable(False)
#
#
# # button_sizer.Add(crawling_button, 0)
# button_sizer.Add(server_button, 0, wx.LEFT, 5)
# button_sizer.Add(task_button, 0, wx.LEFT, 15)
#
# data_panel.SetSizer(button_sizer)
#
# # 우측: 로그 창 설정
# log_panel = wx.Panel(panel, wx.ID_ANY)
# log_sizer = wx.BoxSizer(wx.HORIZONTAL)
#
# log_text_widget = rt.RichTextCtrl(log_panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(350, 500))
# log.set_log_widget(log_text_widget)  # 여기서 위젯 연결
#
# log_sizer.Add(log_text_widget, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
# log_panel.SetSizer(log_sizer)
#
# panel_sizer.Add(data_panel, 0, wx.EXPAND | wx.ALL, border=5)
# panel_sizer.Add(log_panel, 0, wx.EXPAND, 5)
#
# panel.SetSizer(panel_sizer)
#
# frame_sizer.Add(panel, 1, wx.EXPAND)
# frame.SetSizerAndFit(frame_sizer)
#
# frame.Show()
# app.MainLoop()