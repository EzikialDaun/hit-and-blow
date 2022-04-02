# 리스트에 중복된 값이 있는지 확인
# data는 리스트 변수
# 중복된 값이 없으면(고유하면) True 리턴
# 중복된 값이 있으면(고유하지 않으면) False 리턴
def is_unique(data):
    if len(data) == len(set(data)):
        return True
    else:
        return False
