import time
from itertools import permutations


def get_unique_permutations(word):
    if len(word) == 1:
        return [word]
    result = []
    used_letters = []
    for i in range(len(word)):
        current_letter = word[i]
        if current_letter in used_letters:
            continue
        used_letters.append(current_letter)
        remaining_letters = word[:i] + word[i + 1:]
        for perm in get_unique_permutations(remaining_letters):
            result.append(current_letter + perm)
    return result


def get_unique_permutations_itertools(word):
    result = []
    for perm in permutations(word):
        result.append("".join(perm))
    return result


word = "институт"

start_time = time.perf_counter()
my_recursion = get_unique_permutations(word)
end_time = time.perf_counter()
total_time1 = end_time - start_time
print(f"Время выполнения первой функции заняло {total_time1}")


start_time = time.perf_counter()
itertools_recursion = get_unique_permutations_itertools(word)
end_time = time.perf_counter()
total_time2 = end_time - start_time
print(f"Время выполнения второй функции заняло {total_time2}")
