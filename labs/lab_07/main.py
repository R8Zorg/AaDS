import tkinter.scrolledtext as st
from tkinter import StringVar, Tk, ttk

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
    if not all(letter in dict_values for letter in word_value) or word_value == "":
        lb_best_perm_value.configure(foreground="Red")
        best_perm.set("Введены недопустипые символы")
        st_permutations.delete(1.0, "end")
        return
    result, best, _ = get_unique_permutations(word_value)
    lb_best_perm_value.configure(foreground="Green")
    best_perm.set(best)
    st_permutations.delete(1.0, "end")
    st_permutations.insert("end", "\n".join(result))


root = Tk()
root.title("Перестановка")


word = StringVar()
best_perm = StringVar(value="Нет")

root.geometry("252x359")
root.resizable(False, False)
lb_input_value = ttk.Label(text="Введите последовательность:", anchor="center")
lb_input_value.place(relx=0.04, rely=0.028, height=30, width=234)

lb_all_combinations = ttk.Label(text="Все последовательности:", anchor="center")
lb_all_combinations.place(relx=0.04, rely=0.279, height=30, width=236)

entry_input_value = ttk.Entry(textvariable=word)
entry_input_value.place(relx=0.04, rely=0.139, height=25, relwidth=0.54)
entry_input_value.focus()
root.bind("<Return>", get_permutation_data)

btn_compute = ttk.Button(text="Вычислить", command=get_permutation_data)
btn_compute.place(relx=0.591, rely=0.125, height=33, width=81)

st_permutations = st.ScrolledText()
st_permutations.place(relx=0.04, rely=0.362, relheight=0.418, relwidth=0.937)

lb_best_perm = ttk.Label(text="Лучшая перестановка:", anchor="center")
lb_best_perm.place(relx=0.04, rely=0.808, height=33, width=236)
lb_best_perm_value = ttk.Label(textvariable=best_perm, anchor="center")
lb_best_perm_value.place(relx=0.04, rely=0.891, height=22, width=236)

root.mainloop()
