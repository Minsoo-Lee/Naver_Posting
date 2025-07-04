import random


class ContentData:
    _instance = None
    _initialized = False  # 여기서 플래그 설정

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ContentData, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if ContentData._initialized:
            return  # 이미 초기화된 경우, 바로 리턴

        self.keywords = None
        self.image_path = []

        ContentData._initialized = True

    def set_keywords(self, keyword):
        self.keywords = keyword

    def combinate_keywords(self):
        address, company = zip(*self.keywords)
        self.keywords = [[x, y] for x in address for y in company]

    def get_address(self, row):
        return self.keywords[row][0]

    def get_company(self, row):
        return self.keywords[row][1]

    def get_keywords_length(self):
        return len(self.keywords)

    def set_image_path(self, path):
        self.image_path.append(path)

    def get_random_image_path(self, num):
        return random.sample(self.image_path, num)


