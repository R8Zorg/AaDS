import random
from typing import List

from config import FIELD_SIZE, SHIPS, PlacementAlgorithm
from game_field import GameField
from ship import Ship


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

        transpose = random.choice([True, False])
        mirror = random.choice([True, False])
        mirror_axis = random.choice(["x", "y"]) if mirror else None

        ships: List[Ship] = []

        """
        Расстановка 1:
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

        Расстановка 2:
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
        # size, x, y, is_horizontal
        base_ships1: list[tuple[int, int, int, bool]] = [
            (4, 0, 0, False),
            (3, 9, 0, False),
            (3, 9, 4, False),
            (2, 0, 5, False),
            (2, 0, 8, False),
            (2, 9, 8, False),
        ]
        base_ships2: list[tuple[int, int, int, bool]] = [
            (4, 0, 0, False),
            (3, 2, 0, False),
            (3, 2, 4, False),
            (2, 0, 5, False),
            (2, 0, 8, False),
            (2, 2, 8, False),
        ]
        base_ships = random.choice([base_ships1, base_ships2])

        for size, x, y, is_horizontal in base_ships:
            if transpose:
                x, y = y, x
                is_horizontal = not is_horizontal

            if mirror:
                if mirror_axis == "x":
                    x = FIELD_SIZE - 1 - x
                    if is_horizontal and size > 1:
                        x = x - (size - 1)
                else:
                    y = FIELD_SIZE - 1 - y
                    if not is_horizontal and size > 1:
                        y = y - (size - 1)

            ship = Ship(size, is_horizontal=is_horizontal)
            if not field.place_ship(ship, x, y):
                continue

            ships.append(ship)

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
