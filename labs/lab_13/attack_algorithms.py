import random
from enum import Enum
from typing import List, Optional, Set, Tuple

from config import FIELD_SIZE, SHIPS, AttackAlgorithm, CellState
from field_canvas import FieldCanvas
from game_field import GameField


class AttackMode(Enum):
    SEARCH = "search"
    HUNT = "hunt"


class ShipOrientation(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


DO_NOT_ATTACK_CELLS: Set[CellState] = {
    CellState.HIT,
    CellState.DESTROYED,
    CellState.MISS,
    CellState.NO_SHIP,
}

INVALID_CELLS: Set[CellState] = {
    CellState.DESTROYED,
    CellState.MISS,
    CellState.NO_SHIP,
}

DIRECTIONS: List[Tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class AttackAlgorithms:
    def __init__(self, algorithm_type: AttackAlgorithm) -> None:
        self.algorithm_type: AttackAlgorithm = algorithm_type
        self.mode: AttackMode = AttackMode.SEARCH
        self.target_ship: List[Tuple[int, int]] = []
        self.potential_targets: List[Tuple[int, int]] = []
        self.ship_orientation: Optional[ShipOrientation] = None
        self.found_ship_sizes: List[int] = []

        self.priority_zones: List[Tuple[int, int, int]] = self._init_priority_zones()
        self.heat_map: List[List[int]] = [[0] * FIELD_SIZE for _ in range(FIELD_SIZE)]

        self.attack_methods = {
            AttackAlgorithm.RANDOM: self._random_attack,
            AttackAlgorithm.ALGORITHM_1: self._algorithm1_attack,
            AttackAlgorithm.ALGORITHM_2: self._algorithm2_attack,
        }

    def _init_priority_zones(self) -> List[Tuple[int, int, int]]:
        zones: List[Tuple[int, int, int]] = []
        center_coords = {(x, y) for x in range(3, 7) for y in range(3, 7)}

        zones.extend((x, y, 3) for x, y in center_coords)
        zones.extend(
            (x, y, 2)
            for x in range(2, 8)
            for y in range(2, 8)
            if (x, y) not in center_coords
        )

        return zones

    def get_next_attack(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        return self.attack_methods.get(self.algorithm_type, self._random_attack)(
            player_field
        )

    def _random_attack(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        available = [
            (x, y)
            for y in range(FIELD_SIZE)
            for x in range(FIELD_SIZE)
            if player_field.field[y][x] not in DO_NOT_ATTACK_CELLS
        ]
        return random.choice(available) if available else None

    def _algorithm1_attack(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        if self.mode == AttackMode.HUNT and self.potential_targets:
            return self._hunt_mode(player_field)
        return self._search_mode(player_field)

    def _search_mode(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        ship_counts = {
            size: sum(1 for s in self.found_ship_sizes if s == size)
            for size in [4, 3, 2]
        }

        if ship_counts[4] == 0:
            search_size = 4
        elif ship_counts[3] < 2:
            search_size = 3
        elif ship_counts[2] < 3:
            search_size = 2
        else:
            search_size = 1

        candidates = [
            (x, y)
            for y in range(FIELD_SIZE)
            for x in range(FIELD_SIZE)
            if player_field.field[y][x] not in DO_NOT_ATTACK_CELLS
            and (x + y + 1) % search_size == 0
        ]

        return random.choice(candidates) if candidates else None

    def _hunt_mode(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        while self.potential_targets:
            target = self.potential_targets.pop(0)
            if player_field.field[target[1]][target[0]] not in DO_NOT_ATTACK_CELLS:
                return target

        self.mode = AttackMode.SEARCH
        return self._search_mode(player_field)

    def _algorithm2_attack(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        if self.mode == AttackMode.HUNT and self.potential_targets:
            return self._hunt_mode(player_field)

        self._update_heat_map(player_field)

        max_heat = -1
        best_targets = []

        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                if player_field.field[y][x] in DO_NOT_ATTACK_CELLS:
                    continue

                heat = self.heat_map[y][x]
                if heat > max_heat:
                    max_heat = heat
                    best_targets = [(x, y)]
                elif heat == max_heat:
                    best_targets.append((x, y))

        return random.choice(best_targets) if best_targets else None

    def _update_heat_map(self, player_field: GameField) -> None:
        self.heat_map = [[0] * FIELD_SIZE for _ in range(FIELD_SIZE)]

        for x, y, priority in self.priority_zones:
            if player_field.field[y][x] not in DO_NOT_ATTACK_CELLS:
                self.heat_map[y][x] = priority

        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                if player_field.field[y][x] != CellState.HIT:
                    continue

                for dx, dy in DIRECTIONS:
                    nx, ny = x + dx, y + dy
                    if (
                        FieldCanvas.in_field(nx, ny)
                        and player_field.field[ny][nx] not in DO_NOT_ATTACK_CELLS
                    ):
                        self.heat_map[ny][nx] += 10

        ship_counts = {
            size: sum(1 for s in self.found_ship_sizes if s == size)
            for size in [4, 3, 2, 1]
        }

        for size, count in ship_counts.items():
            if count < SHIPS[size]:
                self._add_ship_possibilities(player_field, size)

    def _add_ship_possibilities(self, player_field: GameField, size: int) -> None:
        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                if x + size <= FIELD_SIZE:
                    cells = [player_field.field[y][x + i] for i in range(size)]
                    if not any(cell in INVALID_CELLS for cell in cells):
                        for i in range(size):
                            if cells[i] not in DO_NOT_ATTACK_CELLS:
                                self.heat_map[y][x + i] += 1

                if y + size <= FIELD_SIZE:
                    cells = [player_field.field[y + i][x] for i in range(size)]
                    if not any(cell in INVALID_CELLS for cell in cells):
                        for i in range(size):
                            if cells[i] not in DO_NOT_ATTACK_CELLS:
                                self.heat_map[y + i][x] += 1

    def process_attack_result(
        self, x: int, y: int, result: Optional[CellState], player_field: GameField
    ) -> None:
        if result == CellState.HIT:
            self.mode = AttackMode.HUNT
            self.target_ship.append((x, y))

            if len(self.target_ship) == 1:
                self.potential_targets = [
                    (x + dx, y + dy)
                    for dx, dy in DIRECTIONS
                    if FieldCanvas.in_field(x + dx, y + dy)
                    and player_field.field[y + dy][x + dx] not in DO_NOT_ATTACK_CELLS
                ]
            else:
                self.ship_orientation = (
                    ShipOrientation.VERTICAL
                    if self.target_ship[0][0] == self.target_ship[1][0]
                    else ShipOrientation.HORIZONTAL
                )
                self._update_targets_by_orientation(x, y, player_field)

        elif result == CellState.DESTROYED:
            if self.target_ship:
                self.found_ship_sizes.append(len(self.target_ship) + 1)

            self.mode = AttackMode.SEARCH
            self.target_ship = []
            self.potential_targets = []
            self.ship_orientation = None

    def _update_targets_by_orientation(
        self, x: int, y: int, player_field: GameField
    ) -> None:
        self.potential_targets = []

        if self.ship_orientation == ShipOrientation.HORIZONTAL:
            min_x = min(coord[0] for coord in self.target_ship)
            max_x = max(coord[0] for coord in self.target_ship)

            for nx, check_x in [
                (min_x - 1, min_x > 0),
                (max_x + 1, max_x < FIELD_SIZE - 1),
            ]:
                if check_x and player_field.field[y][nx] not in DO_NOT_ATTACK_CELLS:
                    self.potential_targets.append((nx, y))
        else:
            min_y = min(coord[1] for coord in self.target_ship)
            max_y = max(coord[1] for coord in self.target_ship)

            for ny, check_y in [
                (min_y - 1, min_y > 0),
                (max_y + 1, max_y < FIELD_SIZE - 1),
            ]:
                if check_y and player_field.field[ny][x] not in DO_NOT_ATTACK_CELLS:
                    self.potential_targets.append((x, ny))
