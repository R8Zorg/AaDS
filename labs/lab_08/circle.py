import math


class Circle:
    def __init__(self, x: int, y: int, r: int, color: str, id):
        self._x: int = x
        self._y: int = y
        self._r: int = r
        self._color: str = color
        self._id = id

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def get_r(self) -> int:
        return self._r

    def get_color(self) -> str:
        return self._color

    def set_color(self, color: str):
        self._color = color

    def get_position(self) -> tuple[int, int]:
        return self._x, self._y

    def set_position(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    @staticmethod
    def contains(circle1: "Circle", circle2: "Circle") -> bool:
        dist = math.hypot(
            circle1.get_x() - circle2.get_x(), circle1.get_y() - circle2.get_y()
        )

        r1 = circle1.get_r()
        r2 = circle2.get_r()
        if dist + min(r1, r2) <= max(r1, r2):
            return True
        elif dist <= r1 + r2:
            return True
        else:
            return False
