# 유저의 입력 딕셔너리와 제시된 문제 딕셔너리를 입력받아
# hit와 blow 수를 딕셔너리에 담아 리턴
# 입력 데이터 구조는 {"c": [0, 2, 3, 2], "n": [12, 0, 4, 5]}, 하단 테스트 케이스 참고
# hit: 두 딕셔너리의 c 리스트의 각 자리가 일치하고, 두 딕셔너리의 n 리스트의 각 자리가 일치하면 증가 (자리, 숫자, 색깔 일치)
# blow: task 딕셔너리의 n 리스트에 user_data 딕셔너리의 n 리스트의 해당 숫자가 존재할 경우 증가 (기존 blow와 같음, 숫자만 일치)
# 딕셔너리 키의 이름은 기본적으로 "c"와 "n"이나 인자로 받아서 바뀔 수 있음
# 이때, user_data 리스트의 값은 중복될 수 있음
def check_answer(user_data, task, color_key="c", number_key="n"):
    # 초기값 설정은 자유
    result = {"hit": 0, "blow": 0}
    # 코드 작성
    return result


# 테스트
if __name__ == "__main__":
    # 아래의 출력은 {'hit': 1, 'blow': 2}가 되어야 함
    print(check_answer({"c": [0, 1, 0, 2], "n": [1, 2, 5, 4]}, {"c": [0, 0, 0, 0], "n": [1, 3, 2, 4]}))
    # 아래의 출력은 {'hit': 2, 'blow': 2}가 되어야 함
    print(check_answer({"c": [0, 0, 0, 2], "n": [1, 2, 4, 4]}, {"c": [0, 0, 0, 0], "n": [1, 2, 3, 4]}))
