from tkinter import StringVar, N, W, E, S, Tk
import tkinter.scrolledtext as st
from tkinter import ttk

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


def get_permutation_data(*args):
    word_value = word.get()
    if not all(letter in dict_values for letter in word_value):
        best_perm.set("Введены недопустипые символы")
        return
    result, best, _ = get_unique_permutations(word_value)
    best_perm.set(f"Лучшая перестановка: {best}")
    permutations.delete(1.0, "end")
    permutations.insert("end", "\n".join(result))


root = Tk()
root.title("Перестановка")


frame = ttk.Frame(root, padding="3 3 12 12")
frame.grid(column=0, row=0, sticky=(N, W, E, S))

word = StringVar()
text_entry = ttk.Entry(frame, width=7, textvariable=word)
text_entry.grid(column=2, row=1, sticky=(W, E))

best_perm = StringVar()
ttk.Label(frame, textvariable=best_perm).grid(column=1, row=2, sticky=(W, E))

ttk.Button(frame, text="Начать", command=get_permutation_data).grid(column=3, row=1)
permutations: st.ScrolledText = st.ScrolledText(frame, width=30, height=10)
permutations.grid(column=1, row=1)
for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

text_entry.focus()
root.bind("<Return>", get_permutation_data)

root.mainloop()
