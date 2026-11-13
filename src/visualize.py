from collections import defaultdict
from html import escape
from pathlib import Path
from webbrowser import open as open_page
COL_WIDTH = 284
ROW_HEIGHT = 66
NODE_WIDTH = 204
NODE_HEIGHT = 34
MARGIN = 32
def mermaid_text(graph):
    ids = {name: f'n{index}' for index, name in enumerate(graph)}
    lines = ['flowchart LR']
    for name in graph:
        label = escape(name, quote=True).replace('&quot;', '#quot;')
        lines.append(f'    {ids[name]}["{label}"]')
    for name, targets in graph.items():
        for target in targets:
            lines.append(f'    {ids[name]} --> {ids[target]}')
    return '\n'.join(lines) + '\n'
def graph_layout(graph):
    start = next(iter(graph))
    depths = {start: 0}
    columns = defaultdict(list)
    for name, targets in graph.items():
        depth = depths.get(name, 0)
        columns[depth].append(name)
        for target in targets:
            depths.setdefault(target, depth + 1)
    positions = {}
    for depth, names in columns.items():
        for row, name in enumerate(names):
            positions[name] = (MARGIN + depth * COL_WIDTH,
                               MARGIN + row * ROW_HEIGHT)
    width = max(x for x, _ in positions.values()) + NODE_WIDTH + MARGIN
    height = max(y for _, y in positions.values()) + NODE_HEIGHT + MARGIN
    return positions, width, height
def edge_curve(source, target):
    x, y = source
    end_x, end_y = target
    start_x = x + NODE_WIDTH
    start_y = y + NODE_HEIGHT // 2
    target_y = end_y + NODE_HEIGHT // 2
    if start_x < end_x:
        middle = (start_x + end_x) // 2
        return (f'M {start_x} {start_y} C {middle} {start_y} '
                f'{middle} {target_y} {end_x} {target_y}')
    top = min(y, end_y) - MARGIN // 2
    return (f'M {start_x} {start_y} C {start_x + 32} {top} '
            f'{end_x - 32} {top} {end_x} {target_y}')
def svg_edges(graph, positions):
    for name, targets in graph.items():
        for target in targets:
            curve = edge_curve(positions[name], positions[target])
            yield f'<path d="{curve}" marker-end="url(#arrow)"/>'
def svg_nodes(positions):
    for name, (x, y) in positions.items():
        label = escape(name)
        font_size = min(14, 290 // max(1, len(name)))
        yield (f'<rect x="{x}" y="{y}" width="{NODE_WIDTH}" '
               f'height="{NODE_HEIGHT}" rx="6" fill="white" '
               'stroke="#252525"/>')
        yield (f'<text x="{x + NODE_WIDTH // 2}" y="{y + 22}" '
               f'font-size="{font_size}">{label}</text>')
def svg_text(graph):
    positions, width, height = graph_layout(graph)
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<title>Граф зависимостей</title>',
        f'<rect width="{width}" height="{height}" fill="white"/>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" '
        'refX="8" refY="4" orient="auto">',
        '<path d="M 0 0 L 8 4 L 0 8 Z" fill="#606060"/></marker></defs>',
        '<g fill="none" stroke="#606060" stroke-width="1.3">',
        *svg_edges(graph, positions),
        '</g>',
        '<g fill="#171717" font-family="monospace" text-anchor="middle">',
        *svg_nodes(positions),
        '</g></svg>',
    ]
    return '\n'.join(lines) + '\n'
def save_graph(graph, folder):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'graph.mmd').write_text(mermaid_text(graph), encoding='utf-8')
    output = folder / 'graph.svg'
    output.write_text(svg_text(graph), encoding='utf-8')
    return output
def show_graph(path):
    open_page(Path(path).resolve().as_uri())
