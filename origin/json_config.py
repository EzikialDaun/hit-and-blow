import json


def get_config(config_path):
    with open(config_path, 'r') as f:
        json_data = json.load(f)
    digit = json_data['latestConfig']['digit']
    color = json_data['latestConfig']['color']
    try_count = json_data['latestConfig']['tryCount']
    result = {'digit': digit, 'color': color, 'tryCount': try_count}
    f.close()
    return result


def set_config(config_path, config):
    json_data = {'latestConfig': {}}
    json_data['latestConfig']['digit'] = config['digit']
    json_data['latestConfig']['color'] = config['color']
    json_data['latestConfig']['tryCount'] = config['tryCount']
    with open(config_path, 'w') as f:
        json.dump(json_data, f, indent="\t")
    f.close()


def set_config_with_prop(config_path, prop, target):
    json_data = {prop: target}
    with open(config_path, 'w') as f:
        json.dump(json_data, f, indent="\t")
    f.close()


def get_config_with_prop(config_path, prop):
    with open(config_path, 'r') as f:
        json_data = json.load(f)
    result = json_data[prop]
    f.close()
    return result


playlist_prop_name = 'latestPlaylist'


def set_playlist_config(config_path, playlist):
    set_config_with_prop(config_path, playlist_prop_name, playlist)


def get_playlist_config(config_path):
    result = get_config_with_prop(config_path, playlist_prop_name)
    return result
