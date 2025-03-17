# k, n = input("Input k, n: ").split()
# k = input("Input k: ")


"""
Сохранение чисел под основной диагональю включительно:
Сохраняем все числа. При встрече i == j сохраняем и его, после чего выходим из цикла j, переходя на следующую строку.

Сохранеие чисел над дополнительной диагональю включительно:
Сохраняем все числа. Если i + j == n-1 => break

"""

n = 5

a = [
    [1, 2, 3, 4, 5],
    [1, 1, 3, 4, 5],
    [2, 2, 1, 4, 5],
    [1, 2, 3, 0, 5],
    [1, 2, 3, 4, 0],
]
print("Матрица А:")
for i in range(len(a)):
    print(a[i])


def get_first_chunk() -> list:
    first_chunk = []
    for i in range(n // 2):
        for j in range(i):
            first_chunk.append(a[i][j])

    for i in range(n // 2, n):
        for j in range(n - (i + 1)):
            first_chunk.append(a[i][j])
    return first_chunk


def get_second_chunk() -> list:
    second_chunk = []
    for i in range(n):
        for j in range(i + 1, n - i - 1):
            second_chunk.append(a[i][j])
    return second_chunk


def get_third_chunk() -> list:
    third_chunk = []
    for i in range(1, n // 2):
        for j in range(n - i, n):
            third_chunk.append(a[i][j])

    for i in range(n // 2, n):
        for j in range(i + 1, n):
            third_chunk.append(a[i][j])
    return third_chunk


def get_fourth_chunk() -> list:
    fourth_chunk = []
    for i in range(n // 2 + 1, n):
        for j in range(n - i, i):
            fourth_chunk.append(a[i][j])

    return fourth_chunk


def main():
    f = a
    k = 0  # input
    sum = 0
    mult = 1
    for i in range(1, n // 2):  # 3 chunk
        for j in range(n - i, n):
            if j % 2 != 0 and f[i][j] > k:
                sum += f[i][j]

    for i in range(n // 2, n):  # 3 chunk
        for j in range(i + 1, n):
            if j % 2 != 0 and f[i][j] > k:
                sum += f[i][j]
    
    for j in range(n):
        mult *= f[0][j]
    for i in range(1, n // 2):
        if i == n - i - 1:
            mult *= f[i][i]
            continue
        mult *= f[i][i]
        mult *= f[i][n - i - 1]

    print(f"Sum: {sum}\nMult: {mult}")
    if sum > mult:
        print("sum > mult")
        for i in range(n):
            flag = False
            for j in range(n):
                if i + j == n - 1:
                    break
                if flag:
                    f[i][j], f[j][i] = f[j][i], f[i][j]
                if i == j:
                    flag = True
    else:
        print("sum < mult")
        for i in range(1, n // 2):
            for j in range(n - i, n):
                f[i][j], f[j][j - i + (n - j - 1)] = f[j][j - i + (n - j - 1)], f[i][j]

        for i in range(n // 2, n):
            for j in range(i + 1, n):
                f[i][j], f[j][j - i + (n - j - 1)] = f[j][j - i + (n - j - 1)], f[i][j]

    print("Матрица F:")
    for i in range(n):
        print(f[i])
    # умножение


main()
