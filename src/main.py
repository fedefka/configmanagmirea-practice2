import argparse
import sys
import tarfile
from pathlib import Path
import yaml
from apk_index import load_index
from config import DEFAULT_CONFIG, load_config, repository_path
from graph import build_graph, read_test_graph
from visualize import save_graph, show_graph
from providers import package_neighbors
def get_repository(config, folder):
    name = config['package']
    if config['test_mode']:
        graph = read_test_graph(repository_path(config, folder))
        if name not in graph:
            raise ValueError(f'Пакет не найден: {name}')
        return graph, graph.__getitem__
    packages = load_index(config['repository'])
    if name not in packages:
        raise ValueError(f'Пакет не найден: {name}')
    return packages, package_neighbors(packages)
def main():
    parser = argparse.ArgumentParser(description='Граф зависимостей Alpine')
    parser.add_argument('config', nargs='?', type=Path, default=DEFAULT_CONFIG)
    parser.add_argument('--no-open', action='store_true')
    args = parser.parse_args()
    try:
        config = load_config(args.config)
        _, neighbors = get_repository(config, args.config.parent)
        graph = build_graph(config['package'], neighbors, config['filter'])
        folder = DEFAULT_CONFIG.parent / 'build' / config['package']
        image = save_graph(graph, folder)
        print(f'Mermaid: {folder / "graph.mmd"}')
        print(f'SVG: {image}')
        if not args.no_open:
            show_graph(image)
    except (OSError, ValueError, tarfile.TarError, yaml.YAMLError) as error:
        print(f'Ошибка: {error}', file=sys.stderr)
        return 1
    return 0
if __name__ == '__main__':
    sys.exit(main())
