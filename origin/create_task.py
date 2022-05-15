import random


# 색깔 수 c(양의 정수)와 위치 수 p(양의 정수)를 입력받아서
# 랜덤하고 고유한(중복이 없는) 숫자(양의 정수) 리스트 리턴
# 각 수의 범위는 0 ~ (c - 1)
# 리스트의 길이는 p
# ex) c = 6, p = 4       ==>     [0, 2, 3, 5]
def create_task(color, position):
    result = [i for i in range(0, color)]
    random.shuffle(result)
    result = result[0:position]
    return result


def create_task_group(color, position, group):
    temp = [i for i in range(0, color)]
    random.shuffle(temp)
    temp = temp[0:position]
    result = [[random.randrange(0, group), i] for i in temp]
    return result


def create_task_dict(num, position, color, color_key="c", number_key="n"):
    if position > num:
        return {}
    temp = [i for i in range(0, num)]
    random.shuffle(temp)
    color_list = [random.randrange(0, color) for _ in range(position)]
    number_list = temp[0:position]
    result = {color_key: color_list, number_key: number_list}
    return result


if __name__ == "__main__":
    print(create_task_dict(13, 4, 4))
    print(create_task_dict(13, 4, 4, "c", "n"))
    print(create_task_dict(10, 4, 1))
    print(create_task_dict(4, 5, 1))
    print(create_task_dict(13, 6, 4, "c", "n"))