import re
from pathlib import Path
from urllib.parse import urlsplit
import yaml
KEYS = ('package', 'repository', 'test_mode', 'filter')
DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / 'config.yaml'
def check_url(value):
    address = urlsplit(value)
    if address.scheme not in ('http', 'https') or not address.hostname:
        raise ValueError('repository: нужен URL http или https')
    if address.username or address.password or re.search(r'\s', value):
        raise ValueError('repository: URL без учётных данных и пробелов')
    if address.fragment or address.query:
        raise ValueError('repository: URL без фрагмента и строки запроса')
    try:
        address.port
    except ValueError as error:
        raise ValueError('repository: неверный порт') from error
def check_fields(config):
    if not isinstance(config, dict) or set(config) != set(KEYS):
        raise ValueError('Ожидаются ключи: ' + ', '.join(KEYS))
    name = config['package']
    if not isinstance(name, str):
        raise ValueError("package: ожидается строка")
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_.+-]*', name):
        raise ValueError('package: недопустимое имя пакета')
    if type(config['test_mode']) is not bool:
        raise ValueError('test_mode: ожидается true или false')
    if not isinstance(config['filter'], str):
        raise ValueError('filter: ожидается строка')
    value = config['repository']
    if not isinstance(value, str) or not value.strip():
        raise ValueError('repository: ожидается URL или путь')
def repository_path(config, folder):
    return folder / Path(config['repository']).expanduser()
def load_config(path):
    config = yaml.safe_load(path.read_text(encoding='utf-8'))
    check_fields(config)
    if config['test_mode']:
        if not re.fullmatch(r'[A-Z]', config['package']):
            raise ValueError('package: в тестовом режиме нужна буква A-Z')
        if not repository_path(config, path.parent).is_file():
            raise ValueError('repository: тестовый файл не найден')
    else:
        check_url(config['repository'])
    return config
