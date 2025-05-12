import math


def f_rec(n):
    if n == 1 or n == 2:
        return 1
    return (-1) ** n * (f_rec(n - 2) * math.factorial(n) / math.factorial(2 * n))


def f_iter(n):
    if n == 1 or n == 2:
        return 1

    num_2, num_1 = 1, 1  # n - 2, n - 1
    for i in range(3, n + 1):
        sign = (-1) ** i
        numerator = num_2 * math.factorial(i)
        denominator = math.factorial(2 * i)
        current = sign * numerator / denominator
        num_2, num_1 = num_1, current

    return num_1


n = 29  # 29 max
print(f"1: {f_rec(n)}")
print(f"2: {f_iter(n)}")
