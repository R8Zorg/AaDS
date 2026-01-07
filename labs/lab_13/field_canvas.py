import tkinter as tk
from typing import Callable, List, Optional, Tuple

from config import FIELD_SIZE, CellState, Colors, GUISize
from ship import Ship


class FieldCanvas(tk.Canvas):
    def __init__(
        self,
        parent: tk.Widget,
        is_player: bool = True,
        click_callback: Optional[Callable[[int, int], None]] = None,
        hover_callback: Optional[Callable[[int, int], None]] = None,
    ) -> None:
        canvas_size: int = FIELD_SIZE * GUISize.CELL_SIZE.value
        super().__init__(
            parent,
            width=canvas_size,
            height=canvas_size,
            bg=Colors.BG.value,
            highlightthickness=1,
            highlightbackground=Colors.LINE.value,
        )

        self.is_player: bool = is_player
        self.click_callback: Optional[Callable[[int, int], None]] = click_callback
        self.hover_callback: Optional[Callable[[int, int], None]] = hover_callback
        self.hover_cell: Optional[Tuple[int, int]] = None
        self.selected_ship: Optional[Ship] = None

        self.bind("<Button-1>", self._on_click)
        self.bind("<Motion>", self._on_motion)
        self.bind("<Leave>", self._on_leave)

        self._draw_grid()

    def _draw_grid(self) -> None:
        cell_size: int = GUISize.CELL_SIZE.value

        for i in range(FIELD_SIZE + 1):
            self.create_line(
                i * cell_size,
                0,
                i * cell_size,
                FIELD_SIZE * cell_size,
                fill=Colors.LINE.value,
                width=1,
            )
            self.create_line(
                0,
                i * cell_size,
                FIELD_SIZE * cell_size,
                i * cell_size,
                fill=Colors.LINE.value,
                width=1,
            )

    def draw_field(
        self,
        field: List[List[CellState]],
        show_ships: bool = True,
        highlight_surrounding: bool = True,
    ) -> None:
        self.delete("cell")

        cell_size: int = GUISize.CELL_SIZE.value

        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                cell_state: CellState = field[y][x]
                color: str = self._get_cell_color(cell_state, show_ships)

                x1: int = x * cell_size + 1
                y1: int = y * cell_size + 1
                x2: int = x1 + cell_size - 2
                y2: int = y1 + cell_size - 2

                self.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline=color, tags="cell"
                )

        if highlight_surrounding and not self.is_player:
            self._highlight_surrounding_cells(field)

    def _get_cell_color(self, state: CellState, show_ships: bool) -> str:
        if state == CellState.EMPTY:
            return Colors.EMPTY.value
        elif state == CellState.SHIP:
            if show_ships or self.is_player:
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

    def _highlight_surrounding_cells(self, field: List[List[CellState]]) -> None:
        cell_size: int = GUISize.CELL_SIZE.value

        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                if field[y][x] != CellState.DESTROYED:
                    continue

                for offset_x in range(-1, 2):
                    for offset_y in range(-1, 2):
                        next_x, next_y = x + offset_x, y + offset_y
                        if not self.in_field(next_x, next_y):
                            continue

                        if field[next_y][next_x] != CellState.NO_SHIP:
                            continue

                        x1: int = next_x * cell_size + 1
                        y1: int = next_y * cell_size + 1
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
        self.delete("preview")

        if x is None or y is None:
            return

        cell_size: int = GUISize.CELL_SIZE.value
        color: str = Colors.SELECTED.value if valid else Colors.INVALID.value

        ship.x, ship.y = x, y
        coords: List[Tuple[int, int]] = ship.get_coordinates()
        ship.x, ship.y = None, None

        for cell_x, cell_y in coords:
            if not self.in_field(cell_x, cell_y):
                continue

            x1: int = cell_x * cell_size + 1
            y1: int = cell_y * cell_size + 1
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

        if not self.in_field(x, y):
            return

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
        cell_size: int = GUISize.CELL_SIZE.value
        x: int = event.x // cell_size
        y: int = event.y // cell_size

        if not self.in_field(x, y):
            return

        if not self.click_callback:
            return

        self.click_callback(x, y)

    def _on_motion(self, event: tk.Event) -> None:
        cell_size: int = GUISize.CELL_SIZE.value
        x: int = event.x // cell_size
        y: int = event.y // cell_size

        if self.in_field(x, y):
            if self.hover_cell == (x, y):
                return

            self.hover_cell = (x, y)
            self.highlight_cell(x, y)

            if not self.hover_callback:
                return

            self.hover_callback(x, y)
        else:
            self.hover_cell = None
            self.delete("highlight")

    def _on_leave(self, event: tk.Event) -> None:
        self.hover_cell = None
        self.delete("highlight")
        self.delete("preview")

    @staticmethod
    def in_field(x: int, y: int) -> bool:
        return 0 <= x < FIELD_SIZE and 0 <= y < FIELD_SIZE
