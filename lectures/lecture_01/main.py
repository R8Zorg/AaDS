def f(a):
    s, sp, fl = 0, 0, 0
    i = 0
    while i < len(a):
        if a[i] < 0:
            fl += 1
        if fl % 2 != 0 and a[i] > 0:
            sp += a[i]
        else:
            s += sp
            sp = 0
        i += 1

    if fl == 0:
        print("Нет элементов")
    elif fl == 1:
        print("Найден только один отрицательный элемент")
    else:
        print(f"Сумма положительных чисел между отрицательными: {s}")


l1 = [1, 2, -3, 4, 5, -6, -7, 8, -9, -1, 2]
l2 = [-1, -2, -3, -4]
l3 = [1, 2, 3, 4, 5]
l4 = []
l5 = [1, -2, 3, 4]
list_collection = [l1, l2, l3, l4, l5]

for lst in list_collection:
    f(lst)
