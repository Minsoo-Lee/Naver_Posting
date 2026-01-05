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

# address = "성수동"
# company = "설비업체"
# place = "신공간 설비업체"
#
# keywords = [address, company, place]
#
# for i in range(10):
#     random.shuffle(keywords)
#     print(str(keywords))

title_types = ["후기형", "문장형", "긴급형", "정보형"]

def get_title_ex(address, company, place, key, index):
    title_type_ex = {
        "정보형": [
            f"{address} 지역에서 {company} 점검이 필요한 주요 상황 정리, {place}",
            f"{company} 공사가 필요한 신호를 {address} 사례로 정리한 {place} 안내",
            f"{address} 현장에서 자주 발생하는 {company} 문제와 해결 방향, {place}",
            f"{company} 작업 전 알아두면 좋은 기준을 {address} 기준으로 정리한 {place}",
            f"{address} 기준으로 살펴본 {company} 점검과 공사 흐름, {place}]"],
        "긴급형": [
            f"갑작스러운 문제 발생 시 {address}에서 필요한 {company} 대응, {place}",
            f"방치하면 커지는 {company} 문제, {address}에서 빠른 대응이 필요한 이유와 {place}",
            f"예상치 못한 고장 상황에서 {address} {company} 조치가 중요한 이유, {place}",
            f"반복되는 증상이라면 {address}에서 즉시 확인해야 할 {company}, {place}",
            f"긴급 조치가 필요한 {company} 상황을 {address} 기준으로 정리한 {place}"
        ],
        "후기형": [
            f"작업 이후 달라진 현장 상태, {address} {company} 진행 후 {place} 정리",
            f"공사 완료 후 확인된 변화, {address} {company} 작업 결과와 {place}",
            f"실제 작업을 마친 뒤 느낀 차이, {address} {company} 경험 정리 {place}",
            f"시공 후 관리가 편해진 이유, {address} {company} 작업과 {place}",
            f"작업 전후 비교로 본 변화, {address} {company} 진행 결과 {place}"
        ],
        "문장형": [
            f"{address}에서 신중한 {company} 진행이 중요한 이유를 설명하는 {place}",
            f"안정적인 환경을 위해 {address}에서 선택되는 {company}, {place}",
            f"오래 쓰기 위해 고려해야 할 {company}, {address} 기준으로 보는 {place}",
            f"환경에 맞는 {company} 선택이 중요한 {address} 현장과 {place}",
            f"관리 부담을 줄이기 위한 {address} {company} 방향을 제시하는 {place}"
        ]
    }

    return title_type_ex[key][index]



for i in range(10):
    key = title_types[random.randint(0, len(title_types) - 1)]
    index = random.randint(0, 4)
    print("key = " + key, "index = " + str(index))
    print(get_title_ex("A", "B", "C", key, index))