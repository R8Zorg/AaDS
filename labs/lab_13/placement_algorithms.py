"""
Класс PlacementAlgorithms - алгоритмы расстановки кораблей
"""

import random
from enum import Enum
from typing import List

from config import FIELD_SIZE, SHIPS, PlacementAlgorithm
from game_field import GameField
from ship import Ship


class PlacementPattern(Enum):
    """Паттерны размещения для алгоритма 1"""

    LEFT_VERTICAL = "left_vertical"
    RIGHT_VERTICAL = "right_vertical"
    TOP_HORIZONTAL = "top_horizontal"
    BOTTOM_HORIZONTAL = "bottom_horizontal"
    LEFT_VERTICAL_ALT = "left_vertical_alt"
    RIGHT_VERTICAL_ALT = "right_vertical_alt"
    TOP_HORIZONTAL_ALT = "top_horizontal_alt"
    BOTTOM_HORIZONTAL_ALT = "bottom_horizontal_alt"


class PlacementAlgorithms:
    """Алгоритмы расстановки кораблей"""

    @staticmethod
    def random_placement(field: GameField) -> List[Ship]:
        """
        Случайная расстановка кораблей

        Args:
            field: объект GameField

        Returns:
            list: список размещённых кораблей
        """
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
                    # Если не удалось разместить, начинаем заново
                    return PlacementAlgorithms.random_placement(field)

        return ships

    @staticmethod
    def algorithm1_placement(field: GameField) -> List[Ship]:
        """
        Алгоритм 1: Размещение кораблей по краям с большим свободным пространством

        Использует один из 8 паттернов размещения
        """
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
        Размещение по паттерну: линкор слева, корабли вертикально по левому краю
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

        # Первый эсминец слева (0, 5) вертикально
        ship2_1: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_1, 0, 5):
            ships.append(ship2_1)

        # Второй эсминец слева (0, 8) вертикально
        ship2_2: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_2, 0, 8):
            ships.append(ship2_2)

        # Третий эсминец справа (9, 8) вертикально
        ship2_3: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_3, 9, 8):
            ships.append(ship2_3)

        # Размещаем катера случайно в оставшемся пространстве
        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_right_vertical(field: GameField) -> List[Ship]:
        """Зеркальное отражение left_vertical по вертикали"""
        ships: List[Ship] = []

        # Линкор справа (9, 0) вертикально
        ship4: Ship = Ship(4, is_horizontal=False)
        if field.place_ship(ship4, 9, 0):
            ships.append(ship4)

        # Первый крейсер слева (0, 0) вертикально
        ship3_1: Ship = Ship(3, is_horizontal=False)
        if field.place_ship(ship3_1, 0, 0):
            ships.append(ship3_1)

        # Второй крейсер слева (0, 5) вертикально
        ship3_2: Ship = Ship(3, is_horizontal=False)
        if field.place_ship(ship3_2, 0, 4):
            ships.append(ship3_2)

        # Первый эсминец справа (9, 5) вертикально
        ship2_1: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_1, 9, 5):
            ships.append(ship2_1)

        # Второй эсминец справа (9, 8) вертикально
        ship2_2: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_2, 9, 8):
            ships.append(ship2_2)

        # Третий эсминец слева (0, 8) вертикально
        ship2_3: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_3, 0, 8):
            ships.append(ship2_3)

        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_top_horizontal(field: GameField) -> List[Ship]:
        """Транспонированная версия left_vertical: линкор сверху"""
        ships: List[Ship] = []

        # Линкор сверху (0, 0) горизонтально
        ship4: Ship = Ship(4, is_horizontal=True)
        if field.place_ship(ship4, 0, 0):
            ships.append(ship4)

        # Первый крейсер снизу (0, 9) горизонтально
        ship3_1: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_1, 0, 9):
            ships.append(ship3_1)

        # Второй крейсер снизу (5, 9) горизонтально
        ship3_2: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_2, 4, 9):
            ships.append(ship3_2)

        # Первый эсминец сверху (5, 0) горизонтально
        ship2_1: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_1, 5, 0):
            ships.append(ship2_1)

        # Второй эсминец сверху (8, 0) горизонтально
        ship2_2: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_2, 8, 0):
            ships.append(ship2_2)

        # Третий эсминец снизу (8, 9) горизонтально
        ship2_3: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_3, 8, 9):
            ships.append(ship2_3)

        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_bottom_horizontal(field: GameField) -> List[Ship]:
        """Линкор снизу"""
        ships: List[Ship] = []

        # Линкор снизу (0, 9) горизонтально
        ship4: Ship = Ship(4, is_horizontal=True)
        if field.place_ship(ship4, 0, 9):
            ships.append(ship4)

        # Первый крейсер сверху (0, 0) горизонтально
        ship3_1: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_1, 0, 0):
            ships.append(ship3_1)

        # Второй крейсер сверху (5, 0) горизонтально
        ship3_2: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_2, 4, 0):
            ships.append(ship3_2)

        # Первый эсминец снизу (5, 9) горизонтально
        ship2_1: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_1, 5, 9):
            ships.append(ship2_1)

        # Второй эсминец снизу (8, 9) горизонтально
        ship2_2: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_2, 8, 9):
            ships.append(ship2_2)

        # Третий эсминец сверху (8, 0) горизонтально
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

        # Линкор (0, 0) вертикально
        ship4: Ship = Ship(4, is_horizontal=False)
        if field.place_ship(ship4, 0, 0):
            ships.append(ship4)

        # Первый крейсер (2, 0) вертикально
        ship3_1: Ship = Ship(3, is_horizontal=False)
        if field.place_ship(ship3_1, 2, 0):
            ships.append(ship3_1)

        # Второй крейсер (2, 5) вертикально
        ship3_2: Ship = Ship(3, is_horizontal=False)
        if field.place_ship(ship3_2, 2, 4):
            ships.append(ship3_2)

        # Первый эсминец (0, 5) вертикально
        ship2_1: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_1, 0, 5):
            ships.append(ship2_1)

        # Второй эсминец (0, 8) вертикально
        ship2_2: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_2, 0, 8):
            ships.append(ship2_2)

        # Третий эсминец (2, 8) вертикально
        ship2_3: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_3, 2, 8):
            ships.append(ship2_3)

        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_right_vertical_alt(field: GameField) -> List[Ship]:
        """Зеркальное отражение left_vertical_alt"""
        ships: List[Ship] = []

        # Линкор (9, 0) вертикально
        ship4: Ship = Ship(4, is_horizontal=False)
        if field.place_ship(ship4, 9, 0):
            ships.append(ship4)

        # Первый крейсер (7, 0) вертикально
        ship3_1: Ship = Ship(3, is_horizontal=False)
        if field.place_ship(ship3_1, 7, 0):
            ships.append(ship3_1)

        # Второй крейсер (7, 5) вертикально
        ship3_2: Ship = Ship(3, is_horizontal=False)
        if field.place_ship(ship3_2, 7, 4):
            ships.append(ship3_2)

        # Первый эсминец (9, 5) вертикально
        ship2_1: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_1, 9, 5):
            ships.append(ship2_1)

        # Второй эсминец (9, 8) вертикально
        ship2_2: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_2, 9, 8):
            ships.append(ship2_2)

        # Третий эсминец (7, 8) вертикально
        ship2_3: Ship = Ship(2, is_horizontal=False)
        if field.place_ship(ship2_3, 7, 8):
            ships.append(ship2_3)

        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_top_horizontal_alt(field: GameField) -> List[Ship]:
        """Транспонированная версия left_vertical_alt"""
        ships: List[Ship] = []

        # Линкор (0, 0) горизонтально
        ship4: Ship = Ship(4, is_horizontal=True)
        if field.place_ship(ship4, 0, 0):
            ships.append(ship4)

        # Первый крейсер (0, 2) горизонтально
        ship3_1: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_1, 0, 2):
            ships.append(ship3_1)

        # Второй крейсер (5, 2) горизонтально
        ship3_2: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_2, 4, 2):
            ships.append(ship3_2)

        # Первый эсминец (5, 0) горизонтально
        ship2_1: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_1, 5, 0):
            ships.append(ship2_1)

        # Второй эсминец (8, 0) горизонтально
        ship2_2: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_2, 8, 0):
            ships.append(ship2_2)

        # Третий эсминец (8, 2) горизонтально
        ship2_3: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_3, 8, 2):
            ships.append(ship2_3)

        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_bottom_horizontal_alt(field: GameField) -> List[Ship]:
        """Транспонированная версия с линкором снизу"""
        ships: List[Ship] = []

        # Линкор (0, 9) горизонтально
        ship4: Ship = Ship(4, is_horizontal=True)
        if field.place_ship(ship4, 0, 9):
            ships.append(ship4)

        # Первый крейсер (0, 7) горизонтально
        ship3_1: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_1, 0, 7):
            ships.append(ship3_1)

        # Второй крейсер (5, 7) горизонтально
        ship3_2: Ship = Ship(3, is_horizontal=True)
        if field.place_ship(ship3_2, 4, 7):
            ships.append(ship3_2)

        # Первый эсминец (5, 9) горизонтально
        ship2_1: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_1, 5, 9):
            ships.append(ship2_1)

        # Второй эсминец (8, 9) горизонтально
        ship2_2: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_2, 8, 9):
            ships.append(ship2_2)

        # Третий эсминец (8, 7) горизонтально
        ship2_3: Ship = Ship(2, is_horizontal=True)
        if field.place_ship(ship2_3, 8, 7):
            ships.append(ship2_3)

        ships.extend(PlacementAlgorithms._place_remaining_ships(field, 1, 4))

        return ships

    @staticmethod
    def _place_remaining_ships(field: GameField, size: int, count: int) -> List[Ship]:
        """
        Размещает оставшиеся корабли случайно

        Args:
            field: игровое поле
            size: размер кораблей
            count: количество кораблей

        Returns:
            список размещённых кораблей
        """
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

        return ships

    @staticmethod
    def place_ships(field: GameField, algorithm_type: PlacementAlgorithm) -> List[Ship]:
        """
        Размещает корабли по указанному алгоритму

        Args:
            field: объект GameField
            algorithm_type: тип алгоритма

        Returns:
            list: список размещённых кораблей
        """
        if algorithm_type == PlacementAlgorithm.RANDOM:
            return PlacementAlgorithms.random_placement(field)
        elif algorithm_type == PlacementAlgorithm.ALGORITHM_1:
            return PlacementAlgorithms.algorithm1_placement(field)
        else:
            return PlacementAlgorithms.random_placement(field)
