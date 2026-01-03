from orientation import Orientation


class Ship:
    def __init__(
        self,
        length: int,
        cells: list[tuple[int, int]] | None = None,
        orientation: Orientation = Orientation.H,
    ) -> None:
        self.length = length
        self.orientation = orientation
        self.cells = list(cells) if cells else []
        self.hits: set[tuple[int, int]] = set()

    def occupies(self, x, y) -> bool:
        return (x, y) in self.cells

    def is_sunk(self) -> bool:
        return len(self.hits) >= self.length

    def register_hit(self, x, y) -> None:
        if (x, y) in self.cells:
            self.hits.add((x, y))
