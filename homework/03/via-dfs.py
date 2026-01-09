def dfs(graph, start, end):
    stack = [(start, [start])]
    visited = set()

    while stack:
        node, path = stack.pop()
        if node == end:
            return path
        if node in visited:
            continue
        visited.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    return []


graph = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D", "E"],
    "D": ["B", "C", "E"],
    "E": ["C", "D", "F"],
    "F": ["F"],
}
start_point = "A"
end_point = "F"
print(f"Из {start_point} по дороге: {dfs(graph, start_point, end_point)}")


def dfs_stack(graph, start):
    stack = [start]
    visited = set()

    while stack:
        node = stack.pop()
        if node in visited:
            continue

        visited.add(node)
        print(node)

        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                stack.append(neighbor)


print()
dfs_stack(graph, start_point)
