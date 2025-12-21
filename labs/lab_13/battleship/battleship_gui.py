import copy
import tkinter as tk
from tkinter import messagebox

from auto_placements import auto_place_patterned, auto_place_random_greedy
from board import Board
from bot_ai import BotAI
from cell_state import CellState
from orientation import Orientation

CELL_PIX = 36
DEFAULT_SHIPS = {4: 1, 3: 2, 2: 3, 1: 4}
GRID_SIZE = 10


class BattleshipGUI:
    def __init__(self, root):
        self.root = root
        root.title("Морской бой")
        self.menu_frame = None
        self.game_frame = None

        self.player_board = Board()
        self.bot_board = Board()
        self.bot_ai = BotAI(mode="HUNT_TARGET")

        self.cell_px = CELL_PIX
        self.orientation = Orientation.H
        self.ships_spec = copy.deepcopy(DEFAULT_SHIPS)
        self.current_ship_queue = self._build_ship_queue(self.ships_spec)
        self.current_ship_index = 0
        self.placing_phase = True
        self.bot_attack_mode = "HUNT_TARGET"
        self.bot_place_algo = "RANDOM"

        self.player_canvas = None
        self.bot_canvas = None
        self.info_label = None
        self.orientation_label = None
        self.next_ship_label = None
        self.ready_btn = None
        self.auto_btn = None
        self.turn_indicator = None

    def _create_menu(self):
        if self.game_frame:
            self.game_frame.destroy()
            self.game_frame = None
        if self.menu_frame:
            self.menu_frame.destroy()
        self.menu_frame = tk.Frame(self.root, padx=20, pady=20)
        self.menu_frame.pack(fill="both", expand=True)

        title = tk.Label(
            self.menu_frame, text="Морской бой", font=("TkDefaultFont", 24, "bold")
        )
        title.pack(pady=(0, 20))

        play_btn = tk.Button(
            self.menu_frame, text="Играть", width=20, command=self._start_game_screen
        )
        play_btn.pack(pady=6)

        instr = (
            "Как размещать корабли:\n"
            "- Выбирай ориентацию: Горизонтально (H) — корабль идёт влево от кликнутой клетки.\n"
            "- Вертикально (V) — корабль идёт вниз от кликнутой клетки.\n"
            "- Нажимай на клетку, чтобы разместить текущий корабль.\n"
            "- Кнопка 'Убрать последний' удалит последний поставленный корабль.\n"
            "- Кнопка 'Сбросить' очистит поле.\n"
            "- Кнопка 'Авто-расстановка' расставит корабли по выбранному алгоритму.\n"
            "- После размещения всех кораблей нажми 'Готов', чтобы начать игру."
        )
        instr_label = tk.Label(self.menu_frame, text=instr, justify="left")
        instr_label.pack(pady=10)

        quit_btn = tk.Button(
            self.menu_frame, text="Выход", width=20, command=self.root.quit
        )
        quit_btn.pack(pady=10)

    def _start_game_screen(self):
        self.player_board.reset()
        self.bot_board.reset()
        self.bot_ai.reset()
        self.orientation = Orientation.H
        self.ships_spec = copy.deepcopy(DEFAULT_SHIPS)
        self.current_ship_queue = self._build_ship_queue(self.ships_spec)
        self.current_ship_index = 0
        self.placing_phase = True
        self.bot_attack_mode = "HUNT_TARGET"
        self.bot_place_algo = "RANDOM"

        if self.menu_frame:
            self.menu_frame.destroy()
            self.menu_frame = None

        if self.game_frame:
            self.game_frame.destroy()
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(fill="both", expand=True)

        top_frame = tk.Frame(self.game_frame)
        top_frame.pack(anchor="nw", pady=4)

        self.turn_indicator = tk.Label(
            top_frame, text="Размещение кораблей", font=("TkDefaultFont", 12, "bold")
        )
        self.turn_indicator.pack(side="left", padx=6)

        self.controls_frame = tk.Frame(self.game_frame)
        self.controls_frame.pack(side="left", anchor="ne", padx=10, pady=10, fill="y")

        orient_frame = tk.LabelFrame(self.controls_frame, text="Ориентация")
        orient_frame.pack(padx=6, pady=6, fill="x")
        btn_h = tk.Button(
            orient_frame,
            text="Горизонтально",
            command=lambda: self.set_orientation(Orientation.H),
        )
        btn_h.pack(side="left", padx=2, pady=4)
        btn_v = tk.Button(
            orient_frame,
            text="Вертикально",
            command=lambda: self.set_orientation(Orientation.V),
        )
        btn_v.pack(side="left", padx=2, pady=4)
        self.orientation_label = tk.Label(
            orient_frame, text=f"Текущая: {self.orientation.value}"
        )
        self.orientation_label.pack(side="left", padx=6)

        place_frame = tk.LabelFrame(self.controls_frame, text="Размещение")
        place_frame.pack(padx=6, pady=6, fill="x")
        self.next_ship_label = tk.Label(place_frame, text=self._next_ship_text())
        self.next_ship_label.pack(pady=2)

        btn_remove_last = tk.Button(
            place_frame, text="Убрать последний", command=self.remove_last_ship
        )
        btn_remove_last.pack(fill="x", padx=4, pady=2)

        btn_reset = tk.Button(
            place_frame, text="Сбросить поле", command=self.reset_player_field
        )
        btn_reset.pack(fill="x", padx=4, pady=2)

        lb_arrangement = tk.Label(place_frame, text="Выбор авто расстановки:")
        lb_arrangement.pack(side="left", padx=2)

        auto_frame = tk.Frame(place_frame)
        auto_frame.pack(fill="x", padx=2, pady=4)

        btn_auto_random = tk.Button(
            auto_frame, text="Auto Rnd", command=lambda: self.auto_place("RANDOM")
        )
        btn_auto_random.pack(side="left", padx=2)
        btn_auto_pattern = tk.Button(
            auto_frame,
            text="Auto Pattern",
            command=lambda: self.auto_place("PATTERNED"),
        )
        btn_auto_pattern.pack(side="left", padx=2)

        bot_frame = tk.LabelFrame(self.controls_frame, text="Бот")
        bot_frame.pack(padx=6, pady=6, fill="x")
        tk.Label(bot_frame, text="Алгоритм атаки:").pack(anchor="w", padx=4)
        var_bot_attack = tk.StringVar(value=self.bot_attack_mode)
        rb1 = tk.Radiobutton(
            bot_frame,
            text="Random",
            variable=var_bot_attack,
            value="RANDOM",
            command=lambda: self.set_bot_attack(var_bot_attack.get()),
        )
        rb1.pack(anchor="w", padx=6)
        rb2 = tk.Radiobutton(
            bot_frame,
            text="Hunt&Target",
            variable=var_bot_attack,
            value="HUNT_TARGET",
            command=lambda: self.set_bot_attack(var_bot_attack.get()),
        )
        rb2.pack(anchor="w", padx=6)

        tk.Label(bot_frame, text="Алгоритм расстановки:").pack(
            anchor="w", padx=4, pady=(6, 0)
        )
        var_bot_place = tk.StringVar(value=self.bot_place_algo)
        rpb1 = tk.Radiobutton(
            bot_frame,
            text="Random",
            variable=var_bot_place,
            value="RANDOM",
            command=lambda: self.set_bot_place(var_bot_place.get()),
        )
        rpb1.pack(anchor="w", padx=6)
        rpb2 = tk.Radiobutton(
            bot_frame,
            text="Patterned",
            variable=var_bot_place,
            value="PATTERNED",
            command=lambda: self.set_bot_place(var_bot_place.get()),
        )
        rpb2.pack(anchor="w", padx=6)

        boards_frame = tk.Frame(self.game_frame)
        boards_frame.pack(padx=8, pady=8)

        player_frame = tk.Frame(boards_frame)
        player_frame.pack(side="left", padx=20)
        tk.Label(player_frame, text="Твоё поле").pack()
        self.player_canvas = tk.Canvas(
            player_frame,
            width=self.cell_px * GRID_SIZE + 1,
            height=self.cell_px * GRID_SIZE + 1,
            bg="lightblue",
        )
        self.player_canvas.pack()
        self.player_canvas.bind("<Button-1>", self.on_player_canvas_click)

        bot_frame_canvas = tk.Frame(boards_frame)
        bot_frame_canvas.pack(side="left", padx=10)
        tk.Label(bot_frame_canvas, text="Поле противника").pack()
        self.bot_canvas = tk.Canvas(
            bot_frame_canvas,
            width=self.cell_px * GRID_SIZE + 1,
            height=self.cell_px * GRID_SIZE + 1,
            bg="lightblue",
        )
        self.bot_canvas.pack()
        self.bot_canvas.bind("<Button-1>", self.on_bot_canvas_click)

        info_frame = tk.Frame(self.game_frame)
        info_frame.pack(fill="x", padx=8, pady=(4, 10))
        self.info_label = tk.Label(
            info_frame, text="Информация: размещай корабли.", anchor="w", justify="left"
        )
        self.info_label.pack(fill="x")
        self.ready_btn = tk.Button(
            info_frame,
            text="Готов",
            state="disabled",
            command=self.on_ready,
        )
        self.ready_btn.pack(fill="x", padx=6, pady=(10, 2))
        restart_btn = tk.Button(
            info_frame, text="Перезапустить", command=self._start_game_screen
        )
        restart_btn.pack(fill="x", padx=6, pady=2)

        new_game_btn = tk.Button(
            info_frame, text="В меню", command=self._create_menu
        )
        new_game_btn.pack(fill="x", padx=6, pady=2)

        self._draw_grid(self.player_canvas)
        self._draw_grid(self.bot_canvas)
        self.update_ui()

    def _build_ship_queue(self, ships_spec):
        queue = []
        for length, count in ships_spec.items():
            queue.extend([length] * count)
        queue.sort(reverse=True)
        return queue

    def set_orientation(self, o):
        self.orientation = o
        if self.orientation_label:
            self.orientation_label.config(text=f"Текущая: {self.orientation.value}")
        self.update_ui()

    def set_bot_attack(self, mode):
        self.bot_attack_mode = mode
        self.bot_ai.mode = mode

    def set_bot_place(self, mode):
        self.bot_place_algo = mode

    def _draw_grid(self, canvas):
        for i in range(GRID_SIZE + 1):
            # vertical lines
            canvas.create_line(
                i * self.cell_px,
                0,
                i * self.cell_px,
                GRID_SIZE * self.cell_px,
                fill="black",
            )
            # horizontal lines
            canvas.create_line(
                0,
                i * self.cell_px,
                GRID_SIZE * self.cell_px,
                i * self.cell_px,
                fill="black",
            )

    def _coords_to_cell(self, event):
        x = event.x // self.cell_px
        y = event.y // self.cell_px
        if x < 0:
            x = 0
        if x >= GRID_SIZE:
            x = GRID_SIZE - 1
        if y < 0:
            y = 0
        if y >= GRID_SIZE:
            y = GRID_SIZE - 1
        return x, y

    def on_player_canvas_click(self, event):
        if not self.placing_phase:
            return
        x, y = self._coords_to_cell(event)
        if self.current_ship_index >= len(self.current_ship_queue):
            self.info("Все корабли уже размещены.")
            return
        length = self.current_ship_queue[self.current_ship_index]
        placed = self.player_board.place_ship(x, y, self.orientation, length)
        if placed:
            self.current_ship_index += 1
            self.info(f"Поставлен корабль {length}-палубный.")
            self.update_ui()
            if self.current_ship_index >= len(self.current_ship_queue):
                self.ready_btn.config(state="normal", bg="lightgreen")
                self.info("Все корабли размещены. Нажми 'Готов' чтобы начать.")
        else:
            self.info("Нельзя разместить корабль в этой позиции.")

    def on_bot_canvas_click(self, event):
        if self.placing_phase:
            self.info("Сначала размести все свои корабли.")
            return
        if self.player_board.all_ships_sunk() or self.bot_board.all_ships_sunk():
            return
        x, y = self._coords_to_cell(event)
        result, ship = self.bot_board.receive_shot(x, y)
        if result is None:
            return
        if result == CellState.MISS:
            self.info("Промах.")
            self.update_ui()
            self.root.after(500, self._bot_turn)
        elif result == CellState.HIT:
            self.info("Попадание!")
            self.update_ui()
        elif result == CellState.SUNK:
            self.info("Корабль потоплен!")
            self.update_ui()

        if self.bot_board.all_ships_sunk():
            self.update_ui()
            messagebox.showinfo(
                "Победа", "Ты потопил все корабли противника! Ты выиграл!"
            )
            self.placing_phase = False

    def _bot_turn(self):
        if self.player_board.all_ships_sunk() or self.bot_board.all_ships_sunk():
            return
        self.bot_ai.mode = self.bot_attack_mode
        shot = self.bot_ai.next_shot(self.player_board)
        if shot is None:
            return
        x, y = shot
        result, ship = self.player_board.receive_shot(x, y)
        self.bot_ai.inform_result(x, y, result, ship)
        if result == CellState.MISS:
            self.info(f"Ход бота: ({x}, {y}) — промах.")
            self.update_ui()
            return
        elif result == CellState.HIT:
            self.info(f"Ход бота: ({x}, {y}) — попадание!")
            self.update_ui()
            self.root.after(400, self._bot_turn)
            return
        elif result == CellState.SUNK:
            self.info(f"Ход бота: ({x}, {y}) — потопил корабль!")
            self.update_ui()
            self.root.after(400, self._bot_turn)
            return
        if self.player_board.all_ships_sunk():
            messagebox.showinfo("Поражение", "Все твои корабли потоплены! Ты проиграл.")
            self.placing_phase = False

    def auto_place(self, algo):
        self.player_board.reset()
        self.current_ship_index = len(self._build_ship_queue(self.ships_spec))
        if algo == "RANDOM":
            ok = auto_place_random_greedy(self.player_board, self.ships_spec)
        else:
            ok = auto_place_patterned(self.player_board, self.ships_spec)
        if not ok:
            messagebox.showwarning(
                "Авто-расстановка", "Не удалось расставить корабли автоматически."
            )
            self.current_ship_index = 0
        else:
            self.info("Корабли расставлены автоматически.")
            self.ready_btn.config(state="normal", bg="lightgreen")
        self.update_ui()

    def _bot_place(self):
        self.bot_board.reset()
        if self.bot_place_algo == "RANDOM":
            ok = auto_place_random_greedy(self.bot_board, self.ships_spec)
        else:
            ok = auto_place_patterned(self.bot_board, self.ships_spec)
        if not ok:
            auto_place_random_greedy(self.bot_board, self.ships_spec)

    def on_ready(self):
        if self.current_ship_index < len(self.current_ship_queue):
            messagebox.showwarning(
                "Не готово", "Размести все корабли прежде, чем начать."
            )
            return
        self.placing_phase = False

        self.next_ship_label = None
        self.orientation_label = None
        self.controls_frame.destroy()
        self.ready_btn.config(state="disabled", bg=self.root.cget("bg"))
        self.info("Игра началась! Твой ход — стреляй по полю противника.")
        self.bot_ai.reset()
        self.bot_ai.mode = self.bot_attack_mode
        self._bot_place()
        self.update_ui()

    def remove_last_ship(self):
        if not self.placing_phase:
            self.info("Уже нельзя менять расстановку.")
            return
        ok = self.player_board.remove_last_ship()
        if ok:
            self.current_ship_index = max(0, self.current_ship_index - 1)
            self.info("Последний корабль удалён.")
            self.ready_btn.config(state="disabled")
        else:
            self.info("Нет кораблей для удаления.")
        self.update_ui()

    def reset_player_field(self):
        if not self.placing_phase:
            self.info("Уже нельзя менять расстановку.")
            return
        self.player_board.reset()
        self.current_ship_index = 0
        self.ready_btn.config(state="disabled")
        self.info("Поле очищено.")
        self.update_ui()

    def _next_ship_text(self):
        if self.current_ship_index >= len(self.current_ship_queue):
            return "Все корабли размещены."
        length = self.current_ship_queue[self.current_ship_index]
        remaining = len(self.current_ship_queue) - self.current_ship_index
        return f"Ставится сейчас: {length}-палубный (осталось {remaining} кораблей разных длин)"

    def info(self, text):
        if self.info_label:
            self.info_label.config(text="Информация: " + text)

    def update_ui(self):
        self._draw_board_on_canvas(
            self.player_board, self.player_canvas, reveal_ships=True
        )
        self._draw_board_on_canvas(self.bot_board, self.bot_canvas, reveal_ships=True)
        if self.next_ship_label:
            self.next_ship_label.config(text=self._next_ship_text())
        if self.orientation_label:
            self.orientation_label.config(text=f"Текущая: {self.orientation.value}")
        if self.placing_phase:
            self.turn_indicator.config(text="Размещение кораблей")
        else:
            self.turn_indicator.config(text="Игра: твой ход")

    def _draw_board_on_canvas(
        self, board: Board, canvas: tk.Canvas, reveal_ships=False
    ):
        canvas.delete("cell")
        for y in range(board.size):
            for x in range(board.size):
                sx = x * self.cell_px
                sy = y * self.cell_px
                ex = sx + self.cell_px
                ey = sy + self.cell_px
                state = board.grid[y][x]
                color = self._color_by_state(state, reveal_ships)
                canvas.create_rectangle(
                    sx + 1,
                    sy + 1,
                    ex - 1,
                    ey - 1,
                    fill=color,
                    outline="",
                    tags=("cell"),
                )
                offset = 5
                if state == CellState.MISS or state == CellState.SUNK:
                    canvas.create_line(
                        sx + offset,
                        sy + offset,
                        ex - offset,
                        ey - offset,
                        width=2,
                        tags=("cell",),
                    )
                    canvas.create_line(
                        ex - offset,
                        sy + offset,
                        sx + offset,
                        ey - offset,
                        width=2,
                        tags=("cell",),
                    )
                if state == CellState.HIT:
                    canvas.create_oval(
                        sx + offset,
                        sy + offset,
                        ex - offset,
                        ey - offset,
                        width=2,
                        tags=("cell",),
                    )
        self._draw_grid(canvas)

    def _color_by_state(self, state, reveal_ships):
        if state == CellState.EMPTY:
            return "#a6d9ff"
        if state == CellState.SHIP:
            return "#6bbf59" if reveal_ships else "#a6d9ff"
        if state == CellState.HIT:
            return "#ffdd57"
        if state == CellState.SUNK:
            return "#ff6b6b"
        if state == CellState.MISS:
            return "#a6d9ff"
        return "#a6d9ff"

    def start(self):
        self._create_menu()
