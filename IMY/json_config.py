import json


# JSON이란? https://developer.mozilla.org/ko/docs/Learn/JavaScript/Objects/JSON
# 파이썬에서 JSON 다루기 https://www.daleseo.com/python-json/

# 파일 경로(문자열)와 타겟 딕셔너리(딕셔너리)를 입력하면
# 해당 json파일에 딕셔너리를 업데이트
def set_config_rev(config_path: str, target_obj: dict[str, any]):
    # 기존 파일 설정 가져와서
    json_data = get_config_rev(config_path)
    # 업데이트하는 코드 작성
    json_data.update(target_obj)
    f = open(config_path, 'w')
    json.dump(json_data, f, indent=2)
    f.close()


# 파일 경로(문자열)을 입력하면
# 해당 json 파일을 읽어 딕셔너리로 리턴
def get_config_rev(config_path: str) -> dict[str, any]:
    # 파일 열기 시도
    try:
        with open(config_path, 'r') as f:
            result = json.load(f)
    # 파일이 없으면 빈 딕셔너리 리턴
    except FileNotFoundError:
        result = {}
    # json 오류 발생 시 빈 딕셔너리 리턴
    except json.decoder.JSONDecodeError:
        result = {}
    # 결과 리턴
    return result


if __name__ == "__main__":
    path = "./config.json"
    current_config = {"playlist": ["IU - strawberry moon"]}
    set_config_rev(path, current_config)
    print(get_config_rev(path))
    new_config = {"playlist": ["IU - strawberry moon", "Sam Ryder - Tiny Riot"], "isShuffle": False}
    set_config_rev(path, new_config)
    print(get_config_rev(path))
