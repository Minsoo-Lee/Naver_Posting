from data.box_data import BoxData
from data.button_data import ButtonData
from data.list_data import ListData
from data.text_data import TextData


class Binding:
    def __init__(self):
        self.buttons = ButtonData()
        self.boxes = BoxData()
        self.texts = TextData()
        self.lists = ListData()

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

