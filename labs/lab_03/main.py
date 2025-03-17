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

def print_matrix(m):
    for i in range(len(m)):
        print(m[i])
    print()


print("Матрица А:")
print_matrix(a)

# k, n = input("Input k, n: ").split()
f = [row[:] for row in a]
k = 1  # input
summ = 0
mult = 1
for i in range(1, n // 2):  # 3 chunk
    for j in range(n - i, n):
        if j % 2 != 0 and f[i][j] > k:
            summ += f[i][j]

for i in range(n // 2, n):  # 3 chunk
    for j in range(i + 1, n):
        if j % 2 != 0 and f[i][j] > k:
            summ += f[i][j]

for j in range(n):  # 2 chunk perimeter
    mult *= f[0][j]
for i in range(1, n // 2):
    if i == n - i - 1:
        mult *= f[i][i]
        continue
    mult *= f[i][i]
    mult *= f[i][n - i - 1]

print(f"Sum: {summ}\nMult: {mult}")
if summ > mult:
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
print_matrix(f)
#    1  2 5  4   3
# ((К*A)*F+ K* F^T
f1 = [row[:] for row in a]
for i in range(n):
    for j in range(n):
        f1[i][j] *= k
print("K*A:")
print_matrix(f1)
f2 = [[0] * n for _ in range(n)]

for i in range(n):
    for j in range(n):
        f2[i][j] = sum(f1[i][k] * f[k][j] for k in range(n))
print("(K*A)*F")
print_matrix(f2)

tf = []
for i in range(n):
    row = []
    for j in range(n):
        row.append(f[j][i])
    tf.append(row)
print("F^T:")
print_matrix(tf)

f4 = [row[:] for row in tf]
for i in range(n):
    for j in range(n):
        f4[i][j] *= k
print("K * F^T")
print_matrix(f4)

result = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        result[i][j] = f2[i][j] + f4[i][j]
print("((К*A)*F+ K* F^T:")
print_matrix(result)
