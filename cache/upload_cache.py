import os, json, csv
from data import list_data, text_data

lists = list_data.ListData()
texts = text_data.TextData()
is_exist = False

# def is_JSON_exist():
#     file_path = os.path.join(os.getcwd(), "cache", ".cache_text")
#     if os.path.isfile(file_path):
#         return True
#     else:
#         return False

def upload_JSON():
    file_path = os.path.join(os.getcwd(), "cache", ".cache_text")
    if os.path.isfile(file_path):
        print("✅ .cache_text 파일이 존재합니다.")
        with open("cache/.cache_text", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}


def show_text():
    text_json = upload_JSON()
    text_list = [
        texts.waiting_max, texts.waiting_min, texts.api_number, texts.phone_number, texts.content_input
    ]
    text_keys = [
        "waiting_max", "waiting_min", "api_number", "phone_number", "content_input"
    ]
    for text_input, key in zip(text_list, text_keys):
        print(text_input)
        print(key)
        text_input.SetValue(text_json.get(key, ""))


def upload_CSV(file_name):
    file_path = os.path.join(os.getcwd(), "cache", file_name)
    if os.path.isfile(file_path):
        print("✅ .cache_text 파일이 존재합니다.")
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            return [row for row in reader]
    else:
        return None


def show_lists():
    list_ctrl_list = [lists.account_list, lists.keyword_list, lists.blog_list, lists.cafe_list]
    csv_names = [".cache_account", ".cache_keyword", ".cache_blog", ".cache_cafe"]

    for idx in range(len(csv_names)):
        data = upload_CSV(csv_names[idx])
        if not data or len(data) < 1:
            continue  # 데이터가 없거나 비어 있으면 넘어감

        list_ctrl = list_ctrl_list[idx]
        list_ctrl.DeleteAllItems()  # 기존 항목 삭제

        headers = data[0]
        rows = data[1:]

        # 컬럼 초기화
        for col in range(list_ctrl.GetColumnCount()):
            list_ctrl.DeleteColumn(0)
        for col_idx, header in enumerate(headers):
            list_ctrl.InsertColumn(col_idx, header)

        # 데이터 삽입
        for row in rows:
            if not row:
                continue
            item_index = list_ctrl.InsertItem(list_ctrl.GetItemCount(), row[0])
            for col_idx in range(1, len(row)):
                list_ctrl.SetItem(item_index, col_idx, row[col_idx])