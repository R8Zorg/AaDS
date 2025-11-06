def func() -> list[int]:
    for mask in range(1, 2**n):
        s = 0
        subset = []
        for i in range(n):
            if mask & (1 << i):
                s += weights[i]
                subset.append(i)
        if s == max_weight:
            return subset
    return []


with open("input.txt", "r") as f:
    global max_weight, weights
    max_weight = int(f.readline())
    weights = list(map(int, f.readline().split()))


n = len(weights)
subset = func()
if subset:
    print(subset)
else:
    print("Таких грузов нет")
