import json


def get_config(config_path):
    with open(config_path, 'r') as f:
        json_data = json.load(f)
    digit = json_data['latestConfig']['digit']
    color = json_data['latestConfig']['color']
    try_count = json_data['latestConfig']['tryCount']
    result = {'digit': digit, 'color': color, 'tryCount': try_count}
    return result


def set_config(config_path, config):
    json_data = {'latestConfig': {}}
    json_data['latestConfig']['digit'] = config['digit']
    json_data['latestConfig']['color'] = config['color']
    json_data['latestConfig']['tryCount'] = config['tryCount']
    with open(config_path, 'w') as f:
        json.dump(json_data, f, indent="\t")


# 파일 경로(문자열)와 타겟 딕셔너리(딕셔너리)를 입력하면
# 해당 json파일에 딕셔너리를 업데이트
def set_config_rev(config_path: str, target_obj: dict[str, any]):
    json_data = get_config_rev(config_path)
    json_data.update(target_obj)
    with open(config_path, 'w') as f:
        json.dump(json_data, f, indent="\t")


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
