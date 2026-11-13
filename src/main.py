import argparse
import sys
import tarfile
from pathlib import Path
import yaml
from apk_index import direct_requirements, load_index
from config import DEFAULT_CONFIG, load_config
def main():
    parser = argparse.ArgumentParser(description='Граф зависимостей Alpine')
    parser.add_argument('config', nargs='?', type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args()
    try:
        config = load_config(args.config)
        if config['test_mode']:
            raise ValueError('Для сбора APK нужен test_mode: false')
        packages = load_index(config['repository'])
        dependencies = direct_requirements(packages, config['package'])
        print(f"Прямые зависимости {config['package']}:")
        print('\n'.join(dependencies) or 'Нет зависимостей')
    except (OSError, ValueError, tarfile.TarError, yaml.YAMLError) as error:
        print(f'Ошибка: {error}', file=sys.stderr)
        return 1
    return 0
if __name__ == '__main__':
    sys.exit(main())
