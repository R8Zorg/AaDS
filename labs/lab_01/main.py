import random

FILENAME = "input.txt"
NUMBERS_COUNT = 500
NUMBERS_IN_ROW = 10
MAX_DEC_NUMBER = 2047

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
    9: "девять"
}


def generate_file(filename):
    with open(filename, "w") as file:
        for dozen in range(int(NUMBERS_COUNT / NUMBERS_IN_ROW)):
            for position_in_row in range(NUMBERS_IN_ROW):
                oct_number = oct(random.randint(0, 5000))[2:]
                file.write(oct_number + " ")
            file.write("\n")


def is_oct(number: str):
    return number.isdigit() and all(c in "01234567" for c in number)


def is_valid_number(number: str) -> bool:
    if not is_oct(number):
        return False
    if int(number) % 100 != 77:
        return False
    if int(number, 8) > MAX_DEC_NUMBER:
        return False
    return True


def get_oct_number_by_rule(filename):
    oct_numbers = []
    with open(filename, 'r') as file:
        for line in file:
            row = line.split()
            for value in row:
                if is_valid_number(value):
                    oct_numbers.append(int(value))

    return oct_numbers


def print_numbers_in_words(numbers):
    for number in numbers:
        words = []
        for letter in str(number):
            words.append(digit_dict[int(letter)])
        print(f"{number} ({' '.join(words)})")


def main():
    if not os.path.isfile(FILENAME):
        generate_file(FILENAME)
        print(f"{FILENAME} файл не был найден, поэтому он сгенерировался автоматически.")
    numbers = get_oct_number_by_rule(FILENAME)
    print_numbers_in_words(numbers)


if __name__ == "__main__":
    main()
