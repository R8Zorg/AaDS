from board import Board
from orientation import Orientation
import random

DEFAULT_SHIPS = {4: 1, 3: 2, 2: 3, 1: 4}


def auto_place_random_greedy(
    board: Board, ships_spec=DEFAULT_SHIPS, max_global_attempts=200
):
    """
    Алгоритм A: случайный greedy.
    Для каждого корабля пробуем рандомные позиции, если не получается в лимите - рестарт.
    """
    lengths = []
    for length, count in ships_spec.items():
        lengths.extend([length] * count)
    lengths.sort(reverse=True)
    for attempt in range(max_global_attempts):
        board.reset()
        success = True
        for length in lengths:
            placed = False
            tries = 0
            while tries < 1000 and not placed:
                orientation = random.choice([Orientation.H, Orientation.V])
                x = random.randint(0, board.size - 1)
                y = random.randint(0, board.size - 1)
                if board.place_ship(x, y, orientation, length):
                    placed = True
                tries += 1
            if not placed:
                success = False
                break
        if success:
            return True
    return False


def generate_candidate_positions_pattern(board: Board, length):
    """
    Генерация кандидатов по шаблону: краевые/угловые приоритеты.
    Возвращаем список (x,y,orientation) смешанный.
    """
    candidates = []
    size = board.size
    # edges and corners prioritized
    idxs = list(range(size))
    # try corners first
    corners = [(0, 0), (size - 1, 0), (0, size - 1), (size - 1, size - 1)]
    for cx, cy in corners:
        for ori in (Orientation.H, Orientation.V):
            candidates.append((cx, cy, ori))
    # then edges
    for i in idxs:
        for ori in (Orientation.H, Orientation.V):
            candidates.append((i, 0, ori))
            candidates.append((i, size - 1, ori))
            candidates.append((0, i, ori))
            candidates.append((size - 1, i, ori))
    # then others
    for y in idxs:
        for x in idxs:
            for ori in (Orientation.H, Orientation.V):
                candidates.append((x, y, ori))
    # remove duplicates and shuffle but keep some randomness
    unique = list(dict.fromkeys(candidates))
    random.shuffle(unique)
    return unique


def auto_place_patterned(
    board: Board, ships_spec=DEFAULT_SHIPS, max_global_attempts=200
):
    """
    Алгоритм B: шаблон + случайность.
    Для каждого корабля генерируем кандидатов по шаблону и берём первую подходящую.
    При провале - рестарт.
    """
    lengths = []
    for length, count in ships_spec.items():
        lengths.extend([length] * count)
    lengths.sort(reverse=True)
    for attempt in range(max_global_attempts):
        board.reset()
        success = True
        for length in lengths:
            candidates = generate_candidate_positions_pattern(board, length)
            placed = False
            for x, y, ori in candidates:
                if board.can_place_ship(x, y, ori, length):
                    board.place_ship(x, y, ori, length)
                    placed = True
                    break
            if not placed:
                success = False
                break
        if success:
            return True
    return False
