"""
Конфигурация и константы для игры Морской бой
"""

from enum import Enum, auto
from typing import Dict

# Размеры поля
FIELD_SIZE: int = 10


class CellState(Enum):
    """Состояния клеток игрового поля"""
    EMPTY = 0
    SHIP = 1
    HIT = 2
    DESTROYED = 3
    MISS = 4


class Colors(Enum):
    """Цветовая палитра приложения"""
    EMPTY = "#E8F4F8"
    SHIP = "#4A90E2"
    HIT = "#FF6B6B"
    DESTROYED = "#8B0000"
    MISS = "#B0BEC5"
    HOVER = "#FFE082"
    SELECTED = "#FFA726"
    GRAY_MARK = "#CCCCCC"
    BG = "#F5F5F5"
    MENU_BG = "#FFFFFF"
    BTN_PRIMARY = "#4CAF50"
    BTN_SECONDARY = "#2196F3"
    BTN_DANGER = "#F44336"
    BTN_DISABLED = "#BDBDBD"
    BTN_READY = "#81C784"


class GUISize(Enum):
    """Размеры элементов GUI"""
    CELL_SIZE = 35
    PADDING = 20
    MENU_WIDTH = 280
    STATS_HEIGHT = 60
    BUTTON_HEIGHT = 40


class PlacementAlgorithm(Enum):
    """Типы алгоритмов расстановки кораблей"""
    RANDOM = "random"
    ALGORITHM_1 = "algorithm1"


class AttackAlgorithm(Enum):
    """Типы алгоритмов атаки"""
    RANDOM = "random"
    ALGORITHM_1 = "algorithm1"
    ALGORITHM_2 = "algorithm2"


# Корабли (размер: количество)
SHIPS: Dict[int, int] = {
    4: 1,  # Линкор
    3: 2,  # Крейсер
    2: 3,  # Эсминец
    1: 4   # Катер
}
