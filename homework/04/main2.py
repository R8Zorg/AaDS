def greed_algorithm(items: list[list[int, int]], max_w):
    sorted_items = sorted(items, key=lambda i: i[0], reverse=True)
    current_weight = 0
    backpack = []
    for i in range(len(sorted_items)):
        weight = sorted_items[i][1]
        if current_weight + weight <= max_w:
            backpack.append(sorted_items[i])
            current_weight += weight
        if current_weight == max_w:
            break
    return backpack


items = [  # price, weight
    [17, 5],
    [2, 1],
    [35, 15],
    [10, 7],
]
max_w = 16

print(greed_algorithm(items, max_w))
