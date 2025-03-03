import re

digit_dict = {
    0: "ноль",
    1: "один",
    2: "два",
    3: "три",
    4: "четыре",
    5: "пять",
    6: "шесть",
    7: "семь",
    8: "восемь",
    9: "девять",
}


with open("input.txt", "r") as file:
    file_data = file.read()
    numbers = re.findall(r"\b(77|[0-7]77|[0-3][0-7]77)\b", file_data)
    for number in numbers:
        words = []
        for letter in number:
            words.append(digit_dict[int(letter)])
        print(f"{number} ({' '.join(words)})")
