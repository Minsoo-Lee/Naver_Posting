class BoxData:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BoxData, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if BoxData._initialized:
            return  # 이미 초기화된 경우, 바로 리턴

        self.status_rb = None
        self.comment_cb = None
        BoxData._initialized = True

    # 박스 세팅
    def set_status_rb(self, status_rb):
        self.status_rb = status_rb

    def set_comment_cb(self, comment_cb):
        self.comment_cb = comment_cb

    # 박스 활성화 설정
    def comment_cb_Enable(self, boolean):
        self.comment_cb.Enable(boolean)