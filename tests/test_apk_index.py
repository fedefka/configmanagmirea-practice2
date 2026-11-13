import io
import sys
import tarfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from apk_index import direct_requirements, index_url, parse_index, read_index
class ApkIndexTests(unittest.TestCase):
    def test_archive_and_direct_dependencies(self):
        data = (b'P:demo\nV:1-r0\n'
                b'D:musl>=1 so:demo.so.1 !broken\n\nP:musl\nV:1\n')
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode='w:gz') as archive:
            member = tarfile.TarInfo('APKINDEX')
            member.size = len(data)
            archive.addfile(member, io.BytesIO(data))
        index = parse_index(read_index(buffer.getvalue()))
        self.assertEqual(direct_requirements(index, 'demo'),
                         ['musl>=1', 'so:demo.so.1'])
        self.assertEqual(direct_requirements(index, 'musl'), [])
        with self.assertRaisesRegex(ValueError, 'Пакет не найден'):
            direct_requirements(index, 'absent')
    def test_invalid_index(self):
        with self.assertRaises(ValueError):
            parse_index('P:demo')
    def test_index_url(self):
        url = 'https://host/main/aarch64/APKINDEX.tar.gz'
        self.assertEqual(index_url('https://host/main/aarch64/'), url)
        self.assertEqual(index_url(url), url)
