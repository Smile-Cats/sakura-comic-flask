import yaml


def get_config(env='PRODUCTION'):
    with open('./config.yaml', 'r', encoding='utf-8') as f:
        configs = yaml.safe_load(f)
    if configs.get(env):
        return configs[env]
    else:
        return configs['COMMON']


if __name__ == '__main__':
    print(get_config())