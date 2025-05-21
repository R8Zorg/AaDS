import time
from itertools import permutations

# Указания преподавателя:
# В результате выполнения функции должна получиться одна (самая лучшая) комбинация
# создать словарь, где у буквы будет какое-то число. После одной перестановки сложить.
# В следующей перестановке проверить сумму предыдущей и текущей перестановки.
# Остаётся та, чьё значение больше
# Пример:
# abc = 517
# bac = 157
# abc > bac => result = abc
# cab = 751
# abc < cab => result = cab


dict_values = {
    "и": 1,
    "н": 2,
    "с": 3,
    "т": 4,
    "у": 5,
}


def get_perm_value(perm):
    n = len(perm)
    return sum(dict_values[key] * 10 ** (n - i - 1) for i, key in enumerate(perm))


def get_unique_permutations(word, _best_perm="", _best_perm_value=0):
    if len(word) == 1:
        return [word]
    result = []
    used_letters = []
    best_perm = _best_perm
    best_perm_value = _best_perm_value
    for i in range(len(word)):
        current_letter = word[i]
        if current_letter in used_letters:
            continue
        used_letters.append(current_letter)
        remaining_letters = word[:i] + word[i + 1 :]
        for perm in get_unique_permutations(remaining_letters)[0]:
            current_perm = current_letter + perm
            result.append(current_perm)
            current_perm_value = get_perm_value(current_perm)
            if current_perm_value > best_perm_value:
                best_perm_value = current_perm_value
                best_perm = current_perm

    return result, best_perm, best_perm_value


def get_unique_permutations_itertools(word):
    result = ""
    result_value = 0
    for perm in permutations(word):
        new_result = "".join(perm)
        new_result_value = get_perm_value(new_result)
        if new_result_value > result_value:
            result = new_result
            result_value = new_result_value

    return result


word = "институт"

start_time = time.perf_counter()
my_recursion = get_unique_permutations(word)[1]
end_time = time.perf_counter()
total_time1 = end_time - start_time
print(f"Время выполнения первой функции заняло {total_time1}")
print(f"Лучшая перестановка: {my_recursion}")

start_time = time.perf_counter()
itertools_recursion = get_unique_permutations_itertools(word)
end_time = time.perf_counter()
total_time2 = end_time - start_time
print(f"Время выполнения второй функции заняло {total_time2}")
print(f"Лучшая перестановка: {itertools_recursion}")
