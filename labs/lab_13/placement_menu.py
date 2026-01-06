import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Optional, Tuple

from config import AttackAlgorithm, Colors, PlacementAlgorithm
from game_logic import GameLogic
from ship import Ship


class PlacementMenu(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        game_logic: GameLogic,
        on_ready_callback: Callable[[], None],
        check_ready_button: Callable[[], None],
        update_display: Callable[[], None],
    ) -> None:
        super().__init__(
            parent, bg=Colors.MENU_BG.value, relief=tk.RAISED, borderwidth=2
        )

        self.game_logic: GameLogic = game_logic
        self.on_ready_callback: Callable[[], None] = on_ready_callback
        self.selected_ship: Optional[Ship] = None
        self.check_ready_button: Callable[[], None] = check_ready_button
        self.update_display: Callable[[], None] = update_display

        self._create_widgets()

    def _create_widgets(self) -> None:
        title: tk.Label = tk.Label(
            self,
            text="Размещение кораблей",
            font=("Arial", 14, "bold"),
            bg=Colors.MENU_BG.value,
        )
        title.pack(pady=(10, 5))

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        instructions_frame: tk.Frame = tk.Frame(self, bg=Colors.MENU_BG.value)
        instructions_frame.pack(fill=tk.BOTH, padx=10, pady=5)

        instructions_label: tk.Label = tk.Label(
            instructions_frame,
            text="Инструкции:",
            font=("Arial", 11, "bold"),
            bg=Colors.MENU_BG.value,
        )
        instructions_label.pack(anchor=tk.W)

        instructions_text: tk.Text = tk.Text(
            instructions_frame,
            height=8,
            width=30,
            wrap=tk.WORD,
            font=("Arial", 9),
            bg=Colors.MENU_BG.value,
            relief=tk.FLAT,
            cursor="arrow",
        )
        instructions_text.pack(fill=tk.BOTH)
        instructions_text.insert(
            "1.0",
            "• Расставьте все корабли\n"
            "• 1 линкор (4 клетки)\n"
            "• 2 крейсера (3 клетки)\n"
            "• 3 эсминца (2 клетки)\n"
            "• 4 катера (1 клетка)\n\n"
            "Управление:\n"
            "• ЛКМ - разместить корабль\n"
            "• ПКМ - повернуть корабль\n"
            "• СКМ - удалить корабль",
        )
        instructions_text.config(state=tk.DISABLED)

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        ships_frame: tk.Frame = tk.Frame(self, bg=Colors.MENU_BG.value)
        ships_frame.pack(fill=tk.BOTH, padx=10, pady=5)

        ships_label: tk.Label = tk.Label(
            ships_frame,
            text="Корабли для размещения:",
            font=("Arial", 10, "bold"),
            bg=Colors.MENU_BG.value,
        )
        ships_label.pack(anchor=tk.W)

        self.ships_listbox: tk.Listbox = tk.Listbox(
            ships_frame, height=6, font=("Arial", 9)
        )
        self.ships_listbox.pack(fill=tk.BOTH)
        self.ships_listbox.bind("<<ListboxSelect>>", self._on_ship_select)

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        auto_frame: tk.Frame = tk.Frame(self, bg=Colors.MENU_BG.value)
        auto_frame.pack(fill=tk.X, padx=10, pady=5)

        auto_label: tk.Label = tk.Label(
            auto_frame,
            text="Автоматическое размещение:",
            font=("Arial", 10, "bold"),
            bg=Colors.MENU_BG.value,
        )
        auto_label.pack(anchor=tk.W, pady=(0, 5))

        btn_random: tk.Button = tk.Button(
            auto_frame,
            text="Случайно",
            command=self._auto_place_random,
            bg=Colors.BTN_SECONDARY.value,
            fg="white",
            font=("Arial", 9),
            cursor="hand2",
        )
        btn_random.pack(fill=tk.X, pady=2)

        btn_algo1: tk.Button = tk.Button(
            auto_frame,
            text="По алгоритму",
            command=self._auto_place_algoythm,
            bg=Colors.BTN_SECONDARY.value,
            fg="white",
            font=("Arial", 9),
            cursor="hand2",
        )
        btn_algo1.pack(fill=tk.X, pady=2)

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        settings_frame: tk.Frame = tk.Frame(self, bg=Colors.MENU_BG.value)
        settings_frame.pack(fill=tk.X, padx=10, pady=5)

        settings_label: tk.Label = tk.Label(
            settings_frame,
            text="Настройки:",
            font=("Arial", 10, "bold"),
            bg=Colors.MENU_BG.value,
        )
        settings_label.pack(anchor=tk.W, pady=(0, 5))

        self.show_enemy_var: tk.BooleanVar = tk.BooleanVar(value=False)
        check_enemy: tk.Checkbutton = tk.Checkbutton(
            settings_frame,
            text="Показывать вражеские корабли",
            variable=self.show_enemy_var,
            command=self.update_show_enemy_mark,
            bg=Colors.MENU_BG.value,
            font=("Arial", 9),
        )
        check_enemy.pack(anchor=tk.W)

        self.highlight_surrounding_var: tk.BooleanVar = tk.BooleanVar(value=False)
        check_highlight: tk.Checkbutton = tk.Checkbutton(
            settings_frame,
            text="Выделять соседние клетки",
            variable=self.highlight_surrounding_var,
            command=self.update_highlight_mark,
            bg=Colors.MENU_BG.value,
            font=("Arial", 9),
        )
        check_highlight.pack(anchor=tk.W)

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        bot_placement_frame: tk.Frame = tk.Frame(self, bg=Colors.MENU_BG.value)
        bot_placement_frame.pack(fill=tk.X, padx=10, pady=5)

        bot_placement_label: tk.Label = tk.Label(
            bot_placement_frame,
            text="Расстановка бота:",
            font=("Arial", 10, "bold"),
            bg=Colors.MENU_BG.value,
        )
        bot_placement_label.pack(anchor=tk.W, pady=(0, 5))

        self.bot_placement_var: tk.StringVar = tk.StringVar(
            value=PlacementAlgorithm.RANDOM.value
        )

        rb_random: tk.Radiobutton = tk.Radiobutton(
            bot_placement_frame,
            text="Случайно",
            variable=self.bot_placement_var,
            value=PlacementAlgorithm.RANDOM.value,
            command=self._on_bot_placement_change,
            bg=Colors.MENU_BG.value,
            font=("Arial", 9),
        )
        rb_random.pack(anchor=tk.W)

        rb_algo1: tk.Radiobutton = tk.Radiobutton(
            bot_placement_frame,
            text="По алгоритму",
            variable=self.bot_placement_var,
            value=PlacementAlgorithm.ALGORITHM_1.value,
            command=self._on_bot_placement_change,
            bg=Colors.MENU_BG.value,
            font=("Arial", 9),
        )
        rb_algo1.pack(anchor=tk.W)

        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        # Алгоритм атаки бота
        bot_attack_frame: tk.Frame = tk.Frame(self, bg=Colors.MENU_BG.value)
        bot_attack_frame.pack(fill=tk.X, padx=10, pady=5)

        bot_attack_label: tk.Label = tk.Label(
            bot_attack_frame,
            text="Алгоритм атаки бота:",
            font=("Arial", 10, "bold"),
            bg=Colors.MENU_BG.value,
        )
        bot_attack_label.pack(anchor=tk.W, pady=(0, 5))

        self.bot_attack_var: tk.StringVar = tk.StringVar(
            value=AttackAlgorithm.ALGORITHM_1.value
        )

        rb_attack_random: tk.Radiobutton = tk.Radiobutton(
            bot_attack_frame,
            text="Случайный",
            variable=self.bot_attack_var,
            value=AttackAlgorithm.RANDOM.value,
            bg=Colors.MENU_BG.value,
            font=("Arial", 9),
        )
        rb_attack_random.pack(anchor=tk.W)

        rb_attack_algo1: tk.Radiobutton = tk.Radiobutton(
            bot_attack_frame,
            text="Поиск и охота",
            variable=self.bot_attack_var,
            value=AttackAlgorithm.ALGORITHM_1.value,
            bg=Colors.MENU_BG.value,
            font=("Arial", 9),
        )
        rb_attack_algo1.pack(anchor=tk.W)

        rb_attack_algo2: tk.Radiobutton = tk.Radiobutton(
            bot_attack_frame,
            text="Тепловая карта",
            variable=self.bot_attack_var,
            value=AttackAlgorithm.ALGORITHM_2.value,
            bg=Colors.MENU_BG.value,
            font=("Arial", 9),
        )
        rb_attack_algo2.pack(anchor=tk.W)

    def update_ships_list(self) -> None:
        """Обновляет список кораблей для размещения"""
        self.ships_listbox.delete(0, tk.END)

        # Подсчитываем корабли
        ships_count: Dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0}
        for ship in self.game_logic.player_ships_to_place:
            if ship.x is None:
                ships_count[ship.size] += 1

        ship_names: Dict[int, str] = {
            4: "Линкор",
            3: "Крейсер",
            2: "Эсминец",
            1: "Катер",
        }

        for size in [4, 3, 2, 1]:
            count: int = ships_count[size]
            if count > 0:
                text: str = f"{ship_names[size]} (кол-во клеток - {size}): {count} шт."
                self.ships_listbox.insert(tk.END, text)

        # Автоматически выбираем первый доступный корабль
        self._auto_select_ship()

    def _auto_select_ship(self) -> None:
        """Автоматически выбирает первый доступный корабль"""
        # Ищем первый неразмещённый корабль (самый большой)
        for size in [4, 3, 2, 1]:
            for ship in self.game_logic.player_ships_to_place:
                if ship.size == size and ship.x is None:
                    self.selected_ship = ship
                    # Выделяем в списке
                    items: Tuple = self.ships_listbox.get(0, tk.END)
                    ship_names: Dict[int, str] = {
                        4: "Линкор",
                        3: "Крейсер",
                        2: "Эсминец",
                        1: "Катер",
                    }
                    for i, item in enumerate(items):
                        if ship_names[size] in item:
                            self.ships_listbox.selection_clear(0, tk.END)
                            self.ships_listbox.selection_set(i)
                            break
                    return

        self.selected_ship = None

    def _on_ship_select(self, event: tk.Event) -> None:
        selection: Tuple = self.ships_listbox.curselection()
        if not selection:
            return

        index: int = selection[0]
        items: Tuple = self.ships_listbox.get(0, tk.END)
        selected_text: str = items[index]

        if "Линкор" in selected_text:
            size: int = 4
        elif "Крейсер" in selected_text:
            size = 3
        elif "Эсминец" in selected_text:
            size = 2
        else:
            size = 1

        for ship in self.game_logic.player_ships_to_place:
            if ship.size == size and ship.x is None:
                self.selected_ship = ship
                break

    def _auto_place_random(self) -> None:
        self.game_logic.auto_place_player_ships(PlacementAlgorithm.RANDOM)
        self.selected_ship = None
        self.update_ships_list()
        self.check_ready_button()
        self.update_display()

    def _auto_place_algoythm(self) -> None:
        self.game_logic.auto_place_player_ships(PlacementAlgorithm.ALGORITHM_1)
        self.selected_ship = None
        self.update_ships_list()
        self.check_ready_button()
        self.update_display()

    def update_show_enemy_mark(self) -> None:
        self.game_logic.show_enemy_ships = self.show_enemy_var.get()

    def update_highlight_mark(self) -> None:
        self.game_logic.highlight_surrounding = self.highlight_surrounding_var.get()

    def _on_bot_placement_change(self) -> None:
        algo_value: str = self.bot_placement_var.get()
        self.game_logic.set_bot_placement_algorithm(PlacementAlgorithm(algo_value))

    def get_selected_ship(self) -> Optional[Ship]:
        return self.selected_ship

    def get_bot_attack_algorithm(self) -> AttackAlgorithm:
        return AttackAlgorithm(self.bot_attack_var.get())
