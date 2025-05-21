from interfaces.base_circle import BaseShape


class Circle(BaseShape):
    def __init__(self, color: float, size: float):
        self.color: float = color
        self.size: float = size
        self.x: float = 0
        self.y: float = 0

    def get_color(self) -> str:
        return self.color

    def get_size(self) -> float:
        """Get radius"""
        return self.size

    def get_position(self) -> tuple[float, float]:
        return self.x, self.y

    def set_color(self, color: str) -> None:
        self.color = color

    def set_size(self, r: float) -> None:
        """Set radius"""
        self.size = r

    def set_position(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
