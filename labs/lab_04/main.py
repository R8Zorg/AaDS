import matplotlib
import numpy as np

matplotlib.use("QtAgg")
import matplotlib.pyplot as plt

n = 5
k = 3
a = np.array(
    [
        [5, 1, 0, 6, 2],
        [1, 1, 0, 2, 2],
        [0, 0, 9, 0, 0],
        [3, 3, 0, 4, 4],
        [3, 7, 0, 8, 4],
    ]
)

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
for j in range(second_half, n):
    c_perimetr += a[0, j]

for j in range(second_half, n):
    c_perimetr += a[mid - 1, j]


for i in range(1, mid - 1):
    c_perimetr += a[i, 0]


for i in range(1, mid - 1):
    c_perimetr += a[i, n - 1]


d_diagonal_mult = 1
j = 0
for i in range(second_half, n):
    d_diagonal_mult *= a[i, j]
    j += 1

print(f"Сумма периметра С: {c_perimetr}")
print(f"Произведение основной диагонали D: {d_diagonal_mult}")
if c_perimetr > d_diagonal_mult:
    print("Периметр С > произведения основной диагонали D. B и C меняются симметрично")
    for i in range(0, mid):
        for j in range(0, mid):
            f[i, j], f[i, n - 1 - j] = f[i, n - 1 - j], f[i, j]
else:
    print(
        "Периметр С < произведения основной диагонали D. B и E меняются несимметрично"
    )
    for i in range(0, mid):
        for j in range(0, mid):
            f[i, j], f[i + n - (n // 2), j + n - (n // 2)] = (
                f[i + n - (n // 2), j + n - (n // 2)],
                f[i, j],
            )
# TODO: определитель матрицы не должен быть равен 0
print_matrix(f, "Матрица F:")
det_a = np.linalg.det(a)
f_sum = 0
for i in range(n):
    f_sum += f[i, i]
    if f[i, i] != f[i, n - 1 - i]:
        f_sum += f[i, n - 1 - i]

result = 0
a_t = a.T
if det_a > f_sum:
    a_inv = np.linalg.inv(a)
    f_inv = np.linalg.inv(f)
    result = a_inv @ a_t - k * f_inv
    print(f"Определитель А > суммы диагоналей F. Вычисление по формуле A^-1 * A^T - K * F^-1: {result}")

else:
    g = np.tril(a)
    f_t = f.T
    result = (a_t + g - f_t) * k
    print(f"Определитель А < суммы диагоналей F. Вычисление по формуле (A^Т + G - F^Т) * K: {result}")

print_matrix(result, "Результат: ")

fig, axs = plt.subplots(1, 2, figsize=(15, 7))

# axs[0].imshow(f, cmap="viridis")

axs[0].imshow(f, cmap="coolwarm")
axs[0].set_title("Матрица F")
fig.colorbar(axs[0].images[0], ax=axs[0])

axs[1].imshow(result, cmap="plasma")
axs[1].set_title("A⁻¹ * Aᵀ - K * F⁻¹")
fig.colorbar(axs[1].images[0], ax=axs[1])

plt.tight_layout()
plt.show()
