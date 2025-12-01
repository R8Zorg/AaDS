from collections import deque


def unreachable_city(graph, start):
    queue = deque([start])
    visited = set()

    while queue:
        city = queue.popleft()

        if city in visited:
            continue
        visited.add(city)

        for neighbor in graph[city]:
            if neighbor not in visited:
                queue.append(neighbor)

    all_cities = set(graph.keys())
    return list(all_cities - visited)


graph = {
    "A": ["B", "C"],
    "B": ["A"],
    "C": ["A", "D"],
    "D": ["C"],
    "E": [],
    "F": ["G"],
    "G": ["F"],
}
print(f"Недоступные города: {unreachable_city(graph, 'A')}")
