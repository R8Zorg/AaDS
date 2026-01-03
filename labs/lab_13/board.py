from cell_state import CellState
from orientation import Orientation
from ship import Ship

GRID_SIZE = 10


class Board:
    def __init__(self, grid_size: int = GRID_SIZE) -> None:
        self.size = grid_size
        self.reset()

    def reset(self) -> None:
        self.grid: list[list[int]] = [
            [CellState.EMPTY for _ in range(self.size)] for _ in range(self.size)
        ]
        self.ships: list[Ship] = []
        self.place_history = []

    def in_bounds(self, x, y) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size

    def can_place_ship(self, x: int, y: int, orientation: str, length: int) -> bool:
        """
        Проверяет, можно ли разместить корабль длины length,
        начиная в (x,y), при ориентации:
         - 'H' -> влево: клетками (x, y), (x-1, y), ..., (x-length+1, y)
         - 'V' -> вниз:  (x, y), (x, y+1), ..., (x, y+length-1)
        Также проверяет правило no-touch (включая диагонали).
        """
        coords: list[tuple[int, int]] = []
        if orientation == Orientation.H:
            x0 = x - (length - 1)
            if x0 < 0:
                return False
            for xi in range(x0, x + 1):
                coords.append((xi, y))
        else:
            y1 = y + (length - 1)
            if y1 >= self.size:
                return False
            for yi in range(y, y + length):
                coords.append((x, yi))

        for cx, cy in coords:
            if not self.in_bounds(cx, cy):
                return False
            if self.grid[cy][cx] != CellState.EMPTY:
                return False
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = cx + dx, cy + dy
                    if self.in_bounds(nx, ny):
                        if self.grid[ny][nx] == CellState.SHIP:
                            return False
        return True

    def place_ship(
        self, x: int, y: int, orientation: Orientation, length: int
    ) -> Ship | None:
        """
        Размещает корабль, если можно. Возвращает Ship или None.
        """
        if not self.can_place_ship(x, y, orientation, length):
            return None
        coords = []
        if orientation == Orientation.H:
            x0 = x - (length - 1)
            for xi in range(x0, x + 1):
                coords.append((xi, y))
        else:
            for yi in range(y, y + length):
                coords.append((x, yi))
        ship = Ship(length, coords, orientation)
        self.ships.append(ship)
        for cx, cy in coords:
            self.grid[cy][cx] = CellState.SHIP
        self.place_history.append(ship)
        return ship

    def remove_last_ship(self) -> bool:
        if not self.place_history:
            return False
        ship = self.place_history.pop()
        if ship in self.ships:
            self.ships.remove(ship)
        for cx, cy in ship.cells:
            if self.in_bounds(cx, cy) and self.grid[cy][cx] == CellState.SHIP:
                self.grid[cy][cx] = CellState.EMPTY
        return True

    def receive_shot(self, x: int, y: int) -> tuple[CellState | None, Ship | None]:
        """
        Возвращает строку: 'miss', 'hit', 'sunk', 'repeat'
        и ссылку на корабль (или None).
        """
        state = self.grid[y][x]
        if state == CellState.EMPTY:
            self.grid[y][x] = CellState.MISS
            return CellState.MISS, None
        if state == CellState.SHIP:
            self.grid[y][x] = CellState.HIT
            ship = self.find_ship_by_cell(x, y)
            if ship:
                ship.register_hit(x, y)
                if ship.is_sunk():
                    for cx, cy in ship.cells:
                        self.grid[cy][cx] = CellState.SUNK
                    return CellState.SUNK, ship
                return CellState.HIT, ship
            return CellState.HIT, None
        return None, None

    def find_ship_by_cell(self, x: int, y: int) -> Ship | None:
        for ship in self.ships:
            if ship.occupies(x, y):
                return ship
        return None

    def all_ships_sunk(self) -> bool:
        return all(ship.is_sunk() for ship in self.ships) and bool(self.ships)
