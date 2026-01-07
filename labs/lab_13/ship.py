from typing import List, Optional, Tuple


class Ship:
    def __init__(
        self,
        size: int,
        x: Optional[int] = None,
        y: Optional[int] = None,
        is_horizontal: bool = True,
    ) -> None:
        self.size: int = size
        self.x: Optional[int] = x
        self.y: Optional[int] = y
        self.is_horizontal: bool = is_horizontal
        self.hits: int = 0

    def get_coordinates(self) -> List[Tuple[int, int]]:
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
        self.is_horizontal = not self.is_horizontal

    def is_destroyed(self) -> bool:
        return self.hits >= self.size

    def hit(self) -> None:
        if self.hits >= self.size:
            return

        self.hits += 1

    def reset_hits(self) -> None:
        self.hits = 0
