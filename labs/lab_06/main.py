import math
import time


def f_rec(n):
    if n == 1 or n == 2:
        return 1
    if n % 2 == 0:
        sign = 1
    else:
        sign = -1
    return sign * (f_rec(n - 2) * math.factorial(n) / math.factorial(2 * n))


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


def func_measure_time(func, n):
    start_time = time.perf_counter()
    result = func(n)
    end_time = time.perf_counter()
    return end_time - start_time, result


def comparing():
    print("n\tВремя рекурсивного алгоритма\tВремя итерационного алгоритма")
    print("---------------------------------------------------------------------")

    rec_time, rec_value = 0, 0
    iter_time, iter_value = 0, 0
    try:
        rec_time, rec_value = func_measure_time(f_rec, n)

    except RecursionError:
        print(f"{n}\tГлубина рекурсии превышена\t{iter_time * 1000:.6f}")

    except Exception as e:
        print(f"{n}\tОшибка: {str(e)}")

    try:
        iter_time, iter_value = func_measure_time(f_iter, n)

    except Exception as e:
        print(f"{n}\tОшибка: {str(e)}")

    print(f"{n}\t{rec_time * 1000:.6f}\t\t\t{iter_time * 1000:.6f}")


def detemenite_borders():
    print("\nОпределение границ применимости алгоритмов:")

    big_num = 1000
    max_rec_n = 0
    for n in range(1, big_num):
        try:
            f_rec(n)
            max_rec_n = n
        except Exception:
            print(f"Рекурсивный алгоритм: максимальное n = {max_rec_n}")
            break

    max_it_n = 0
    for n in range(1, big_num):
        try:
            f_iter(n)
            max_it_n = n
        except Exception:
            print(f"Итеративный алгоритм: алгоритм: максимальное n = {max_it_n}")
            break


n = int(input("Введите n: "))
comparing()
detemenite_borders()
