from typing import Dict, List, Optional, Set, Tuple

from config import FIELD_SIZE, CellState
from ship import Ship
from field_canvas import FieldCanvas


class GameField:
    def __init__(self) -> None:
        self.field: List[List[CellState]] = [
            [CellState.EMPTY for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)
        ]
        self.ships: List[Ship] = []
        self.ship_cells: Dict[Tuple[int, int], Ship] = {}

    def reset(self) -> None:
        self.field = [
            [CellState.EMPTY for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)
        ]
        self.ships = []
        self.ship_cells = {}

    def is_valid_position(self, ship: Ship, x: int, y: int) -> bool:
        ship.x, ship.y = x, y
        coords: list[tuple[int, int]] = ship.get_coordinates()
        ship.x, ship.y = None, None

        for cx, cy in coords:
            if not FieldCanvas.in_field(cx, cy):
                return False

        for cx, cy in coords:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = cx + dx, cy + dy
                    if not FieldCanvas.in_field(nx, ny):
                        continue

                    if (nx, ny) in self.ship_cells:
                        return False
        return True

    def place_ship(self, ship: Ship, x: int, y: int) -> bool:
        if not self.is_valid_position(ship, x, y):
            return False

        ship.x = x
        ship.y = y

        self.ships.append(ship)

        for coord in ship.get_coordinates():
            self.field[coord[1]][coord[0]] = CellState.SHIP
            self.ship_cells[coord] = ship

        return True

    def remove_ship(self, ship: Ship) -> None:
        for coord in ship.get_coordinates():
            if coord not in self.ship_cells:
                continue

            del self.ship_cells[coord]
            self.field[coord[1]][coord[0]] = CellState.EMPTY
        self.ships.remove(ship)
        ship.x, ship.y = None, None

    def get_ship_at(self, x: int, y: int) -> Optional[Ship]:
        return self.ship_cells.get((x, y))

    def attack(self, x: int, y: int) -> Optional[CellState]:
        current_state: CellState = self.field[y][x]

        if current_state in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
            return None

        if (x, y) in self.ship_cells:
            ship: Ship = self.ship_cells[(x, y)]
            ship.hit()

            if ship.is_destroyed():
                for coord in ship.get_coordinates():
                    self.field[coord[1]][coord[0]] = CellState.DESTROYED

                self.mark_surrounding_cells(ship)
                return CellState.DESTROYED
            else:
                self.field[y][x] = CellState.HIT
                return CellState.HIT
        else:
            self.field[y][x] = CellState.MISS
            return CellState.MISS

    def mark_surrounding_cells(self, ship: Ship) -> None:
        coords: List[Tuple[int, int]] = ship.get_coordinates()
        for cx, cy in coords:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = cx + dx, cy + dy
                    if not FieldCanvas.in_field(nx, ny):
                        continue

                    if self.field[ny][nx] != CellState.EMPTY:
                        continue

                    self.field[ny][nx] = CellState.NO_SHIP

    def get_all_ship_coordinates(self) -> Set[Tuple[int, int]]:
        return set(self.ship_cells.keys())

    def is_all_ships_destroyed(self) -> bool:
        return all(ship.is_destroyed() for ship in self.ships)

    def get_stats(self) -> Dict[str, int]:
        destroyed_ships: int = sum(1 for ship in self.ships if ship.is_destroyed())
        total_ships: int = len(self.ships)

        return {
            "destroyed_ships": destroyed_ships,
            "total_ships": total_ships,
        }
