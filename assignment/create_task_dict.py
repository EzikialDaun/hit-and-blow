import random


# 최대 숫자 n(양의 정수), 색깔의 최대 갯수 c(양의 정수)와 자릿수 p(양의 정수)를 입력받아서
# 숫자 리스트: 랜덤하고 고유한(중복이 없는) 리스트
# 색 리스트: 랜덤하고 중복이 허용되는 리스트
# 위 두 리스트를 key - value로 묶은 딕셔너리를 리턴하는 함수
# 출력 데이터 구조는 {"c": [0, 2, 3, 2], "n": [12, 0, 4, 5]} (c = 4, n = 13, p = 4의 예시)
# 딕셔너리 키의 이름은 기본적으로 "c"와 "n"이나 인자로 받아서 바뀔 수 있음
# 각 리스트의 길이는 p
# number 리스트 내의 각 수의 범위는 0 ~ (n - 1)
# color 리스트 내의 각 수의 범위는 0 ~ (c - 1)
# n이 p보다 작으면 {} 리턴
# can_duplicate이 True면 중복 값 허용
# ex) n = 13, p = 4, c = 4      ==>     {"c": [0, 1, 3, 1], "n": [11, 3, 12, 5]}(단, 각 자리의 수는 랜덤)
# ex) n = 10, p = 4, c = 1      ==>     {"c": [0, 0, 0, 0], "n": [9, 0, 1, 4]}(단, 각 자리의 수는 랜덤)
# ex) n = 4, p = 5, c = 1       ==>     {}
def create_task_dict(number, position, color, can_duplicate=False, color_key="c", number_key="n"):
    result = {}
    # 코드 작성
    return result


# 테스트
if __name__ == "__main__":
    print(create_task_dict(13, 4, 4))
    print(create_task_dict(13, 4, 4, "color", "number"))
    print(create_task_dict(10, 4, 1))
    print(create_task_dict(4, 5, 1))
    print(create_task_dict(13, 6, 4, "color", "number"))
    print(create_task_dict(10, 4, 1, True))
