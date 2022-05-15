# 유저의 입력 리스트와 제시된 문제 리스트를 입력받아
# hit와 blow 수를 딕셔너리에 담아 리턴
# 두 리스트는 모두 양의 정수를 가지고 중복된 숫자가 없음
# 두 리스트의 각 자리(같은 인덱스)를 비교하는데
# 같은 자리에 같은 숫자가 있으면 hit
# 다른 자리에 같은 숫자가 있으면 blow
# ex) [0, 1, 2, 3], [5, 3, 2, 1]    =>      {'hit': 1, 'blow': 2}
# ex) [0, 5, 1, 4], [5, 3, 2, 1]    =>      {'hit': 0, 'blow': 2}
# ex) [5, 4, 0, 1], [5, 3, 2, 1]    =>      {'hit': 2, 'blow': 0}
# ex) [5, 3, 2, 1], [5, 3, 2, 1]    =>      {'hit': 4, 'blow': 0}
def check_answer(user_data, task):
    result = {"hit": 0, "blow": 0}
    hit = 0
    blow = 0
    for i in range(0, len(task)):
        if task[i] == user_data[i]:
            hit += 1
        elif user_data[i] in task:
            blow += 1
    result.update({"hit": hit})
    result.update({"blow": blow})
    return result


def check_answer_group(user_data, task):
    result = {"hit": 0, "blow": 0, "shot": 0, "strike": 0}
    hit = 0
    blow = 0
    shot = 0
    strike = 0
    for i in range(len(user_data)):
        if user_data[i][0] == task[i][0] and user_data[i][1] == task[i][1]:
            strike += 1
        else:
            number_list = [i[1] for i in task]
            if user_data[i][0] == task[i][0]:
                shot += 1
            if user_data[i][1] == task[i][1]:
                hit += 1
            elif user_data[i][1] in number_list:
                blow += 1
    result.update({"strike": strike})
    result.update({"hit": hit})
    result.update({"blow": blow})
    result.update({"shot": shot})
    return result


def check_answer_dict(user_data, task, color_key="c", number_key="n"):
    result = {"hit": 0, "blow": 0}
    hit = 0
    blow = 0
    for i in range(len(user_data[number_key])):
        if user_data[number_key][i] == task[number_key][i] and user_data[color_key][i] == task[color_key][i]:
            hit += 1
        elif user_data[number_key][i] in task[number_key]:
            blow += 1
    result.update({"hit": hit})
    result.update({"blow": blow})
    return result


if __name__ == "__main__":
    print(check_answer_group([[0, 1], [1, 2], [0, 5], [2, 4]], [[0, 1], [0, 3], [0, 2], [0, 4]]))
    print(check_answer_dict({"c": [0, 1, 0, 2], "n": [1, 2, 5, 4]}, {"c": [0, 0, 0, 0], "n": [1, 3, 2, 4]}))
    print(check_answer_dict({"c": [0, 0, 0, 2], "n": [1, 2, 4, 4]}, {"c": [0, 0, 0, 0], "n": [1, 2, 3, 4]}))
