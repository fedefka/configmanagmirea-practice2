import argparse
import sys
from pathlib import Path
import yaml
from config import DEFAULT_CONFIG, KEYS, load_config
def main():
    parser = argparse.ArgumentParser(description='Граф зависимостей Alpine')
    parser.add_argument('config', nargs='?', type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args()
    try:
        config = load_config(args.config)
        for key in KEYS:
            value = config[key]
            if isinstance(value, bool):
                value = str(value).lower()
            print(f'{key}: {value}')
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f'Ошибка: {error}', file=sys.stderr)
        return 1
    return 0
if __name__ == '__main__':
    sys.exit(main())
