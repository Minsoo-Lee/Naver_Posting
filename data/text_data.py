class TextData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TextData, cls).__new__(cls)
            cls._instance._initialized = False  # 여기서 플래그 설정
        return cls._instance

    def __init__(self):
        if self._initialized:
            return  # 이미 초기화된 경우, 바로 리턴

        self.status_label = None
        self.phone_number = None

    def set_status_label(self, status_label):
        self.status_label = status_label

    def set_phone_number(self, phone_number):
        self.phone_number = phone_number