import random

# 색깔 수 c(양의 정수)와 위치 수 p(양의 정수)를 입력받아서
# 랜덤하고 고유한(중복이 없는) 숫자(양의 정수) 리스트 리턴
# 각 수의 범위는 0 ~ (c - 1)
# 리스트의 길이는 p

# 입력이 상기 조건과 다를 경우 [] 리턴
# ex) c = 6, p = 4      ==>     [0, 2, 3, 5]
# ex) c = 4, p = 6      ==>     []
# ex) c = 0, p = 1      ==>     []
def create_task(color, position):
    result = []
    # 코드 작성
    return result


# 테스트 케이스
print(create_task(6, 4))
print(create_task(5, 3))
print(create_task(4, 6))
print(create_task(0, 1))
print(create_task(11, 10))
