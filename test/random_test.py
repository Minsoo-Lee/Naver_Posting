import random
#
# for x in range(100):
#     i = random.randint(1, 3)
#     print(i)

# for x in range(100):
#     thickness_percent = random.uniform(0.01, 0.05)  # 5% ~ 10% 사이 랜덤
#     print(thickness_percent)

# width, height = 100, 140
# min_dimension = min(width, height)
# thickness_percent = random.randint(1, 5)  # 5% ~ 10% 사이 랜덤
# random_thickness = int(min_dimension * (thickness_percent / 100.0))

address = "성수동"
company = "설비업체"
place = "신공간 설비업체"

keywords = [address, company, place]

for i in range(10):
    random.shuffle(keywords)
    print(str(keywords))

