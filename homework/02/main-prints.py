with open("input.txt", "r") as f:
    global max_weight, weights
    max_weight = int(f.readline())
    weights = list(map(int, f.readline().split()))


n = len(weights)
for mask in range(1, 1 << len(weights)):  # от 1 до 2^n - 1
    print(f"{mask=} (bin: {mask:0{n}b})")
    print()
    s = 0
    subset = []
    for i in range(len(weights)):
        print(f"1 << {i}: {(1 << i):0{n}b}")
        print(f"{mask:0{n}b}\n{(1 << i):0{n}b}")
        print(f"&: [{mask & (1 << i)}] (bin: {(mask & (1 << i)):0{n}b})")
        if mask & (1 << i):
            s += weights[i]
            subset.append(weights[i])
        print()
    print(f"s ({s}) == max_weight ({max_weight}): {s == max_weight}")
    print()
    if s == max_weight:
        print(subset)
