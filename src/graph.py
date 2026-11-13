import re
from collections import deque
LETTER = re.compile(r'[A-Z]')
RECURSION_BATCH = 64
def read_test_graph(path):
    graph = {}
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(),
                                  start=1):
        if not line.strip():
            continue
        name, separator, targets = line.strip().partition(':')
        targets = targets.split()
        valid = all(LETTER.fullmatch(x) for x in [name] + targets)
        if not separator or not valid:
            raise ValueError(f'Строка {number}: ожидается запись A: B C')
        if name in graph:
            raise ValueError(f'Повтор пакета {name} в строке {number}')
        graph[name] = targets
    if not graph:
        raise ValueError('Тестовый репозиторий пуст')
    for targets in list(graph.values()):
        for name in targets:
            graph.setdefault(name, [])
    return graph
def bfs_batch(queue, seen, graph, neighbors, excluded):
    if not queue:
        return
    for _ in range(len(queue)):
        name = queue.popleft()
        for target in dict.fromkeys(neighbors(name)):
            if excluded and excluded in target:
                continue
            graph[name].append(target)
            if target not in seen:
                seen.add(target)
                graph[target] = []
                queue.append(target)
def bfs_level(levels, queue, seen, graph, neighbors, excluded):
    if not queue or not levels:
        return
    bfs_batch(queue, seen, graph, neighbors, excluded)
    bfs_level(levels - 1, queue, seen, graph, neighbors, excluded)
def build_graph(start, neighbors, excluded=''):
    if excluded and excluded in start:
        raise ValueError(f'Начальный пакет {start} исключён фильтром')
    graph = {start: []}
    queue = deque([start])
    seen = {start}
    while queue:
        bfs_level(RECURSION_BATCH, queue, seen, graph, neighbors, excluded)
    return graph
def print_graph(graph):
    for name, targets in graph.items():
        print(f'{name}: {" ".join(targets) or "-"}')
