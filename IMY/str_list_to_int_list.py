# 문자열 형태의 정수의 리스트에서 모든 항목을 입력받아
# 정수의 항목으로 이루어진 리스트로 리턴
# ex) ["1", "2", "5", "4"]         ==>      [1, 2, 5, 4]
# ex) ["2", "1", "0", "3"]         ==>      [2, 1, 0, 3]
def str_list_to_int_list(data):
    result = []
    # 코드 작성
    for i in data:
        result.append(int(i))
    return result


# 테스트
if __name__ == "__main__":
    print(str_list_to_int_list(["1", "2", "5", "4"]))
    print(str_list_to_int_list(["2", "1", "0", "3"]))
    print(str_list_to_int_list(["7", "9", "3", "4", "6"]))
