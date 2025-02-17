import math


def first_solution(k: int):
    n = (1 + math.sqrt(1 + 8 * k)) / 2
    if n < 0:
        print("Невозможно рассчитать число программистов.")
        return
    return math.ceil(n)


def second_solution(k: int):
    n = 1
    while n * (n - 1) // 2 < k:
        n += 1
    return n if n * (n - 1) // 2 == k else None


def main():
    handshakes_number = int(input("Введите количество рукопожатий: "))
    if handshakes_number == 0:
        print("Количество программистов может быть 1 либо 0.")
        return
    print(f"Количество программистов: {first_solution(handshakes_number)}")
    print(f"Количество программистов: {second_solution(handshakes_number)}")


if __name__ == "__main__":
    main()
