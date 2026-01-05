from typing import Dict, List, Optional, Set, Tuple

from config import FIELD_SIZE, CellState
from ship import Ship


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
        old_x, old_y = ship.x, ship.y  # TODO: ?
        ship.x, ship.y = x, y

        coords: List[Tuple[int, int]] = ship.get_coordinates()

        ship.x, ship.y = old_x, old_y

        for cx, cy in coords:
            if cx < 0 or cx >= FIELD_SIZE or cy < 0 or cy >= FIELD_SIZE:
                return False

        for cx, cy in coords:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < FIELD_SIZE and 0 <= ny < FIELD_SIZE:
                        if (nx, ny) in self.ship_cells and self.ship_cells[
                            (nx, ny)
                        ] != ship:
                            return False

        return True

    def place_ship(self, ship: Ship, x: int, y: int) -> bool:
        if not self.is_valid_position(ship, x, y):
            return False

        # Удаляем старые координаты, если корабль уже был размещён
        # if ship.x is not None and ship.y is not None:
        #     for coord in ship.get_coordinates():
        #         if coord in self.ship_cells:
        #             del self.ship_cells[coord]
        #             self.field[coord[1]][coord[0]] = CellState.EMPTY

        ship.x = x
        ship.y = y

        if ship not in self.ships:
            self.ships.append(ship)

        for coord in ship.get_coordinates():
            self.field[coord[1]][coord[0]] = CellState.SHIP
            self.ship_cells[coord] = ship

        return True

    def remove_ship(self, ship: Ship) -> None:
        if ship in self.ships:
            for coord in ship.get_coordinates():
                if coord in self.ship_cells:
                    del self.ship_cells[coord]
                    self.field[coord[1]][coord[0]] = CellState.EMPTY
            self.ships.remove(ship)
            ship.x = None
            ship.y = None

    def get_ship_at(self, x: int, y: int) -> Optional[Ship]:
        return self.ship_cells.get((x, y))

    def attack(self, x: int, y: int) -> str:
        """
        Args:
            x, y: координаты атаки

        Returns:
            str: результат атаки ("miss", "hit", "destroyed", "already_attacked")
        """
        current_state: CellState = self.field[y][x]

        if current_state in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
            return "already_attacked"

        if (x, y) in self.ship_cells:
            ship: Ship = self.ship_cells[(x, y)]
            ship.hit()

            if ship.is_destroyed():
                # Помечаем весь корабль как уничтоженный
                for coord in ship.get_coordinates():
                    self.field[coord[1]][coord[0]] = CellState.DESTROYED

                # Помечаем соседние клетки как промахи
                self.mark_surrounding_cells(ship)  # TODO: только если включено
                return "destroyed"
            else:
                self.field[y][x] = CellState.HIT
                return "hit"
        else:
            self.field[y][x] = CellState.MISS
            return "miss"

    def mark_surrounding_cells(self, ship: Ship) -> None:
        coords: List[Tuple[int, int]] = ship.get_coordinates()
        for cx, cy in coords:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < FIELD_SIZE and 0 <= ny < FIELD_SIZE:
                        if self.field[ny][nx] == CellState.EMPTY:
                            # WARN: есл не CellState.MISS, то бот может атаковать клетку рядом с потопленным кораблём
                            self.field[ny][nx] = CellState.NO_SHIP

    def get_all_ship_coordinates(self) -> Set[Tuple[int, int]]:
        return set(self.ship_cells.keys())

    def is_all_ships_destroyed(self) -> bool:
        return all(ship.is_destroyed() for ship in self.ships)

    def get_stats(self) -> Dict[str, int]:
        """
        Returns:
            dict: {"destroyed_ships": int, "total_ships": int,
                   "destroyed_cells": int, "total_cells": int}
        """
        destroyed_ships: int = sum(1 for ship in self.ships if ship.is_destroyed())
        total_ships: int = len(self.ships)

        destroyed_cells: int = sum(
            ship.size for ship in self.ships if ship.is_destroyed()
        )
        total_cells: int = sum(ship.size for ship in self.ships)

        return {
            "destroyed_ships": destroyed_ships,
            "total_ships": total_ships,
            "destroyed_cells": destroyed_cells,
            "total_cells": total_cells,
        }
