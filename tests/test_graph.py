import sys
import unittest
from pathlib import Path
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'src'))
from graph import build_graph, read_test_graph, reverse_edges
from providers import package_neighbors
CHAIN_END = 1500
class GraphTests(unittest.TestCase):
    def test_bfs_order_and_cycle(self):
        graph = read_test_graph(root / 'examples/graph.txt')
        result = build_graph('A', graph.__getitem__)
        self.assertEqual(list(result), ['A', 'B', 'C', 'D'])
        self.assertEqual(result['D'], ['A'])
        self.assertEqual(result['C'], ['D'])
    def test_filter_removed_node_and_path(self):
        graph = {'A': ['B'], 'B': ['C'], 'C': []}
        self.assertEqual(build_graph('A', graph.__getitem__, 'B'), {'A': []})
        with self.assertRaises(ValueError):
            build_graph('A', graph.__getitem__, 'A')
    def test_long_chain(self):
        def neighbors(name):
            return [name + 1] if name < CHAIN_END else []
        self.assertEqual(len(build_graph(0, neighbors)), CHAIN_END + 1)
    def test_virtual_providers_versions_and_missing(self):
        packages = {
            'root': {'V': '1', 'D': 'so:lib>=2 absent !conflict'},
            'old': {'V': '9', 'p': 'so:lib=1'},
            'new': {'V': '1', 'p': 'so:lib=2'},
            'other': {'V': '1', 'p': 'so:lib=3'},
        }
        result = build_graph('root', package_neighbors(packages))
        self.assertEqual(result['root'], ['new', 'other', 'absent'])
        self.assertEqual(result['absent'], [])
    def test_reverse_dependencies(self):
        graph = read_test_graph(root / 'examples/graph.txt')
        reverse = reverse_edges(graph, graph.__getitem__)
        result = build_graph('D', reverse.__getitem__)
        self.assertEqual(list(result), ['D', 'B', 'C', 'A', 'E'])
        self.assertEqual(result['A'], ['D'])
        self.assertEqual(build_graph('F', reverse.__getitem__), {'F': []})
        result = build_graph('D', reverse.__getitem__, 'C')
        self.assertEqual(list(result), ['D', 'B', 'A'])
