import random

from board import Board
from cell_state import CellState

GRID_SIZE = 10


class BotAI:
    def __init__(self, board_size: int = GRID_SIZE, mode: str = "RANDOM") -> None:
        self.size = board_size
        self.mode = mode
        self.reset()

    def reset(self) -> None:
        self.shots: set[tuple[int, int]] = set()
        self.target_queue: list[tuple[int, int]] = []
        self.last_hit_stack = []

    def next_shot(self, enemy_board: Board):
        if self.mode == "RANDOM":
            return self.random_shot()
        else:
            return self.hunt_target_shot(enemy_board)

    def random_shot(self) -> tuple[int, int] | None:
        choices: list[tuple[int, int]] = [
            (x, y)
            for x in range(self.size)
            for y in range(self.size)
            if (x, y) not in self.shots
        ]
        if not choices:
            return None
        target: tuple[int, int] = random.choice(choices)
        self.shots.add(target)
        return target

    def hunt_target_shot(self, enemy_board: Board) -> tuple[int, int] | None:
        while self.target_queue:
            tx, ty = self.target_queue.pop(0)
            if (tx, ty) in self.shots:
                continue
            if 0 <= tx < self.size and 0 <= ty < self.size:
                self.shots.add((tx, ty))
                return (tx, ty)

        choices = []
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) in self.shots:
                    continue

                if (x + y) % 2 == 0:
                    choices.append((x, y))
        if not choices:
            for y in range(self.size):
                for x in range(self.size):
                    if (x, y) not in self.shots:
                        choices.append((x, y))
        if not choices:
            return None
        target = random.choice(choices)
        self.shots.add(target)
        return target

    def inform_result(self, x: int, y: int, result: CellState, ship=None):
        """
        Передавать результат выстрела боту, чтобы он мог корректно добавлять цели.
        result: 'miss', 'hit', 'sunk'
        """
        if result == CellState.MISS:
            return
        if result == CellState.HIT:
            neighbors = [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]
            for nx, ny in neighbors:
                if (
                    (nx, ny) not in self.shots
                    and 0 <= nx < self.size
                    and 0 <= ny < self.size
                ):
                    if (nx, ny) not in self.target_queue:
                        self.target_queue.append((nx, ny))
        if result == CellState.SUNK:
            self.target_queue = []
