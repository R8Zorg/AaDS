import tkinter as tk
from functools import partial


class ColorButtons:
    def __init__(self, root: tk.Tk, colors: list[str], command: callable):
        self.buttons = []
        for i, color in enumerate(colors):
            btn = tk.Button(
                root,
                background=color,
                activebackground=color,
                width=10,
                command=partial(command, color),
            )
            btn.place(
                relx=0.797 + 0.068 * (i % 2),
                rely=0.084 + 0.041 * (i // 2),
                height=33,
                width=71,
            )
            self.buttons.append(btn)
