import re

variables: list[list[str | bool]] = [[]]


def string_to_bool(sring: str) -> bool:
    return sring.strip() == "1"


def get_variable_value(var_name) -> bool | None:
    for item in variables:
        if len(item) == 2 and item[0] == var_name:
            return 1 if item[1] else 0  # type: ignore
    return None


def set_variable(var_name: str, value: bool) -> None:
    for item in variables:
        if len(item) == 2 and item[0] == var_name:
            item[1] = value
            return
    variables.append([var_name, value])


def readln(line: str) -> None:
    variables_to_read = [variable.strip() for variable in line.split(",")]
    print(
        f"Введите значения (0 или 1) для {', '.join(variables_to_read)} через пробел:"
    )
    user_input = input("> ").split()

    for i, variable_name in enumerate(variables_to_read):
        if i < len(user_input) and user_input[i] in ["0", "1"]:
            value = user_input[i]
        else:
            if i < len(user_input):
                print(f"Ошибка: '{user_input[i]}' не является 0 или 1")

            value = ""
            while value not in ["0", "1"]:
                value = input(f"{variable_name} = ").strip()
                if value not in ["0", "1"]:
                    print("Ошибка: введите только 0 или 1")

        set_variable(variable_name, string_to_bool(value))


def writeln(line: str) -> None:
    variables_to_write = [variable.strip() for variable in line.split(",")]
    output_values = []
    for variable_name in variables_to_write:
        value = get_variable_value(variable_name)
        output_values.append(f"{variable_name} = {value}")
    print(", ".join(output_values))


def assign(line: str, line_num: int) -> None:
    target_variable, expression = line.split("=", 1)
    target_variable = target_variable.strip()
    expression = expression.strip()

    if not re.match(r"^[a-zA-Z0-1_\+\*\^\(\)\s]+$", expression):
        print(
            f"Ошибка в строке {line_num}: Недопустимые символы в выражении '{expression}'"
        )
        return
    py_expression = (
        expression.replace("^", " not ").replace("*", " and ").replace("+", " or ")
    )
    try:
        context = {}
        for item in variables:
            if len(item) == 2:
                context[item[0]] = item[1]
        result = eval(py_expression, {"__builtins__": {}}, context)
        set_variable(target_variable, bool(result))
    except Exception as e:
        print(f"Ошибка на {line_num}: Невозможно выполнить выражение. {e}")


def parse_and_execute(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        if line.startswith("#"):
            print(line[2:])
            continue
        if line.startswith("readln"):
            readln(line[6:].strip())
        elif line.startswith("writeln"):
            writeln(line[7:].strip())
        elif "=" in line:
            assign(line, line_num)
        else:
            print(f"Неизвестная команда на строке {line_num}: {line}")


if __name__ == "__main__":
    # filename = input("введите полное имя файла (пример: input.txt): ")
    # filename = "input.txt"
    # parse_and_execute(filename)
    import sys
    if len(sys.argv) < 2:
        print("Использование: python main.py <полное название файла с кодом>")
    else:
        parse_and_execute(sys.argv[1])
