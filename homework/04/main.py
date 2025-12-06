def check_brackets_pair_recursive(text: str):
    if "(" not in text and ")" not in text:
        return True

    close = text.find(")")
    open = text.rfind("(", 0, close)
    if open == -1 or close == -1:
        return False
    new_text = text[:open] + text[open + 1 : close] + text[close + 1 :]
    return check_brackets_pair_recursive(new_text)


def check_brackets_pair_stack(text: str):
    stack = []
    for i in range(len(text)):
        if text[i] == "(":
            stack.append(text[i])
        elif text[i] == ")":
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0


print(check_brackets_pair_recursive("()"))
print(check_brackets_pair_recursive(")("))
print(check_brackets_pair_recursive("()(())"))
print(check_brackets_pair_recursive("((("))

print()
print(check_brackets_pair_stack("()"))
print(check_brackets_pair_stack(")("))
print(check_brackets_pair_stack("()(())"))
print(check_brackets_pair_stack("((("))
