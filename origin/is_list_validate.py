# 리스트(양의 정수)와 최솟값(정수), 최댓값(정수)를 입력받아
# 리스트의 모든 값이 최솟값과 최댓값 사이에 속하는지 확인
def is_list_validate(data, min_number, max_number):
    result = list(filter(lambda x: x >= min_number and x < max_number, data))
    if len(data) == len(result):
         return True
    else:
          return False
