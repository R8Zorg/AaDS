
n = 5

a = [
    [5, 1, 0, 6, 2],
    [1, 1, 0, 2, 2],
    [0, 0, 0, 0, 0],
    [3, 3, 0, 4, 4],
    [3, 7, 0, 8, 4],
]

f = a.copy()

def print_matrix(m, text):
    print(text)
    for i in range(len(m)):
        print(m[i])
    print()

print_matrix(a, "Матрица A:")
mid = n // 2
second_half = mid + 1 if n % 2 != 0 else mid

c_perimetr = 0
for j in range (second_half, n):
    c_perimetr += a[0][j]

for j in range (second_half, n):
    c_perimetr += a[mid - 1][j]


for i in range (1, mid - 1):
    c_perimetr += a[i][0]


for i in range (1, mid - 1):
    c_perimetr += a[i][n - 1]


d_diagonal_mult = 1
j = 0
for i in range(second_half, n):
    d_diagonal_mult *= a[i][j]
    j += 1

print(f"Сумма периметра С: {c_perimetr}")
print(f"Произведение основной диагонали D: {d_diagonal_mult}")
if c_perimetr > d_diagonal_mult:
    print("Периметр С > произведения основной диагонали D. B и C меняются симметрично")
    for i in range(0, mid):
        for j in range(0, mid):
            f[i][j], f[i][n - 1 - j] = f[i][n - 1 - j], f[i][j]
else:
    print("Периметр С < произведения основной диагонали D. B и E меняются несимметрично")
    for i in range(0, mid):
        for j in range(0, mid):
            f[i][j], f[i + n - (n // 2)][j + n - (n // 2)] = f[i + n - (n // 2)][j + n - (n // 2)], f[i][j]

print_matrix(f, "Матрица F:")

