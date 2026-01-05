from typing import Dict, List, Optional, Tuple

from attack_algorithms import AttackAlgorithms
from config import SHIPS, AttackAlgorithm, PlacementAlgorithm
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
        self.highlight_adjacent: bool = True
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
        """Сброс игры"""
        self.player_field.reset()
        self.bot_field.reset()
        self.player_turn = True
        self.game_started = False
        self.game_over = False
        self.winner = None
        self._init_player_ships()
        self.bot_attack_algorithm = None

    def start_game(self, attack_algorithm_type: AttackAlgorithm) -> bool:
        """
        Начинает игру

        Args:
            attack_algorithm_type: тип алгоритма атаки бота

        Returns:
            bool: True если игра началась успешно
        """
        if not self.all_player_ships_placed():
            return False

        # Расставляем корабли бота
        PlacementAlgorithms.place_ships(self.bot_field, self.bot_placement_algorithm)

        # Инициализируем алгоритм атаки бота
        self.bot_attack_algorithm = AttackAlgorithms(attack_algorithm_type)

        self.game_started = True
        self.player_turn = True

        return True

    def all_player_ships_placed(self) -> bool:
        return len(self.player_field.ships) == sum(SHIPS.values())

    def place_player_ship(self, ship: Ship, x: int, y: int) -> bool:
        """
        Размещает корабль игрока

        Args:
            ship: объект Ship
            x, y: координаты

        Returns:
            bool: успешно ли размещён корабль
        """
        return self.player_field.place_ship(ship, x, y)

    def remove_player_ship(self, ship: Ship) -> None:
        """Удаляет корабль игрока с поля"""
        self.player_field.remove_ship(ship)

    def auto_place_player_ships(self, algorithm_type: PlacementAlgorithm) -> None:
        """
        Автоматически расставляет корабли игрока

        Args:
            algorithm_type: тип алгоритма размещения
        """
        self.player_field.reset()
        self.player_ships_to_place = []
        ships: List[Ship] = PlacementAlgorithms.place_ships(
            self.player_field, algorithm_type
        )
        # Добавляем корабли в список для отслеживания
        self.player_ships_to_place = ships

    def player_attack(self, x: int, y: int) -> str:
        """
        Игрок атакует бота

        Args:
            x, y: координаты атаки

        Returns:
            str: результат атаки
        """
        if not self.game_started or self.game_over or not self.player_turn:
            return "invalid"

        result: str = self.bot_field.attack(x, y)

        if result == "already_attacked":
            return result

        # Если промах, ход переходит к боту
        if result == "miss":
            self.player_turn = False

        # Проверяем победу
        if self.bot_field.is_all_ships_destroyed():
            self.game_over = True
            self.winner = "player"

        return result

    def bot_attack(self) -> Optional[Tuple[Tuple[int, int], str]]:
        """
        Бот атакует игрока

        Returns:
            tuple: ((x, y), result) координаты и результат атаки или None
        """
        if not self.game_started or self.game_over or self.player_turn:
            return None

        if self.bot_attack_algorithm is None:
            return None

        # Получаем координаты атаки от алгоритма
        coords: Optional[Tuple[int, int]] = self.bot_attack_algorithm.get_next_attack(
            self.player_field
        )

        if coords is None:
            return None

        x, y = coords
        result: str = self.player_field.attack(x, y)

        # Сообщаем алгоритму о результате
        self.bot_attack_algorithm.process_attack_result(x, y, result, self.player_field)

        # Если промах, ход переходит к игроку
        if result == "miss":
            self.player_turn = True

        # Проверяем победу
        if self.player_field.is_all_ships_destroyed():
            self.game_over = True
            self.winner = "bot"

        return ((x, y), result)

    def get_player_stats(self) -> Dict[str, int]:
        """Возвращает статистику игрока"""
        return self.player_field.get_stats()

    def get_bot_stats(self) -> Dict[str, int]:
        """Возвращает статистику бота"""
        return self.bot_field.get_stats()

    def set_bot_placement_algorithm(self, algorithm_type: PlacementAlgorithm) -> None:
        """Устанавливает алгоритм расстановки кораблей бота"""
        self.bot_placement_algorithm = algorithm_type
