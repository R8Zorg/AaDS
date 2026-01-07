from typing import Dict, List, Optional, Tuple

from attack_algorithms import AttackAlgorithms
from config import SHIPS, AttackAlgorithm, CellState, PlacementAlgorithm
from game_field import GameField
from placement_algorithms import PlacementAlgorithms
from ship import Ship


class GameLogic:
    def __init__(self) -> None:
        self.player_field: GameField = GameField()
        self.bot_field: GameField = GameField()
        self.player_turn: bool = True
        self.game_started: bool = False
        self.game_over: bool = False
        self.winner: Optional[str] = None

        self.show_enemy_ships: bool = False
        self.highlight_surrounding: bool = False
        self.bot_placement_algorithm: PlacementAlgorithm = PlacementAlgorithm.RANDOM
        self.bot_attack_algorithm: Optional[AttackAlgorithms] = None

        self.player_ships_to_place: List[Ship] = []
        self._init_player_ships()

    def _init_player_ships(self) -> None:
        self.player_ships_to_place = []
        for size, count in SHIPS.items():
            for _ in range(count):
                self.player_ships_to_place.append(Ship(size))

    def reset_game(self) -> None:
        self.player_field.reset()
        self.bot_field.reset()
        self.player_turn = True
        self.game_started = False
        self.game_over = False
        self.winner = None
        self._init_player_ships()
        self.bot_attack_algorithm = None

    def start_game(self, attack_algorithm_type: AttackAlgorithm) -> bool:
        if not self.all_player_ships_placed():
            return False

        PlacementAlgorithms.place_ships(self.bot_field, self.bot_placement_algorithm)

        self.bot_attack_algorithm = AttackAlgorithms(attack_algorithm_type)

        self.game_started = True
        self.player_turn = True

        return True

    def all_player_ships_placed(self) -> bool:
        return len(self.player_field.ships) == sum(SHIPS.values())

    def place_player_ship(self, ship: Ship, x: int, y: int) -> bool:
        return self.player_field.place_ship(ship, x, y)

    def remove_player_ship(self, ship: Ship) -> None:
        self.player_field.remove_ship(ship)

    def auto_place_player_ships(self, algorithm_type: PlacementAlgorithm) -> None:
        self.player_field.reset()
        self.player_ships_to_place = []
        self.player_ships_to_place = PlacementAlgorithms.place_ships(
            self.player_field, algorithm_type
        )

    def player_attack(self, x: int, y: int) -> Optional[CellState]:
        if not self.game_started or not self.player_turn:
            return None

        result: Optional[CellState] = self.bot_field.attack(x, y)

        if not result:
            return None

        if result == CellState.MISS:
            self.player_turn = False
        elif self.bot_field.is_all_ships_destroyed():
            self.game_over = True
            self.winner = "player"

        return result

    def bot_attack(self) -> Optional[Tuple[Tuple[int, int], Optional[CellState]]]:
        if not self.game_started or self.game_over or self.player_turn:
            return None

        if self.bot_attack_algorithm is None:
            return None

        coords: Optional[Tuple[int, int]] = self.bot_attack_algorithm.get_next_attack(
            self.player_field
        )

        if coords is None:
            return None

        x, y = coords
        result: Optional[CellState] = self.player_field.attack(x, y)

        self.bot_attack_algorithm.process_attack_result(x, y, result, self.player_field)

        if result == CellState.MISS:
            self.player_turn = True

        if self.player_field.is_all_ships_destroyed():
            self.game_over = True
            self.winner = "bot"

        return ((x, y), result)

    def get_player_stats(self) -> Dict[str, int]:
        return self.player_field.get_stats()

    def get_bot_stats(self) -> Dict[str, int]:
        return self.bot_field.get_stats()

    def set_bot_placement_algorithm(self, algorithm_type: PlacementAlgorithm) -> None:
        self.bot_placement_algorithm = algorithm_type
