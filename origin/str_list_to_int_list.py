# 문자열 형태의 정수의 리스트에서 모든 항목을 입력받아
# 정수의 항목으로 이루어진 리스트로 리턴
# ex) ["1", "2", "5", "4"]         ==>      [1, 2, 5, 4]
# ex) ["2", "1", "0", "3"]         ==>      [2, 1, 0, 3]
def str_list_to_int_list(data):
    result = []
    for i in range(0, len(data)):
        result.append(int(data[i]))
    return result
