import tkinter as tk
from typing import Callable

from config import Colors


class MainMenu(tk.Frame):
    def __init__(self, parent: tk.Tk, start_game_callback: Callable[[], None]) -> None:
        super().__init__(parent, bg=Colors.BG.value)

        self.start_game_callback: Callable[[], None] = start_game_callback

        self._create_widgets()

    def _create_widgets(self) -> None:
        center_frame = tk.Frame(
            self, bg=Colors.MENU_BG.value, relief=tk.RAISED, borderwidth=3
        )
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        title = tk.Label(
            center_frame,
            text="МОРСКОЙ БОЙ",
            font=("Arial", 32, "bold"),
            bg=Colors.MENU_BG.value,
            fg=Colors.BTN_PRIMARY.value,
        )
        title.pack(pady=(30, 10))

        subtitle = tk.Label(
            center_frame,
            text="Игра с ботом",
            font=("Arial", 14, "italic"),
            bg=Colors.MENU_BG.value,
            fg=Colors.FOREGROUND.value,
        )
        subtitle.pack(pady=(0, 30))

        description_frame = tk.Frame(center_frame, bg=Colors.MENU_BG.value)
        description_frame.pack(padx=40, pady=10)

        description_text = tk.Text(
            description_frame,
            height=10,
            width=50,
            wrap=tk.WORD,
            font=("Arial", 11),
            bg=Colors.MENU_BG.value,
            relief=tk.FLAT,
            cursor="arrow",
        )
        description_text.pack()
        description_text.insert(
            "1.0",
            "Добро пожаловать в игру Морской Бой!\n\n"
            "Правила игры:\n"
            "• Расставьте корабли на своём поле\n"
            "• Между кораблями должно быть минимальное пространство в одну клетку\n"
            "• Атакуйте вражеское поле, стараясь потопить все корабли\n"
            "• Выигрывает тот, кто первым потопит все корабли противника\n\n"
            "Состав флота:\n"
            "• 1 линкор (4 клетки)\n"
            "• 2 крейсера (3 клетки)\n"
            "• 3 эсминца (2 клетки)\n"
            "• 4 катера (1 клетка)",
        )
        description_text.config(state=tk.DISABLED)

        btn_start = tk.Button(
            center_frame,
            text="НАЧАТЬ ИГРУ",
            command=self.start_game_callback,
            bg=Colors.BTN_PRIMARY.value,
            fg="white",
            font=("Arial", 16, "bold"),
            cursor="hand2",
            padx=40,
            pady=15,
            relief=tk.RAISED,
            borderwidth=3,
        )
        btn_start.pack(pady=30)
