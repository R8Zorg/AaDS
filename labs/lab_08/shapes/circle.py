import math


class Circle:
    def __init__(self, x: int, y: int, r: int, color: str):
        self._x: int = x
        self._y: int = y
        self._r: int = r
        self._color: str = color

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def get_r(self) -> int:
        return self._r

    def get_color(self) -> str:
        return self._color

    def get_position(self) -> tuple[int, int]:
        return self._x, self._y

    def set_position(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def contains(self, other: "Circle") -> bool:
        distance = math.hypot(self.x - other.x, self.y - other.y)
        return distance + other.r <= self.r
