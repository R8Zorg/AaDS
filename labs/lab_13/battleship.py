import tkinter as tk
from enum import Enum
from tkinter import messagebox
from typing import Dict, Optional, Tuple

from config import AttackAlgorithm, CellState, Colors, GUISize
from field_canvas import FieldCanvas
from game_logic import GameLogic
from main_menu import MainMenu
from placement_menu import PlacementMenu
from ship import Ship


class GameState(Enum):
    MENU = "menu"
    PLACEMENT = "placement"
    GAME = "game"


class Battleship(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Морской Бой")
        self.configure(bg=Colors.BG.value)

        self.game_logic: GameLogic = GameLogic()

        self.current_state: GameState = GameState.MENU

        self.main_menu: Optional[MainMenu] = None

        self.placement_menu: Optional[PlacementMenu] = None
        self.player_canvas: Optional[FieldCanvas] = None
        self.bot_canvas: Optional[FieldCanvas] = None
        self.player_stats_label: Optional[tk.Label] = None
        self.bot_stats_label: Optional[tk.Label] = None
        self.ready_button: Optional[tk.Button] = None
        self.restart_button: Optional[tk.Button] = None
        self.menu_button: Optional[tk.Button] = None

        self.preview_position: Optional[Tuple[int, int]] = None

        self._show_main_menu()

    def _center_window(self) -> None:
        self.update_idletasks()
        width: int = self.winfo_width()
        height: int = self.winfo_height()
        x: int = (self.winfo_screenwidth() // 2) - (width // 2)
        y: int = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _show_main_menu(self) -> None:
        self._clear_window()

        self.current_state = GameState.MENU

        self.main_menu = MainMenu(self, self._start_placement)
        self.main_menu.pack(fill=tk.BOTH, expand=True)

        self.geometry("700x600")
        self._center_window()

    def _start_placement(self) -> None:
        self._clear_window()

        self.current_state = GameState.PLACEMENT
        self.game_logic.reset_game()

        main_container: tk.Frame = tk.Frame(self, bg=Colors.BG.value)
        main_container.pack(
            fill=tk.BOTH,
            expand=True,
            padx=GUISize.PADDING.value,
            pady=GUISize.PADDING.value,
        )

        self.placement_menu = PlacementMenu(
            main_container,
            self.game_logic,
            self._on_ready,
            self._check_ready_button,
            self._update_display,
        )
        self.placement_menu.pack(
            side=tk.LEFT, fill=tk.Y, padx=(0, GUISize.PADDING.value)
        )

        game_container: tk.Frame = tk.Frame(main_container, bg=Colors.BG.value)
        game_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        fields_container: tk.Frame = tk.Frame(game_container, bg=Colors.BG.value)
        fields_container.pack(pady=(0, GUISize.PADDING.value))

        player_frame: tk.Frame = tk.Frame(fields_container, bg=Colors.BG.value)
        player_frame.pack(side=tk.LEFT, padx=GUISize.PADDING.value)

        player_title: tk.Label = tk.Label(
            player_frame,
            text="Ваше поле",
            font=("Arial", 14, "bold"),
            bg=Colors.BG.value,
        )
        player_title.pack(pady=(0, 5))

        self.player_stats_label = tk.Label(
            player_frame, text="", font=("Arial", 10), bg=Colors.BG.value
        )
        self.player_stats_label.pack(pady=(0, 5))

        self.player_canvas = FieldCanvas(
            player_frame,
            is_player=True,
            click_callback=self._on_player_field_click,
            hover_callback=self._on_player_field_hover,
        )
        self.player_canvas.pack()

        bot_frame: tk.Frame = tk.Frame(fields_container, bg=Colors.BG.value)
        bot_frame.pack(side=tk.LEFT, padx=GUISize.PADDING.value)

        bot_title: tk.Label = tk.Label(
            bot_frame,
            text="Поле противника",
            font=("Arial", 14, "bold"),
            bg=Colors.BG.value,
        )
        bot_title.pack(pady=(0, 5))

        self.bot_stats_label = tk.Label(
            bot_frame, text="", font=("Arial", 10), bg=Colors.BG.value
        )
        self.bot_stats_label.pack(pady=(0, 5))

        self.bot_canvas = FieldCanvas(bot_frame, is_player=False)
        self.bot_canvas.pack()

        buttons_frame: tk.Frame = tk.Frame(game_container, bg=Colors.BG.value)
        buttons_frame.pack()

        self.ready_button = tk.Button(
            buttons_frame,
            text="Готов",
            command=self._on_ready,
            bg=Colors.BTN_DISABLED.value,
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            padx=20,
            pady=10,
            state=tk.DISABLED,
            width=15,
        )
        self.ready_button.pack(side=tk.LEFT, padx=5)

        self.restart_button = tk.Button(
            buttons_frame,
            text="Перезапустить",
            command=self._restart_game,
            bg=Colors.BTN_SECONDARY.value,
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            padx=20,
            pady=10,
            width=15,
        )
        self.restart_button.pack(side=tk.LEFT, padx=5)

        self.menu_button = tk.Button(
            buttons_frame,
            text="В меню",
            command=self._show_main_menu,
            bg=Colors.BTN_DANGER.value,
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            padx=20,
            pady=10,
            width=15,
        )
        self.menu_button.pack(side=tk.LEFT, padx=5)

        self.bind("<Button-3>", self._on_right_click)
        self.bind("<Button-2>", self._on_middle_click)

        self.placement_menu.update_ships_list()

        self._update_display()

        self.geometry("")
        self._center_window()

    def _on_player_field_click(self, x: int, y: int) -> None:
        if self.current_state != GameState.PLACEMENT:
            return

        assert self.placement_menu is not None
        selected_ship: Optional[Ship] = self.placement_menu.get_selected_ship()
        if not selected_ship:
            return

        if not self.game_logic.place_player_ship(selected_ship, x, y):
            return

        self.placement_menu.update_ships_list()
        self._update_display()
        self._check_ready_button()

    def _on_player_field_hover(self, x: int, y: int) -> None:
        if self.current_state != GameState.PLACEMENT:
            return

        assert self.placement_menu is not None
        selected_ship: Optional[Ship] = self.placement_menu.get_selected_ship()
        if not selected_ship:
            return

        valid: bool = self.game_logic.player_field.is_valid_position(
            selected_ship, x, y
        )
        assert self.player_canvas is not None
        self.player_canvas.draw_ship_preview(selected_ship, x, y, valid)
        self.preview_position = (x, y)

    def _on_right_click(self, event: tk.Event) -> None:
        if self.current_state != GameState.PLACEMENT:
            return

        assert self.placement_menu is not None
        selected_ship: Optional[Ship] = self.placement_menu.get_selected_ship()
        if not selected_ship:
            return

        selected_ship.rotate()
        if not self.preview_position:
            return

        x, y = self.preview_position
        valid: bool = self.game_logic.player_field.is_valid_position(
            selected_ship, x, y
        )
        assert self.player_canvas is not None
        self.player_canvas.draw_ship_preview(selected_ship, x, y, valid)

    def _on_middle_click(self, event: tk.Event) -> None:
        if self.current_state != GameState.PLACEMENT:
            return

        if event.widget != self.player_canvas:
            return

        cell_size: int = GUISize.CELL_SIZE.value
        x: int = event.x // cell_size
        y: int = event.y // cell_size

        if not FieldCanvas.in_field(x, y):
            return

        ship: Optional[Ship] = self.game_logic.player_field.get_ship_at(x, y)
        if not ship:
            return

        self.game_logic.remove_player_ship(ship)
        assert self.placement_menu is not None
        self.placement_menu.update_ships_list()
        self._update_display()
        self._check_ready_button()

    def _check_ready_button(self) -> None:
        assert self.ready_button is not None
        if self.game_logic.all_player_ships_placed():
            self.ready_button.config(state=tk.NORMAL, bg=Colors.BTN_READY.value)
        else:
            self.ready_button.config(state=tk.DISABLED, bg=Colors.BTN_DISABLED.value)

    def _on_ready(self) -> None:
        if not self.game_logic.all_player_ships_placed():
            messagebox.showwarning(
                "Внимание", "Разместите все корабли перед началом игры!"
            )
            return

        assert self.placement_menu is not None
        attack_algorithm: AttackAlgorithm = (
            self.placement_menu.get_bot_attack_algorithm()
        )
        self.placement_menu.update_show_enemy_mark()
        self.placement_menu.update_highlight_mark()

        if not self.game_logic.start_game(attack_algorithm):
            return

        self._start_game_screen()

    def _start_game_screen(self) -> None:
        self.current_state = GameState.GAME

        assert self.placement_menu is not None
        self.placement_menu.destroy()
        self.placement_menu = None

        assert self.ready_button is not None
        self.ready_button.config(state=tk.DISABLED)

        assert self.bot_canvas is not None
        self.bot_canvas.click_callback = self._on_bot_field_click

        self._update_display()

        self.geometry("")
        self._center_window()

    def _on_bot_field_click(self, x: int, y: int) -> None:
        if self.current_state != GameState.GAME or self.game_logic.game_over:
            return

        if not self.game_logic.player_turn:
            return

        result: Optional[CellState] = self.game_logic.player_attack(x, y)

        if not result:
            return

        self._update_display()

        if self.game_logic.game_over:
            self._show_game_over()
            return

        if not self.game_logic.player_turn:
            self.after(500, self._bot_turn)

    def _bot_turn(self) -> None:
        if self.game_logic.game_over or self.game_logic.player_turn:
            return

        result: Optional[Tuple[Tuple[int, int], Optional[CellState]]] = (
            self.game_logic.bot_attack()
        )

        if not result:
            return

        self._update_display()

        if self.game_logic.game_over:
            self._show_game_over()
            return

        coords, attack_result = result
        if attack_result not in [CellState.HIT, CellState.DESTROYED]:
            return

        self.after(500, self._bot_turn)

    def _update_display(self) -> None:
        if not self.player_canvas or not self.bot_canvas:
            return

        self.player_canvas.draw_field(
            self.game_logic.player_field.field,
            show_ships=True,
            highlight_surrounding=self.game_logic.highlight_surrounding,
        )

        self.bot_canvas.draw_field(
            self.game_logic.bot_field.field,
            show_ships=self.game_logic.show_enemy_ships,
            highlight_surrounding=self.game_logic.highlight_surrounding,
        )

        if not self.player_stats_label and not self.bot_stats_label:
            return

        player_stats: Dict[str, int] = self.game_logic.get_player_stats()
        bot_stats: Dict[str, int] = self.game_logic.get_bot_stats()

        player_text: str = (
            f"Потоплено: {player_stats['destroyed_ships']}/"
            f"{player_stats['total_ships']} кораблей "
        )

        bot_text: str = (
            f"Потоплено: {bot_stats['destroyed_ships']}/"
            f"{bot_stats['total_ships']} кораблей "
        )

        assert self.player_stats_label is not None
        self.player_stats_label.config(text=player_text)
        assert self.bot_stats_label is not None
        self.bot_stats_label.config(text=bot_text)

    def _show_game_over(self) -> None:
        if self.game_logic.winner == "player":
            message: str = "Вы победили!"
            title: str = "Победа!"
        else:
            message = "Вы проиграли."
            title = "Поражение"

        messagebox.showinfo(title, message)

    def _restart_game(self) -> None:
        self._start_placement()

    def _clear_window(self) -> None:
        for widget in self.winfo_children():
            widget.destroy()

        self.main_menu = None
        self.placement_menu = None
        self.player_canvas = None
        self.bot_canvas = None
        self.player_stats_label = None
        self.bot_stats_label = None
        self.ready_button = None
        self.restart_button = None
        self.menu_button = None
