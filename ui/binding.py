from data.box_data import BoxData
from data.button_data import ButtonData
from data.list_data import ListData
from data.parsing_data import ParseData
from data.text_data import TextData
import wx, csv

from task.task_thread import make_thread_task
from ui import log

class Binding:
    def __init__(self):
        self.buttons = ButtonData()
        self.boxes = BoxData()
        self.texts = TextData()
        self.lists = ListData()
        self.parsing_data = ParseData()

        self.parse_setter = []
        self.parse_getter = []
        self.list_collection = []
        self.LABEL_LIST = ["계정", "키워드", "블로그", "카페"]

    def on_radio_selected(self, event):
        selected = event.GetString()
        self.texts.status_label.SetLabel(selected)
        if selected == "카페":
            self.on_radio_selected_utils(False)
        elif selected == "블로그":
            self.on_radio_selected_utils(True)
        else:
            self.on_radio_selected_utils(True, False)


    def on_radio_selected_utils(self, boolean, is_each=True):
        # 블로그 활성화 다중 설정
        self.buttons.blog_button_Enable(boolean)
        self.lists.blog_list_Enable(boolean)

        # 카페 활성화 다중 설정
        self.buttons.cafe_button_Enable(not boolean if is_each else boolean)
        self.lists.cafe_list_Enable(not boolean if is_each else boolean)
        self.boxes.comment_cb_Enable(not boolean if is_each else boolean)

    def on_list_button_clicked(self, event, panel):

        self.set_collection()

        text = event.GetEventObject().GetLabel()
        index = -1
        found_indexes = [i for i, label in enumerate(self.LABEL_LIST) if label in text]
        if found_indexes:
            index = found_indexes[0]

        # 파일 불러오기 & 데이터 파싱
        self.upload_data(index, panel)

        # 멤버 변수를 지역 변수로 치환 (인덱스 접근 X)
        csv_data = self.parse_getter[index]()
        list_data = self.list_collection[index]

        # ListCtrl에 표시
        self.upload_list(csv_data, list_data, True if index == 0 else False)

    def set_collection(self):
        self.parse_setter = [
            self.parsing_data.set_account_data,
            self.parsing_data.set_keyword_data,
            self.parsing_data.set_blog_data,
            self.parsing_data.set_cafe_data
        ]

        self.parse_getter = [
            self.parsing_data.get_account_data,
            self.parsing_data.get_keyword_data,
            self.parsing_data.get_blog_data,
            self.parsing_data.get_cafe_data
        ]

        self.list_collection = [
            self.lists.account_list, self.lists.keyword_list, self.lists.blog_list, self.lists.cafe_list
        ]

    def upload_data(self, index, panel):
        # 파일 불러오기
        with wx.FileDialog(panel, "CSV 파일 선택", wildcard="CSV 파일 (*.csv)|*.csv",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return

            path = dialog.GetPath()
            try:
                with open(path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    self.parse_setter[index](list(reader))
            except FileNotFoundError as e:
                print(f"파일을 열 수 업습니다.\n{e}")

    def upload_list(self, csv_data, list_data, is_account):

        list_data.DeleteAllItems()

        # 유효성 검사 할 것 (데이터 열 개수와 리스트 행 개수가 맞는지)
        if len(csv_data[0]) != list_data.GetColumnCount() and is_account is False:
            log.append_log("[ERROR] 데이터의 열 개수와 리스트의 열 개수가 맞지 않습니다.파일의 열 개수를 다시 확인해주세요.")
            return

        for i in range(len(csv_data)):
            index = list_data.InsertItem(list_data.GetItemCount(), csv_data[i][0])
            if is_account is False:
                for j in range(1, len(csv_data[i])):
                    list_data.SetItem(index, j, csv_data[i][j])

    def on_execute_button_clicked(self, event, content_value):
        self.parsing_data.content_data = content_value
        make_thread_task()

