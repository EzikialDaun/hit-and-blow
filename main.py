import json.decoder
from origin import create_task as ct
from origin import str_list_to_int_list as slti
from origin import is_list_validate as ilv
from origin import check_answer as ca
from origin import json_config as jc


def hit_blow():
    # 경계선 숫자
    board_count = 80
    print("-" * board_count)
    print("Project: Hit & Blow")
    print("Team: 탈3진")
    print("Authors: 금용호, 김민석, 박수민, 임민영")
    print("-" * board_count)
    # 자릿수(d)
    digit = 0
    # 색깔 수(c)
    color = 0
    # 시도 가능 횟수(t)
    try_count = 0
    # 파일 설정 불러오기
    config_path = './config.json'
    try:
        config = jc.get_config(config_path)
    except FileNotFoundError:
        config = {}
    except json.decoder.JSONDecodeError:
        config = {}
    # 파일이 있으면 설정 불러올 것인지 직접 입력할 것인지 선택
    is_direct = False
    if config != {}:
        print("최근 게임 설정")
        print("자릿수: %d" % config["digit"])
        print("색깔의 수: %d" % config["color"])
        print("기회의 수: %d" % config["tryCount"])
        print("-" * board_count)
        answer = input("최근에 진행한 게임의 설정을 불러오시겠습니까? (y/n) ==> ")
        if answer == 'y' or answer == 'Y':
            digit = config["digit"]
            color = config["color"]
            try_count = config["tryCount"]
        else:
            is_direct = True
    else:
        print("게임 설정 파일이 존재하지 않습니다. 새 설정 입력을 진행합니다.")
    # 파일이 없거나 직접 입력 모드이면 직접 입력
    if config == {} or is_direct:
        print("-" * board_count)
        digit = int(input("정답의 자릿수(정수, d)를 입력하세요. (d >= 1) ==> "))
        color = int(input("색깔의 수(정수, c)를 입력하세요. (c >= 1, c >= d) ==> "))
        try_count = int(input("시도 가능한 횟수(정수, t)를 입력하세요. (t >= 1) ==> "))
    # d >= 1
    if digit < 1:
        print("자릿수는 1 이상이어야 합니다.")
        return
    # c >= 1
    if color < 1:
        print("색깔의 수는 1 이상이어야 합니다.")
        return
    # c >= p
    if color < digit:
        print("색깔의 수는 자릿수보다 많아야 합니다.")
        return
    # t >= 1
    if try_count <= 0:
        print("기회의 수는 1 이상이어야 합니다.")
        return
    config_dict = {"digit": digit, "color": color, "tryCount": try_count}
    jc.set_config(config_path, config_dict)
    # 문제 생성
    task = (ct.create_task(color, digit))
    # 성공 여부
    is_success = False
    # 최대 시도 가능 횟수만큼 반복
    # 횟수 안에 정답 맞추면 성공
    # 맞추지 못하면 실패
    for i in range(try_count):
        print("-" * board_count)
        print("남은 기회: %d" % (try_count - i))
        # 플레이어 입력
        answer = input("정수 %d개를 공백(space)으로 분리하여 입력하세요. (0 ~ %d) ==> " % (digit, color - 1))
        # 자릿수가 position과 맞는지 검사
        answer_str_list = answer.split()
        # 문자열 리스트를 숫자 리스트로 변환
        answer_list = slti.str_list_to_int_list(answer_str_list)
        if len(answer_list) == digit:
            # 값의 범위를 검사
            if ilv.is_list_validate(answer_list, 0, color):
                result_dict = ca.check_answer(answer_list, task)
                print("hit: %d, blow: %d" % (result_dict["hit"], result_dict["blow"]))
                if result_dict["hit"] == digit:
                    is_success = True
                    break
                else:
                    is_success = False
            else:
                print("값의 범위가 올바르지 않습니다.")
        else:
            print("숫자의 갯수가 올바르지 않습니다.")
    print("-" * board_count)
    if is_success:
        print("축하드립니다. 정답입니다.")
    else:
        print("아깝네요 ㅠ")
        print("정답은")
        print(task)
        print("입니다.")


hit_blow()
