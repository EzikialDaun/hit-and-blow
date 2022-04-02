import random

# 색깔 수 c(양의 정수)와 위치 수 p(양의 정수)를 입력받아서
# 랜덤하고 고유한(중복이 없는) 숫자(양의 정수) 리스트 리턴
# 각 수의 범위는 0 ~ (c - 1)
# 리스트의 길이는 p
# c >= p
# c >= 1, p >= 1
# ex) c = 6, p = 4       ==>     [0, 2, 3, 5]
def create_task(color, position):
    if color >= position and color >= 1 and position >= 1:
        result = []
        # 리스트의 길이가 위치 수와 같아질 때까지 반복
        while True:
            # 난수 생성
            random_number = random.randrange(0, color)
            # 생성된 수가 리스트에 없으면 추가
            if random_number not in result:
                result.append(random_number)
            # 리스트의 길이가 입력된 위치 수와 같으면 while문 종료
            if len(result) == position:
                break
            else:
                continue
        # 결과 리턴
        return result
    else:
        return []
