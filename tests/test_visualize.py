import sys
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as element_tree
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from visualize import save_graph
class VisualizeTests(unittest.TestCase):
    def test_cyclic_graph_outputs(self):
        graph = {'A': ['B', 'A'], 'B': ['A']}
        with tempfile.TemporaryDirectory() as location:
            folder = Path(location)
            path = save_graph(graph, folder)
            mermaid = (folder / 'graph.mmd').read_text(encoding='utf-8')
            self.assertIn('n0 --> n1', mermaid)
            self.assertIn('n1 --> n0', mermaid)
            self.assertIn('n0 --> n0', mermaid)
            svg = element_tree.parse(path).getroot()
            ns = {'s': 'http://www.w3.org/2000/svg'}
            self.assertEqual(svg.findall('.//s:text', ns)[0].text, 'A')
            self.assertEqual(len(svg.findall('.//s:g/s:path', ns)), 3)
