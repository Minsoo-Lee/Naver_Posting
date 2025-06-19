class BoxData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BoxData, cls).__new__(cls)
            cls._instance._initialized = False  # 여기서 플래그 설정
        return cls._instance

    def __init__(self):
        self.status_rb = None
        self.comment_cb = None

    # 박스 세팅
    def set_status_rb(self, status_rb):
        self.status_rb = status_rb

    def set_comment_cb(self, comment_cb):
        self.comment_cb = comment_cb

    # 박스 활성화 설정
    def comment_cb_Enable(self, boolean):
        self.comment_cb.Enable(boolean)