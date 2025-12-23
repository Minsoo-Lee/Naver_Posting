import random
#
# for x in range(100):
#     i = random.randint(1, 3)
#     print(i)

# for x in range(100):
#     thickness_percent = random.uniform(0.01, 0.05)  # 5% ~ 10% 사이 랜덤
#     print(thickness_percent)

width, height = 100, 140
min_dimension = min(width, height)
thickness_percent = random.randint(1, 5)  # 5% ~ 10% 사이 랜덤
random_thickness = int(min_dimension * (thickness_percent / 100.0))
