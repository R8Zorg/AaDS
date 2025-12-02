from collections import deque


def unreachable_matrix(graph, names, start_name):
    start = names.index(start_name)

    visited = set()
    queue = deque([start])

    while queue:
        node_i = queue.popleft()
        if node_i in visited:
            continue
        visited.add(node_i)

        for neighbor_j, is_available in enumerate(graph[node_i]):
            if is_available and neighbor_j not in visited:
                queue.append(neighbor_j)

    result = [names[i] for i in range(len(names)) if i not in visited]
    return result


graph = [
    [0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 1, 0, 1],
    [0, 0, 1, 1, 0],
]

names = ["A", "B", "C", "D", "E"]
start_point = "A"
print(
    f"Недоступные города из {start_point}: {unreachable_matrix(graph, names, start_point)}"
)
