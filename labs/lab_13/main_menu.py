"""
Класс MainMenu - главное меню игры
"""

import tkinter as tk
from typing import Callable

from config import Colors

class MainMenu(tk.Frame):
    def __init__(self, parent: tk.Widget, start_game_callback: Callable[[], None]) -> None:
        """
        Инициализация главного меню
        
        Args:
            parent: родительский виджет
            start_game_callback: функция обратного вызова для начала игры
        """
        super().__init__(parent, bg=Colors.BG.value)
        
        self.start_game_callback: Callable[[], None] = start_game_callback
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Создаёт виджеты меню"""
        # Контейнер по центру
        center_frame = tk.Frame(self, bg=Colors.MENU_BG.value, relief=tk.RAISED, borderwidth=3)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Заголовок
        title = tk.Label(center_frame, text="МОРСКОЙ БОЙ", 
                        font=("Arial", 32, "bold"), bg=Colors.MENU_BG.value, 
                        fg=Colors.BTN_PRIMARY.value)
        title.pack(pady=(30, 10))
        
        subtitle = tk.Label(center_frame, text="Battleship Game", 
                           font=("Arial", 14, "italic"), bg=Colors.MENU_BG.value, 
                           fg="#666666")
        subtitle.pack(pady=(0, 30))
        
        # Описание
        description_frame = tk.Frame(center_frame, bg=Colors.MENU_BG.value)
        description_frame.pack(padx=40, pady=10)
        
        description_text = tk.Text(description_frame, height=10, width=50, 
                                  wrap=tk.WORD, font=("Arial", 11), 
                                  bg=Colors.MENU_BG.value, relief=tk.FLAT, 
                                  cursor="arrow")
        description_text.pack()
        description_text.insert("1.0", 
            "Добро пожаловать в игру Морской Бой!\n\n"
            "Правила игры:\n"
            "• Расставьте корабли на своём поле\n"
            "• Атакуйте вражеское поле, пытаясь потопить все корабли\n"
            "• Выигрывает тот, кто первым потопит все корабли противника\n\n"
            "Состав флота:\n"
            "• 1 линкор (4 клетки)\n"
            "• 2 крейсера (3 клетки)\n"
            "• 3 эсминца (2 клетки)\n"
            "• 4 катера (1 клетка)"
        )
        description_text.config(state=tk.DISABLED)
        
        # Кнопка начала игры
        btn_start = tk.Button(center_frame, text="НАЧАТЬ ИГРУ", 
                             command=self._on_start_click,
                             bg=Colors.BTN_PRIMARY.value, fg="white", 
                             font=("Arial", 16, "bold"), 
                             cursor="hand2", padx=40, pady=15,
                             relief=tk.RAISED, borderwidth=3)
        btn_start.pack(pady=30)
        
        # Информация о разработке
        info = tk.Label(center_frame, 
                       text="Используйте меню слева для настройки игры", 
                       font=("Arial", 9, "italic"), bg=Colors.MENU_BG.value, 
                       fg="#999999")
        info.pack(pady=(10, 30))
    
    def _on_start_click(self) -> None:
        """Обработчик нажатия кнопки начала игры"""
        if self.start_game_callback:
            self.start_game_callback()
