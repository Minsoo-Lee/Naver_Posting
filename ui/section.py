import wx

from data.account_web_section import AccountWebSection


# ================================ 좌측 패널 ================================================
# 명시적으로 나타내기 위해 함수를 각각 선언 (중복 부분 분리 X)

# 현재 상태 나타내는 라벨
def current_status_label(panel):
    status_panel = wx.Panel(panel, wx.ID_ANY)
    status_sizer = wx.BoxSizer(wx.HORIZONTAL)

    # "현재 상태: " -> 변하지 않는 값
    current_label =wx.StaticText(status_panel, wx.ID_ANY, "현재 상태:")
    status_label = wx.StaticText(status_panel, wx.ID_ANY, "블로그")

    font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
    status_label.SetFont(font)

    # 글자 색상 설정 (예: 빨간색)
    status_label.SetForegroundColour((255, 0, 0))

    status_sizer.Add(current_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)  # wx.ALIGN_CENTER_VERTICAL로 수직 가운데 정렬
    status_sizer.Add(status_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
    status_panel.SetSizer(status_sizer)

    return status_panel, status_label

def platform_radio_box(panel):
    rb_panel = wx.Panel(panel, wx.ID_ANY)
    rb_box = wx.StaticBox(rb_panel, wx.ID_ANY)
    rb_sizer = wx.StaticBoxSizer(rb_box, wx.VERTICAL)

    rb_title = wx.StaticText(rb_panel, wx.ID_ANY, "플랫폼 선택")

    rb_labels = ['블로그', '카페']
    radio_box = wx.RadioBox(rb_panel, -1,
                            size = (-1, -1),
                            choices=rb_labels,
                            majorDimension=2)

    rb_sizer.Add(rb_title, 0, wx.ALL, 5)
    rb_sizer.Add(radio_box, 0, wx.ALL , 5)
    rb_panel.SetSizer(rb_sizer)

    return rb_panel, radio_box


# 핸드폰 번호 입력
def phone_section(panel):
    phone_panel = wx.Panel(panel, wx.ID_ANY)
    phone_sizer = wx.BoxSizer(wx.VERTICAL)

    phone_input_label = wx.StaticText(phone_panel, wx.ID_ANY, "핸드폰 번호", size=(80, 20))
    phone_input = wx.TextCtrl(phone_panel, wx.ID_ANY, size=(150, 20))

    phone_input_sizer = wx.BoxSizer(wx.HORIZONTAL)
    phone_input_sizer.Add(phone_input_label, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)  # wx.ALIGN_CENTER_VERTICAL로 수직 가운데 정렬
    phone_input_sizer.Add(phone_input, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

    phone_sizer.Add(phone_input_sizer, 0, wx.ALL, 5)
    phone_panel.SetSizer(phone_sizer)

    return phone_panel

# 계정 박스
def account_section(panel):
    account_panel = wx.Panel(panel, wx.ID_ANY)
    account_sizer = wx.BoxSizer(wx.VERTICAL)

    # 업체 버튼 설정
    account_button = wx.Button(account_panel, wx.ID_ANY, "계정 업로드", size=wx.Size(250, 50))
    account_button.Enable(True)

    account_list = wx.ListCtrl(account_panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=wx.Size(250, 200))
    account_list.InsertColumn(0, "주소", width=120)
    account_list.InsertColumn(1, "업체", width=130)

    account_sizer.Add(account_button, 0, wx.ALL, border=3)
    account_sizer.Add(account_list, 0, wx.ALL, border=3)
    account_panel.SetSizer(account_sizer)

    return account_panel, account_button, account_list

# 키워드 박스
def keyword_section(panel):
    keyword_panel = wx.Panel(panel, wx.ID_ANY)
    keyword_box = wx.StaticBox(keyword_panel)
    keyword_sizer = wx.StaticBoxSizer(keyword_box, wx.VERTICAL)

    # 업체 버튼 설정
    keyword_button = wx.Button(keyword_panel, wx.ID_ANY, "키워드 업로드", size=wx.Size(250, 50))
    # server_button.Bind(wx.EVT_BUTTON,)
    keyword_button.Enable(True)

    keyword_list = wx.ListCtrl(keyword_panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=wx.Size(550, 200))
    keyword_list.InsertColumn(0, "주소", width=120)
    keyword_list.InsertColumn(1, "업체", width=130)

    keyword_sizer.Add(keyword_button, 0, wx.ALL, border=3)
    keyword_sizer.Add(keyword_list, 0, wx.ALL, border=3)
    keyword_panel.SetSizer(keyword_sizer)

    return keyword_panel, keyword_button, keyword_list

# 카페 박스
def cafe_section(panel):
    cafe_panel = wx.Panel(panel, wx.ID_ANY)
    cafe_sizer = wx.BoxSizer(wx.VERTICAL)

    # 업체 버튼 설정
    cafe_button = wx.Button(cafe_panel, wx.ID_ANY, "카페 업로드", size=wx.Size(250, 50))
    # server_button.Bind(wx.EVT_BUTTON,)
    cafe_button.Enable(True)

    cafe_list = wx.ListCtrl(cafe_panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=wx.Size(250, 200))
    cafe_list.InsertColumn(0, "이름", width=120)
    cafe_list.InsertColumn(1, "카테고리", width=130)

    cafe_sizer.Add(cafe_button, 0, wx.ALL, 3)
    cafe_sizer.Add(cafe_list, 0, wx.ALL, 3)
    cafe_panel.SetSizer(cafe_sizer)

    return cafe_panel, cafe_button, cafe_list

# 카페 박스
def blog_section(panel):
    blog_panel = wx.Panel(panel, wx.ID_ANY)
    blog_sizer = wx.BoxSizer(wx.VERTICAL)

    # 업체 버튼 설정
    blog_button = wx.Button(blog_panel, wx.ID_ANY, "블로그 업로드", size=wx.Size(250, 50))
    # server_button.Bind(wx.EVT_BUTTON,)
    blog_button.Enable(True)

    blog_list = wx.ListCtrl(blog_panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, size=wx.Size(250, 200))
    blog_list.InsertColumn(0, "이름", width=120)
    blog_list.InsertColumn(1, "카테고리", width=130)

    blog_sizer.Add(blog_button, 0, wx.ALL, 3)
    blog_sizer.Add(blog_list, 0, wx.ALL, 3)
    blog_panel.SetSizer(blog_sizer)

    return blog_panel, blog_button, blog_list

# 웹주소 섹션, 계정 섹션을 박스 하나에 배치
def account_web_section(panel):
    account_web_panel = wx.Panel(panel, wx.ID_ANY)
    account_web_box = wx.StaticBox(account_web_panel)
    account_web_sizer = wx.StaticBoxSizer(account_web_box, wx.HORIZONTAL)

    account_panel, account_button, account_list = account_section(account_web_panel)
    web_panel, web_button, web_list = blog_section(account_web_panel)

    account_web_sizer.Add(account_panel, 0, wx.RIGHT, 50)
    account_web_sizer.Add(web_panel, 0, wx.ALL)
    account_web_panel.SetSizer(account_web_sizer)



    return AccountWebSection(
        parent_panel=account_web_panel,
        parent_sizer=account_web_sizer,
        child_panel=web_panel,
        account_button=account_button,
        account_list=account_list,
        web_button=web_button,
        web_list=web_list
    )

# ================================ 좌측 패널 ================================================
# 안내글 표시
def inform_section(panel):
    form_label = wx.StaticText(panel, wx.ID_ANY, "폼 형식 지정 안내글 - 추후에 채울 예정", size=(300, 400))
    form_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
    form_label_sizer.Add(form_label, 0, wx.ALL, 5)

    return form_label_sizer

# 텍스트 형식 입력
def content_input_section(panel):
    form_input = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=(300, 400))
    form_input_sizer = wx.BoxSizer(wx.VERTICAL)
    form_input_sizer.Add(form_input, 1, wx.TOP | wx.LEFT | wx.RIGHT, 3)

    return form_input_sizer

# 작업 수행 버튼
def execute_section(panel):
    task_button = wx.Button(panel, wx.ID_ANY, "작업 수행", size=wx.Size(300, 50))
    # task_button.Bind(wx.EVT_BUTTON, lambda event: make_thread_task(id_input.Value, pw_input.Value))
    task_button.Enable(True)
    task_button_sizer = wx.BoxSizer(wx.VERTICAL)
    task_button_sizer.Add(task_button, 0)

    return task_button_sizer