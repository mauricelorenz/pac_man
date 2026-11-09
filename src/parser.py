import json

from .config import Config


def parse_config(path: str) -> Config:
    config_list = []
    with open(path) as f:
        for line in f:
            if not line.strip().startswith("#"):
                config_list.append(line)
            else:
                config_list.append("\n")
    config_dict = json.loads("".join(config_list))
    config = Config(**config_dict)
    return config
