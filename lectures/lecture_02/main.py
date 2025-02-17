a = [1, 2, 3, -4, 0, -5, 0, 6, 0, 0, -1, 0]
i, f, c = 0, 0, 0
while i < len(a) - 1:
    if a[i] == 0:
        f = 1
    if f == 1 and a[i] < 0 and a[i + 1] == 0:
        c += 1
        f = 0
    i += 1

print(c)
