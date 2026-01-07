from enum import Enum
from typing import Dict

FIELD_SIZE: int = 10


class CellState(Enum):
    EMPTY = 0
    SHIP = 1
    HIT = 2
    DESTROYED = 3
    MISS = 4
    NO_SHIP = 5


class Colors(Enum):
    EMPTY = "#E8F4F8"
    SHIP = "#4A90E2"
    HIT = "#F0AB54"
    DESTROYED = "#EA4A4A"
    MISS = "#B0BEC5"
    HOVER = "#FFE082"
    SELECTED = "#FFA726"
    BLACK_MARK = "#000000"
    BG = "#F5F5F5"
    MENU_BG = "#FFFFFF"
    BTN_PRIMARY = "#4CAF50"
    BTN_SECONDARY = "#2196F3"
    BTN_DANGER = "#F44336"
    BTN_DISABLED = "#BDBDBD"
    BTN_READY = "#81C784"
    LINE = "#CCCCCC"
    INVALID = "#FF5252"
    FOREGROUND = "#666666"


class GUISize(Enum):
    CELL_SIZE = 35
    PADDING = 20
    MENU_WIDTH = 280
    STATS_HEIGHT = 60
    BUTTON_HEIGHT = 40


class PlacementAlgorithm(Enum):
    RANDOM = "random"
    ALGORITHM = "algorithm"


class AttackAlgorithm(Enum):
    RANDOM = "random"
    ALGORITHM_1 = "algorithm1"
    ALGORITHM_2 = "algorithm2"


# размер: количество
SHIPS: Dict[int, int] = {
    4: 1,
    3: 2,
    2: 3,
    1: 4,
}
