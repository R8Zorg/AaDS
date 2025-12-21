from enum import Enum


class CellState(Enum):
    EMPTY = 0
    SHIP = 1
    HIT = 2
    SUNK = 3
    MISS = 4
