import os
from origin import create_task
from origin import is_unique
from origin import str_list_to_int_list
from origin import is_list_validate
from origin import check_answer

def hit_blow():
    # 경계선 숫자
    board_count = 80
    print("-" * board_count)
    # 위치 수
    position = int(input("위치의 수(정수, p)를 입력하세요. (p >= 1) ==> "))
    # 색깔 수
    color = int(input("색깔의 수(정수, c)를 입력하세요. (c >= 1, c >= p) ==> "))
    # 문제
    task = (create_task.create_task(color, position))
    if len(task) == 0:
        print("입력한 값이 올바르지 않습니다.")
        return
    # 시도 가능 횟수
    try_count = int(input("시도 가능한 횟수(정수, t)를 입력하세요. (t >= 1) ==> "))
    if try_count <= 0:
        print("입력한 값이 올바르지 않습니다.")
        return
    # 성공 여부
    is_success = False
    # 최대 시도 가능 횟수만큼 반복
    # 횟수 안에 정답 맞추면 성공
    # 맞추지 못하면 실패
    for i in range(0, try_count):
            print("-" * board_count)
            print("남은 기회: %d" % (try_count - i))
            # 플레이어 입력
            answer = input("정수 %d개를 공백으로 분리하여 입력하세요. (0 ~ %d) ==> " % (position, color - 1))
            # 자릿수가 position과 맞는지 검사
            answer_str_list = answer.split()
            # 문자열 리스트를 숫자 리스트로 변환
            answer_list = str_list_to_int_list.str_list_to_int_list(answer_str_list)
            if len(answer_list) == position:
                # 중복이 있는지 검사
                if is_unique.is_unique(answer_list):
                    # 값의 범위를 검사
                    if is_list_validate.is_list_validate(answer_list, 0, color):
                        result_dict = check_answer.check_answer(answer_list, task)
                        print("hit: %d, blow: %d" % (result_dict["hit"], result_dict["blow"]))
                        if result_dict["hit"] == position:
                            is_success = True
                            break
                        else:
                            is_success = False
                    else:
                        print("값의 범위가 올바르지 않습니다.")
                else:
                    print("입력이 중복되었습니다.")
            else:
                print("숫자의 갯수가 올바르지 않습니다.")
    print("-" * board_count)
    if is_success:
        print("성공")
    else:
        print("실패")
        print("정답은")
        print(task)
        print("입니다.")
    
hit_blow()
# 자동 창꺼짐 방지
os.system("pause")
