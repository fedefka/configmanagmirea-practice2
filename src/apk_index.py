import gzip
import io
import re
import tarfile
from urllib.request import urlopen
INDEX_NAME = 'APKINDEX.tar.gz'
MAX_DOWNLOAD = 32 * 1024 * 1024
MAX_INDEX = 64 * 1024 * 1024
TIMEOUT = 20
def index_url(repository):
    if repository.endswith('/' + INDEX_NAME):
        return repository
    return repository.rstrip('/') + '/' + INDEX_NAME
def read_index(data):
    with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
        return read_tar(stream)
def read_tar(stream):
    with tarfile.open(fileobj=stream, mode='r|', ignore_zeros=True) as archive:
        for member in archive:
            if member.name not in ('APKINDEX', './APKINDEX'):
                continue
            if not member.isfile() or member.size > MAX_INDEX:
                raise ValueError('Недопустимый файл APKINDEX в архиве')
            with archive.extractfile(member) as stream:
                return stream.read().decode('utf-8')
    raise ValueError('В архиве нет файла APKINDEX')
def parse_index(text):
    packages = {}
    for record in re.split(r'\n\s*\n', text.strip()):
        fields = dict(line.split(':', 1) for line in record.splitlines()
                      if ':' in line)
        name = fields.get('P')
        if not name or not fields.get('V'):
            raise ValueError('Запись APKINDEX без имени или версии пакета')
        if name in packages:
            raise ValueError(f'Повтор пакета в APKINDEX: {name}')
        packages[name] = fields
    return packages
def load_index(repository):
    with urlopen(index_url(repository), timeout=TIMEOUT) as response:
        data = response.read(MAX_DOWNLOAD + 1)
    if len(data) > MAX_DOWNLOAD:
        raise ValueError('Архив APKINDEX слишком большой')
    return parse_index(read_index(data))
def direct_requirements(packages, package):
    if package not in packages:
        raise ValueError(f'Пакет не найден: {package}')
    tokens = packages[package].get('D', '').split()
    return [token for token in tokens if not token.startswith('!')]
