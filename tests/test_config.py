import sys
import tempfile
import unittest
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from config import load_config
class ConfigTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = Path(folder.name) / 'config.yaml'
        self.values = dict(package='nano', repository='https://host/repo',
                           test_mode=False, filter='')
    def load(self):
        self.path.write_text(yaml.safe_dump(self.values), encoding='utf-8')
        return load_config(self.path)
    def test_valid_url(self):
        self.assertEqual(self.load(), self.values)
    def test_each_invalid_field(self):
        for key, value in [('package', 'a b'), ('repository', 'ftp://host'),
                           ('test_mode', 'true'), ('filter', 5)]:
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, key):
                self.values[key], saved = value, self.values[key]
                try:
                    self.load()
                finally:
                    self.values[key] = saved
    def test_test_file_relative_to_config(self):
        self.values.update(package='A', repository='graph.txt', test_mode=True)
        with self.assertRaisesRegex(ValueError, 'repository'):
            self.load()
        self.path.with_name('graph.txt').write_text('A:', encoding='utf-8')
        self.assertEqual(self.load(), self.values)
    def test_wrong_document(self):
        for value in [None, ['nano'], {'package': 'nano'}]:
            self.values = value
            with self.assertRaises(ValueError):
                self.load()
