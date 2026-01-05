from typing import List, Optional, Tuple


class Ship:
    def __init__(
        self,
        size: int,
        x: Optional[int] = None,
        y: Optional[int] = None,
        is_horizontal: bool = True,
    ) -> None:
        """
        Args:
            size: размер корабля (1-4)
            x, y: координаты начала корабля
            is_horizontal: ориентация (True - горизонтально, False - вертикально)
        """
        self.size: int = size
        self.x: Optional[int] = x
        self.y: Optional[int] = y
        self.is_horizontal: bool = is_horizontal
        self.hits: int = 0

    def get_coordinates(self) -> List[Tuple[int, int]]:
        """Возвращает список координат, занимаемых кораблём"""
        if self.x is None or self.y is None:
            return []

        coords: List[Tuple[int, int]] = []
        for i in range(self.size):
            if self.is_horizontal:
                coords.append((self.x + i, self.y))
            else:
                coords.append((self.x, self.y + i))
        return coords

    def rotate(self) -> None:
        """Поворачивает корабль"""
        self.is_horizontal = not self.is_horizontal

    def is_destroyed(self) -> bool:
        """Проверяет, уничтожен ли корабль"""
        return self.hits >= self.size

    def hit(self) -> None:
        """Регистрирует попадание в корабль"""
        if self.hits < self.size:
            self.hits += 1

    def reset_hits(self) -> None:
        """Сбрасывает количество попаданий"""
        self.hits = 0

    def __repr__(self) -> str:
        orientation: str = "H" if self.is_horizontal else "V"
        return f"Ship(size={self.size}, pos=({self.x},{self.y}), {orientation}, hits={self.hits})"
