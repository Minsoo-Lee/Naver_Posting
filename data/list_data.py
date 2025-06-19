class ListData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ListData, cls).__new__(cls)
            cls._instance._initialized = False  # 여기서 플래그 설정
        return cls._instance

    def __init__(self):
        self.account_list = None
        self.keyword_list = None
        self.blog_list = None
        self.cafe_list = None

    # 리스트 세팅
    def set_account_list(self, account_list):
        self.account_list = account_list

    def set_keyword_list(self, keyword_list):
        self.keyword_list = keyword_list

    def set_blog_list(self, blog_list):
        self.blog_list = blog_list

    def set_cafe_list(self, cafe_list):
        self.cafe_list = cafe_list

    # 리스트 활성화 설정
    def account_list_Enable(self, boolean):
        self.account_list.Enable(boolean)

    def keyword_list_Enable(self, boolean):
        self.keyword_list.Enable(boolean)

    def blog_list_Enable(self, boolean):
        self.blog_list.Enable(boolean)

    def cafe_list_Enable(self, boolean):
        self.cafe_list.Enable(boolean)