from typing import Dict, Any


def parse_config(path: str) -> Dict[str, Any]:
    config_list = []
    with open(path) as f:
        for line in f:
            if not line.strip().startswith("#"):
                config_list.append(line)
            else:
                config_list.append("\n")
    return {}
