import random
from enum import Enum
from typing import List

from config import FIELD_SIZE, SHIPS, PlacementAlgorithm
from game_field import GameField
from ship import Ship

"""
1. Стороны: верх-низ или лево-право? (транспонирование базовой матрицы)
2. Зеркалить?
3. Если зеркалить, то по X или по Y?
"""


class PlacementPattern(Enum):
    LEFT_VERTICAL = "left_vertical"
    RIGHT_VERTICAL = "right_vertical"
    TOP_HORIZONTAL = "top_horizontal"
    BOTTOM_HORIZONTAL = "bottom_horizontal"
    LEFT_VERTICAL_ALT = "left_vertical_alt"
    RIGHT_VERTICAL_ALT = "right_vertical_alt"
    TOP_HORIZONTAL_ALT = "top_horizontal_alt"
    BOTTOM_HORIZONTAL_ALT = "bottom_horizontal_alt"


class PlacementAlgorithms:
    @staticmethod
    def random_placement(field: GameField) -> List[Ship]:
        field.reset()
        ships: List[Ship] = []

        for size, count in sorted(SHIPS.items(), reverse=True):
            for _ in range(count):
                placed: bool = False
                attempts: int = 0
                max_attempts: int = 1000

                while not placed and attempts < max_attempts:
                    x: int = random.randint(0, FIELD_SIZE - 1)
                    y: int = random.randint(0, FIELD_SIZE - 1)
                    is_horizontal: bool = random.choice([True, False])

                    ship: Ship = Ship(size, is_horizontal=is_horizontal)

                    if field.place_ship(ship, x, y):
                        ships.append(ship)
                        placed = True

                    attempts += 1

                if not placed:
                    return PlacementAlgorithms.random_placement(field)

        return ships

    @staticmethod
    def algorithm_placement(field: GameField) -> List[Ship]:
        field.reset()

        pattern: PlacementPattern = random.choice(list(PlacementPattern))

        ships: List[Ship] = []

        if pattern == PlacementPattern.LEFT_VERTICAL:
            ships = PlacementAlgorithms._place_left_vertical(field)
        elif pattern == PlacementPattern.RIGHT_VERTICAL:
            ships = PlacementAlgorithms._place_right_vertical(field)
        elif pattern == PlacementPattern.TOP_HORIZONTAL:
            ships = PlacementAlgorithms._place_top_horizontal(field)
        elif pattern == PlacementPattern.BOTTOM_HORIZONTAL:
            ships = PlacementAlgorithms._place_bottom_horizontal(field)
        elif pattern == PlacementPattern.LEFT_VERTICAL_ALT:
            ships = PlacementAlgorithms._place_left_vertical_alt(field)
        elif pattern == PlacementPattern.RIGHT_VERTICAL_ALT:
            ships = PlacementAlgorithms._place_right_vertical_alt(field)
        elif pattern == PlacementPattern.TOP_HORIZONTAL_ALT:
            ships = PlacementAlgorithms._place_top_horizontal_alt(field)
        elif pattern == PlacementPattern.BOTTOM_HORIZONTAL_ALT:
            ships = PlacementAlgorithms._place_bottom_horizontal_alt(field)

        return ships

    @staticmethod
    def _place_left_vertical(field: GameField) -> List[Ship]:
        """
        Размещение по паттерну: линкор слева, корабли вертикально по краям
        Базовая матрица:
        1000000001
        1000000001
        1000000001
        1000000000
        0000000001
        1000000001
        1000000001
        0000000000
        1000000001
        1000000001
        """
        ships: List[Ship] = []

        ship4: Ship = Ship(4, is_horizontal=False)
        if field.place_ship(ship4, 0, 0):
            ships.append(ship4)

        ship3_1: Ship = Ship(3, is_horizontal=False)
        if field.place_ship(ship3_1, 9, 0):
            ships.append(ship3_1)

        ship3_2: Ship = Ship(3, is_horizontal=False)
        if field.place_ship(ship3_2, 9, 4):
            ships.append(ship3_2)

        ship2_1: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_1, 0, 5):
            ships.append(ship2_1)

        ship2_2: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_2, 0, 8):
            ships.append(ship2_2)

        ship2_3: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_3, 9, 8):
            ships.append(ship2_3)

        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_right_vertical(field: GameField) -> List[Ship]:
        ships: List[Ship] = []

        ship4: Ship = Ship(4, is_horizontal=False)
        if field.place_ship(ship4, 9, 0):
            ships.append(ship4)

        ship3_1: Ship = Ship(3, is_horizontal=False)
        if field.place_ship(ship3_1, 0, 0):
            ships.append(ship3_1)

        ship3_2: Ship = Ship(3, is_horizontal=False)
        if field.place_ship(ship3_2, 0, 4):
            ships.append(ship3_2)

        ship2_1: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_1, 9, 5):
            ships.append(ship2_1)

        ship2_2: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_2, 9, 8):
            ships.append(ship2_2)

        ship2_3: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_3, 0, 8):
            ships.append(ship2_3)

        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_top_horizontal(field: GameField) -> List[Ship]:
        ships: List[Ship] = []

        ship4: Ship = Ship(4, is_horizontal=True)
        if field.place_ship(ship4, 0, 0):
            ships.append(ship4)

        ship3_1: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_1, 0, 9):
            ships.append(ship3_1)

        ship3_2: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_2, 4, 9):
            ships.append(ship3_2)

        ship2_1: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_1, 5, 0):
            ships.append(ship2_1)

        ship2_2: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_2, 8, 0):
            ships.append(ship2_2)

        ship2_3: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_3, 8, 9):
            ships.append(ship2_3)

        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_bottom_horizontal(field: GameField) -> List[Ship]:
        """Линкор снизу"""
        ships: List[Ship] = []

        ship4: Ship = Ship(4, is_horizontal=True)
        if field.place_ship(ship4, 0, 9):
            ships.append(ship4)

        ship3_1: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_1, 0, 0):
            ships.append(ship3_1)

        ship3_2: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_2, 4, 0):
            ships.append(ship3_2)

        ship2_1: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_1, 5, 9):
            ships.append(ship2_1)

        ship2_2: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_2, 8, 9):
            ships.append(ship2_2)

        ship2_3: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_3, 8, 0):
            ships.append(ship2_3)

        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_left_vertical_alt(field: GameField) -> List[Ship]:
        """
        Альтернативное размещение слева:
        1010000000
        1010000000
        1010000000
        1000000000
        0010000000
        1010000000
        1010000000
        0000000000
        1010000000
        1010000000
        """
        ships: List[Ship] = []

        ship4: Ship = Ship(4, is_horizontal=False)
        if field.place_ship(ship4, 0, 0):
            ships.append(ship4)

        ship3_1: Ship = Ship(3, is_horizontal=False)
        if field.place_ship(ship3_1, 2, 0):
            ships.append(ship3_1)

        ship3_2: Ship = Ship(3, is_horizontal=False)
        if field.place_ship(ship3_2, 2, 4):
            ships.append(ship3_2)

        ship2_1: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_1, 0, 5):
            ships.append(ship2_1)

        ship2_2: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_2, 0, 8):
            ships.append(ship2_2)

        ship2_3: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_3, 2, 8):
            ships.append(ship2_3)

        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_right_vertical_alt(field: GameField) -> List[Ship]:
        """Зеркальное отражение left_vertical_alt"""
        ships: List[Ship] = []

        ship4: Ship = Ship(4, is_horizontal=False)
        if field.place_ship(ship4, 9, 0):
            ships.append(ship4)

        ship3_1: Ship = Ship(3, is_horizontal=False)
        if field.place_ship(ship3_1, 7, 0):
            ships.append(ship3_1)

        ship3_2: Ship = Ship(3, is_horizontal=False)
        if field.place_ship(ship3_2, 7, 4):
            ships.append(ship3_2)

        ship2_1: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_1, 9, 5):
            ships.append(ship2_1)

        ship2_2: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_2, 9, 8):
            ships.append(ship2_2)

        ship2_3: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_3, 7, 8):
            ships.append(ship2_3)

        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_top_horizontal_alt(field: GameField) -> List[Ship]:
        """Транспонированная версия left_vertical_alt"""
        ships: List[Ship] = []

        ship4: Ship = Ship(4, is_horizontal=True)
        if field.place_ship(ship4, 0, 0):
            ships.append(ship4)

        ship3_1: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_1, 0, 2):
            ships.append(ship3_1)

        ship3_2: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_2, 4, 2):
            ships.append(ship3_2)

        ship2_1: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_1, 5, 0):
            ships.append(ship2_1)

        ship2_2: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_2, 8, 0):
            ships.append(ship2_2)

        ship2_3: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_3, 8, 2):
            ships.append(ship2_3)

        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_bottom_horizontal_alt(field: GameField) -> List[Ship]:
        ships: List[Ship] = []

        ship4: Ship = Ship(4, is_horizontal=True)
        if field.place_ship(ship4, 0, 9):
            ships.append(ship4)

        ship3_1: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_1, 0, 7):
            ships.append(ship3_1)

        ship3_2: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_2, 4, 7):
            ships.append(ship3_2)

        ship2_1: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_1, 5, 9):
            ships.append(ship2_1)

        ship2_2: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_2, 8, 9):
            ships.append(ship2_2)

        ship2_3: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_3, 8, 7):
            ships.append(ship2_3)

        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_remaining_ships(field: GameField, size: int, count: int) -> List[Ship]:
        ships: List[Ship] = []

        for _ in range(count):
            placed: bool = False
            attempts: int = 0
            max_attempts: int = 1000

            while not placed and attempts < max_attempts:
                x: int = random.randint(0, FIELD_SIZE - 1)
                y: int = random.randint(0, FIELD_SIZE - 1)
                is_horizontal: bool = random.choice([True, False])

                ship: Ship = Ship(size, is_horizontal=is_horizontal)

                if field.place_ship(ship, x, y):
                    ships.append(ship)
                    placed = True

                attempts += 1

        if not placed:
            return PlacementAlgorithms._place_remaining_ships(field, size, count)

        return ships

    @staticmethod
    def place_ships(field: GameField, algorithm_type: PlacementAlgorithm) -> List[Ship]:
        if algorithm_type == PlacementAlgorithm.RANDOM:
            return PlacementAlgorithms.random_placement(field)
        elif algorithm_type == PlacementAlgorithm.ALGORITHM_1:
            return PlacementAlgorithms.algorithm_placement(field)
        else:
            return PlacementAlgorithms.random_placement(field)
