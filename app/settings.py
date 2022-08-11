import yaml


def get_config(env='PRODUCTION'):
    with open('./config/config.yaml', 'r', encoding='utf-8') as f:
        configs = yaml.safe_load(f)
    if configs.get(env):
        return configs[env]
    else:
        return configs['COMMON']


def get_logging_config():
    with open('./config/logging.yaml', 'r', encoding='utf-8') as f:
        logging_config = yaml.safe_load(f)
    return logging_config


if __name__ == '__main__':
    print(get_logging_config())