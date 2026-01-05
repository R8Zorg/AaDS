"""
Класс FieldCanvas - виджет для отображения игрового поля
"""

import tkinter as tk
from typing import Callable, List, Optional, Tuple

from config import FIELD_SIZE, CellState, Colors, GUISize
from ship import Ship


class FieldCanvas(tk.Canvas):
    """Канвас для отображения игрового поля"""

    def __init__(
        self,
        parent: tk.Widget,
        is_player: bool = True,
        click_callback: Optional[Callable[[int, int], None]] = None,
        hover_callback: Optional[Callable[[int, int], None]] = None,
    ) -> None:
        """
        Инициализация канваса игрового поля

        Args:
            parent: родительский виджет
            is_player: True если поле игрока, False если поле бота
            click_callback: функция обратного вызова при клике
            hover_callback: функция обратного вызова при наведении
        """
        canvas_size: int = FIELD_SIZE * GUISize.CELL_SIZE.value
        super().__init__(
            parent,
            width=canvas_size,
            height=canvas_size,
            bg=Colors.BG.value,
            highlightthickness=1,
            highlightbackground="#CCCCCC",
        )

        self.is_player: bool = is_player
        self.click_callback: Optional[Callable[[int, int], None]] = click_callback
        self.hover_callback: Optional[Callable[[int, int], None]] = hover_callback
        self.hover_cell: Optional[Tuple[int, int]] = None
        self.selected_ship: Optional[Ship] = None

        # Привязываем события
        self.bind("<Button-1>", self._on_click)
        self.bind("<Motion>", self._on_motion)
        self.bind("<Leave>", self._on_leave)

        self._draw_grid()

    def _draw_grid(self) -> None:
        """Рисует сетку поля"""
        cell_size: int = GUISize.CELL_SIZE.value

        # Рисуем линии сетки
        for i in range(FIELD_SIZE + 1):
            # Вертикальные линии
            self.create_line(
                i * cell_size,
                0,
                i * cell_size,
                FIELD_SIZE * cell_size,
                fill="#CCCCCC",
                width=1,
            )
            # Горизонтальные линии
            self.create_line(
                0,
                i * cell_size,
                FIELD_SIZE * cell_size,
                i * cell_size,
                fill="#CCCCCC",
                width=1,
            )

        # Подписи координат
        for i in range(FIELD_SIZE):
            # Буквы сверху (A-J)
            letter: str = chr(65 + i)
            self.create_text(
                i * cell_size + cell_size // 2,
                -10,
                text=letter,
                font=("Arial", 10, "bold"),
            )
            # Цифры слева (1-10)
            self.create_text(
                -15,
                i * cell_size + cell_size // 2,
                text=str(i + 1),
                font=("Arial", 10, "bold"),
            )

    def draw_field(
        self,
        field: List[List[CellState]],
        show_ships: bool = True,
        highlight_adjacent: bool = True,
        game_started: bool = False,
    ) -> None:
        """
        Отрисовывает игровое поле

        Args:
            field: двумерный массив состояний клеток
            show_ships: показывать ли корабли
            highlight_adjacent: выделять ли соседние клетки
            game_started: началась ли игра
        """
        self.delete("cell")

        cell_size: int = GUISize.CELL_SIZE.value

        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                cell_state: CellState = field[y][x]
                color: str = self._get_cell_color(cell_state, show_ships, game_started)

                x1: int = x * cell_size + 1
                y1: int = y * cell_size + 1
                x2: int = x1 + cell_size - 2
                y2: int = y1 + cell_size - 2

                self.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline=color, tags="cell"
                )

        # Если игра началась и нужно выделять соседние клетки
        if game_started and highlight_adjacent and not self.is_player:
            self._highlight_adjacent_cells(field)

    def _get_cell_color(
        self, state: CellState, show_ships: bool, game_started: bool
    ) -> str:
        if state == CellState.EMPTY:
            return Colors.EMPTY.value
        elif state == CellState.SHIP:
            # Показываем корабли только если разрешено
            if show_ships or self.is_player or not game_started:
                return Colors.SHIP.value
            else:
                return Colors.EMPTY.value
        elif state == CellState.HIT:
            return Colors.HIT.value
        elif state == CellState.DESTROYED:
            return Colors.DESTROYED.value
        elif state == CellState.MISS:
            return Colors.MISS.value
        return Colors.EMPTY.value

    def _highlight_adjacent_cells(self, field: List[List[CellState]]) -> None:
        cell_size: int = GUISize.CELL_SIZE.value

        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                if field[y][x] == CellState.DESTROYED:
                    # Проверяем соседние клетки
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < FIELD_SIZE and 0 <= ny < FIELD_SIZE:
                                if field[ny][nx] == CellState.NO_SHIP:
                                    x1: int = nx * cell_size + 1
                                    y1: int = ny * cell_size + 1
                                    x2: int = x1 + cell_size - 2
                                    y2: int = y1 + cell_size - 2

                                    self.create_rectangle(
                                        x1,
                                        y1,
                                        x2,
                                        y2,
                                        fill=Colors.BLACK_MARK.value,
                                        outline=Colors.BLACK_MARK.value,
                                        tags="cell",
                                    )

    def draw_ship_preview(
        self, ship: Ship, x: Optional[int], y: Optional[int], valid: bool = True
    ) -> None:
        """
        Args:
            ship: объект Ship
            x, y: координаты
            valid: валидна ли позиция
        """
        self.delete("preview")

        if x is None or y is None:
            return

        cell_size: int = GUISize.CELL_SIZE.value
        color: str = Colors.SELECTED.value if valid else "#FF5252"

        coords: List[Tuple[int, int]] = []
        for i in range(ship.size):
            if ship.is_horizontal:
                coords.append((x + i, y))
            else:
                coords.append((x, y + i))

        for cx, cy in coords:
            if 0 <= cx < FIELD_SIZE and 0 <= cy < FIELD_SIZE:
                x1: int = cx * cell_size + 1
                y1: int = cy * cell_size + 1
                x2: int = x1 + cell_size - 2
                y2: int = y1 + cell_size - 2

                self.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline=color,
                    tags="preview",
                    stipple="gray50",
                )

    def highlight_cell(self, x: int, y: int) -> None:
        self.delete("highlight")

        if x is not None and y is not None:
            if 0 <= x < FIELD_SIZE and 0 <= y < FIELD_SIZE:
                cell_size: int = GUISize.CELL_SIZE.value
                x1: int = x * cell_size + 1
                y1: int = y * cell_size + 1
                x2: int = x1 + cell_size - 2
                y2: int = y1 + cell_size - 2

                self.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill="",
                    outline=Colors.HOVER.value,
                    width=3,
                    tags="highlight",
                )

    def _on_click(self, event: tk.Event) -> None:
        """Обработчик клика мыши"""
        cell_size: int = GUISize.CELL_SIZE.value
        x: int = event.x // cell_size
        y: int = event.y // cell_size

        if 0 <= x < FIELD_SIZE and 0 <= y < FIELD_SIZE:
            if self.click_callback:
                self.click_callback(x, y)

    def _on_motion(self, event: tk.Event) -> None:
        """Обработчик движения мыши"""
        cell_size: int = GUISize.CELL_SIZE.value
        x: int = event.x // cell_size
        y: int = event.y // cell_size

        if 0 <= x < FIELD_SIZE and 0 <= y < FIELD_SIZE:
            if self.hover_cell != (x, y):
                self.hover_cell = (x, y)
                self.highlight_cell(x, y)

                if self.hover_callback:
                    self.hover_callback(x, y)
        else:
            self.hover_cell = None
            self.delete("highlight")

    def _on_leave(self, event: tk.Event) -> None:
        """Обработчик ухода мыши с канваса"""
        self.hover_cell = None
        self.delete("highlight")
        self.delete("preview")
