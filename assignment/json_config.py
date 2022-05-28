import json


# JSON이란? https://developer.mozilla.org/ko/docs/Learn/JavaScript/Objects/JSON
# 파이썬에서 JSON 다루기 https://www.daleseo.com/python-json/

# 파일 경로(문자열)와 타겟 딕셔너리(딕셔너리)를 입력하면
# 해당 json파일에 딕셔너리를 업데이트
def set_config_rev(config_path: str, target_obj: dict[str, any]):
    # 기존 파일 설정 가져와서
    json_data = get_config_rev(config_path)
    # 업데이트하는 코드 작성


# 파일 경로(문자열)을 입력하면
# 해당 json 파일을 읽어 딕셔너리로 리턴
def get_config_rev(config_path: str) -> dict[str, any]:
    result = {}
    return result


if __name__ == "__main__":
    path = "./config.json"
    current_config = {"playlist": ["IU - strawberry moon"]}
    set_config_rev(path, current_config)
    print(get_config_rev(path))
    new_config = {"playlist": ["IU - strawberry moon", "Sam Ryder - Tiny Riot"], "isShuffle": False}
    set_config_rev(path, new_config)
    print(get_config_rev(path))
