import random
from enum import Enum
from typing import List, Optional, Tuple

from config import FIELD_SIZE, SHIPS, AttackAlgorithm, CellState
from field_canvas import FieldCanvas
from game_field import GameField


class AttackMode(Enum):
    SEARCH = "search"
    HUNT = "hunt"


class ShipOrientation(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


DO_NOT_ATTACK_CELLS: List[CellState] = [
    CellState.HIT,
    CellState.DESTROYED,
    CellState.MISS,
    CellState.NO_SHIP,
]


class AttackAlgorithms:
    def __init__(self, algorithm_type: AttackAlgorithm) -> None:
        self.algorithm_type: AttackAlgorithm = algorithm_type
        self.mode: AttackMode = AttackMode.SEARCH
        self.target_ship: List[Tuple[int, int]] = []
        self.potential_targets: List[Tuple[int, int]] = []
        self.ship_orientation: Optional[ShipOrientation] = None
        self.current_search_size: int = 4
        self.found_ship_sizes: List[int] = []

        self.priority_zones: List[Tuple[int, int, int]] = self._init_priority_zones()
        self.heat_map: List[List[int]] = [
            [0 for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)
        ]

    def _init_priority_zones(self) -> List[Tuple[int, int, int]]:
        zones: List[Tuple[int, int, int]] = []
        for x in range(3, 7):
            for y in range(3, 7):
                zones.append((x, y, 3))

        for x in range(2, 8):
            for y in range(2, 8):
                if not any(z[0] == x and z[1] == y for z in zones):
                    zones.append((x, y, 2))

        return zones

    def get_next_attack(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        if self.algorithm_type == AttackAlgorithm.RANDOM:
            return self._random_attack(player_field)
        elif self.algorithm_type == AttackAlgorithm.ALGORITHM_1:
            return self._algorithm1_attack(player_field)
        elif self.algorithm_type == AttackAlgorithm.ALGORITHM_2:
            return self._algorithm2_attack(player_field)
        else:
            return self._random_attack(player_field)

    def _random_attack(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        available: List[Tuple[int, int]] = []
        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                if player_field.field[y][x] in DO_NOT_ATTACK_CELLS:
                    continue

                available.append((x, y))

        return random.choice(available) if available else None

    def _algorithm1_attack(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        if self.mode == AttackMode.HUNT and self.potential_targets:
            return self._hunt_mode(player_field)
        else:
            return self._search_mode(player_field)

    def _search_mode(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        if len([s for s in self.found_ship_sizes if s == 4]) == 0:
            search_size: int = 4
        elif len([s for s in self.found_ship_sizes if s == 3]) < 2:
            search_size = 3
        elif len([s for s in self.found_ship_sizes if s == 2]) < 3:
            search_size = 2
        else:
            search_size = 1

        candidates: List[Tuple[int, int]] = []
        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                if player_field.field[y][x] in DO_NOT_ATTACK_CELLS:
                    continue

                if (x + y + 1) % search_size != 0:
                    continue

                candidates.append((x, y))

        return random.choice(candidates)

    def _hunt_mode(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        if not self.potential_targets:
            self.mode = AttackMode.SEARCH
            return self._search_mode(player_field)

        target: Tuple[int, int] = self.potential_targets.pop(0)

        if player_field.field[target[1]][target[0]] in DO_NOT_ATTACK_CELLS:
            return self._hunt_mode(player_field)

        return target

    def _algorithm2_attack(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        if self.mode == AttackMode.HUNT and self.potential_targets:
            return self._hunt_mode(player_field)

        self._update_heat_map(player_field)

        max_heat: int = -1
        best_targets: List[Tuple[int, int]] = []

        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                if player_field.field[y][x] in DO_NOT_ATTACK_CELLS:
                    continue

                heat: int = self.heat_map[y][x]
                if heat > max_heat:
                    max_heat = heat
                    best_targets = [(x, y)]
                elif heat == max_heat:
                    best_targets.append((x, y))

        return random.choice(best_targets) if best_targets else None

    def _update_heat_map(self, player_field: GameField) -> None:
        self.heat_map = [[0 for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]

        for x, y, priority in self.priority_zones:
            if player_field.field[y][x] in DO_NOT_ATTACK_CELLS:
                continue

            self.heat_map[y][x] = priority

        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                if player_field.field[y][x] != CellState.HIT:
                    continue

                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if not FieldCanvas.in_field(nx, ny):
                        continue

                    if player_field.field[ny][nx] in DO_NOT_ATTACK_CELLS:
                        continue

                    self.heat_map[ny][nx] += 10

        for size in [4, 3, 2, 1]:
            if len([s for s in self.found_ship_sizes if s == size]) >= SHIPS[size]:
                continue

            self._add_ship_possibilities(player_field, size)

    def _add_ship_possibilities(self, player_field: GameField, size: int) -> None:
        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                can_fit_horizontal: bool = True
                if x + size > FIELD_SIZE:
                    continue

                for i in range(size):
                    if player_field.field[y][x + i] not in [
                        CellState.DESTROYED,
                        CellState.MISS,
                        CellState.NO_SHIP,
                    ]:
                        continue

                    can_fit_horizontal = False
                    break

                if can_fit_horizontal:
                    for i in range(size):
                        if player_field.field[y][x + i] in DO_NOT_ATTACK_CELLS:
                            continue

                        self.heat_map[y][x + i] += 1

                can_fit_vertical: bool = True
                if y + size > FIELD_SIZE:
                    continue

                for i in range(size):
                    if player_field.field[y + i][x] not in [
                        CellState.DESTROYED,
                        CellState.MISS,
                        CellState.NO_SHIP,
                    ]:
                        continue

                    can_fit_vertical = False
                    break

                if can_fit_vertical:
                    for i in range(size):
                        if player_field.field[y + i][x] in DO_NOT_ATTACK_CELLS:
                            continue

                        self.heat_map[y + i][x] += 1

    def process_attack_result(
        self, x: int, y: int, result: Optional[CellState], player_field: GameField
    ) -> None:
        if result == CellState.HIT:
            self.mode = AttackMode.HUNT
            self.target_ship.append((x, y))

            if len(self.target_ship) == 1:
                self.potential_targets = []
                for offset_x, offset_y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    next_x, next_y = x + offset_x, y + offset_y
                    if not FieldCanvas.in_field(next_x, next_y):
                        continue

                    if player_field.field[next_y][next_x] in DO_NOT_ATTACK_CELLS:
                        continue

                    self.potential_targets.append((next_x, next_y))
            else:
                if self.target_ship[0][0] == self.target_ship[1][0]:
                    self.ship_orientation = ShipOrientation.VERTICAL
                else:
                    self.ship_orientation = ShipOrientation.HORIZONTAL

                self._update_targets_by_orientation(x, y, player_field)

        elif result == CellState.DESTROYED:
            if len(self.target_ship) > 0:
                ship_size: int = len(self.target_ship) + 1
                self.found_ship_sizes.append(ship_size)

            self.mode = AttackMode.SEARCH
            self.target_ship = []
            self.potential_targets = []
            self.ship_orientation = None

    def _update_targets_by_orientation(
        self, x: int, y: int, player_field: GameField
    ) -> None:
        self.potential_targets = []

        if self.ship_orientation == ShipOrientation.HORIZONTAL:
            min_x: int = min(coord[0] for coord in self.target_ship)
            max_x: int = max(coord[0] for coord in self.target_ship)

            if (
                min_x > 0
                and player_field.field[y][min_x - 1] not in DO_NOT_ATTACK_CELLS
            ):
                self.potential_targets.append((min_x - 1, y))
            if (
                max_x < FIELD_SIZE - 1
                and player_field.field[y][max_x + 1] not in DO_NOT_ATTACK_CELLS
            ):
                self.potential_targets.append((max_x + 1, y))

        else:
            min_y: int = min(coord[1] for coord in self.target_ship)
            max_y: int = max(coord[1] for coord in self.target_ship)

            if (
                min_y > 0
                and player_field.field[min_y - 1][x] not in DO_NOT_ATTACK_CELLS
            ):
                self.potential_targets.append((x, min_y - 1))
            if (
                max_y < FIELD_SIZE - 1
                and player_field.field[max_y + 1][x] not in DO_NOT_ATTACK_CELLS
            ):
                self.potential_targets.append((x, max_y + 1))
