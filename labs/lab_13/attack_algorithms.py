"""
Класс AttackAlgorithms - алгоритмы атаки бота
"""

import random
from typing import Optional, List, Tuple

from config import FIELD_SIZE, SHIPS, CellState, AttackAlgorithm
from game_field import GameField


class AttackAlgorithms:
    """Алгоритмы атаки бота"""
    
    def __init__(self, algorithm_type: AttackAlgorithm) -> None:
        """
        Инициализация алгоритма атаки
        
        Args:
            algorithm_type: тип алгоритма
        """
        self.algorithm_type: AttackAlgorithm = algorithm_type
        self.mode: str = "search"  # "search" или "hunt"
        self.target_ship: List[Tuple[int, int]] = []
        self.potential_targets: List[Tuple[int, int]] = []
        self.ship_orientation: Optional[str] = None  # "horizontal" или "vertical"
        self.current_search_size: int = 4
        self.found_ship_sizes: List[int] = []
        
        # Для алгоритма 2
        self.priority_zones: List[Tuple[int, int, int]] = self._init_priority_zones()
        self.heat_map: List[List[int]] = [[0 for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]
    
    def _init_priority_zones(self) -> List[Tuple[int, int, int]]:
        """Инициализация приоритетных зон для алгоритма 2"""
        zones: List[Tuple[int, int, int]] = []
        for x in range(3, 7):
            for y in range(3, 7):
                zones.append((x, y, 3))
        
        for x in range(2, 8):
            for y in range(2, 8):
                if not any(z[0] == x and z[1] == y for z in zones):
                    zones.append((x, y, 2))
        
        return zones
    
    def get_next_attack(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        """
        Возвращает координаты следующей атаки
        
        Args:
            player_field: объект GameField игрока
            
        Returns:
            tuple: (x, y) координаты атаки или None
        """
        if self.algorithm_type == AttackAlgorithm.RANDOM:
            return self._random_attack(player_field)
        elif self.algorithm_type == AttackAlgorithm.ALGORITHM_1:
            return self._algorithm1_attack(player_field)
        elif self.algorithm_type == AttackAlgorithm.ALGORITHM_2:
            return self._algorithm2_attack(player_field)
        else:
            return self._random_attack(player_field)
    
    def _random_attack(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        """Случайная атака"""
        available: List[Tuple[int, int]] = []
        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                if player_field.field[y][x] not in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
                    available.append((x, y))
        
        return random.choice(available) if available else None
    
    def _algorithm1_attack(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        """
        Алгоритм 1: Поиск и охота
        
        Режим поиска: ищет корабли по паттерну в зависимости от размера
        Режим охоты: добивает найденный корабль
        """
        if self.mode == "hunt" and self.potential_targets:
            return self._hunt_mode(player_field)
        else:
            return self._search_mode(player_field)
    
    def _search_mode(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        """Режим поиска - ищет корабли по паттерну"""
        # Определяем текущий размер для поиска
        if len([s for s in self.found_ship_sizes if s == 4]) == 0:
            search_size: int = 4
        elif len([s for s in self.found_ship_sizes if s == 3]) < 2:
            search_size = 3
        elif len([s for s in self.found_ship_sizes if s == 2]) < 3:
            search_size = 2
        else:
            search_size = 1
        
        # Ищем клетки по формуле
        candidates: List[Tuple[int, int]] = []
        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                if player_field.field[y][x] not in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
                    if (x + y + 1) % search_size == 0:
                        candidates.append((x, y))
        
        if candidates:
            return random.choice(candidates)
        
        # Если нет кандидатов по паттерну, атакуем случайно
        return self._random_attack(player_field)
    
    def _hunt_mode(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        """Режим охоты - добивает найденный корабль"""
        if not self.potential_targets:
            self.mode = "search"
            return self._search_mode(player_field)
        
        # Берём первую доступную цель
        target: Tuple[int, int] = self.potential_targets.pop(0)
        
        # Проверяем, что цель доступна
        if player_field.field[target[1]][target[0]] in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
            return self._hunt_mode(player_field)
        
        return target
    
    def _algorithm2_attack(self, player_field: GameField) -> Optional[Tuple[int, int]]:
        """
        Алгоритм 2: Атака с использованием тепловой карты
        
        Учитывает вероятность расположения кораблей
        """
        if self.mode == "hunt" and self.potential_targets:
            return self._hunt_mode(player_field)
        
        # Обновляем тепловую карту
        self._update_heat_map(player_field)
        
        # Находим клетку с максимальным "теплом"
        max_heat: int = -1
        best_targets: List[Tuple[int, int]] = []
        
        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                if player_field.field[y][x] not in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
                    heat: int = self.heat_map[y][x]
                    if heat > max_heat:
                        max_heat = heat
                        best_targets = [(x, y)]
                    elif heat == max_heat:
                        best_targets.append((x, y))
        
        return random.choice(best_targets) if best_targets else None
    
    def _update_heat_map(self, player_field: GameField) -> None:
        """Обновляет тепловую карту для алгоритма 2"""
        # Сбрасываем карту
        self.heat_map = [[0 for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]
        
        # Добавляем базовые приоритеты
        for x, y, priority in self.priority_zones:
            if player_field.field[y][x] not in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
                self.heat_map[y][x] = priority
        
        # Увеличиваем "тепло" вокруг попаданий
        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                if player_field.field[y][x] == CellState.HIT:
                    # Увеличиваем приоритет соседних клеток
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < FIELD_SIZE and 0 <= ny < FIELD_SIZE:
                            if player_field.field[ny][nx] not in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
                                self.heat_map[ny][nx] += 10
        
        # Увеличиваем приоритет клеток, где могут поместиться корабли
        for size in [4, 3, 2, 1]:
            if len([s for s in self.found_ship_sizes if s == size]) < SHIPS[size]:
                self._add_ship_possibilities(player_field, size)
    
    def _add_ship_possibilities(self, player_field: GameField, size: int) -> None:
        """Добавляет вероятность для размещения корабля указанного размера"""
        for y in range(FIELD_SIZE):
            for x in range(FIELD_SIZE):
                # Горизонтально
                can_fit_h: bool = True
                if x + size <= FIELD_SIZE:
                    for i in range(size):
                        if player_field.field[y][x + i] in [CellState.DESTROYED, CellState.MISS]:
                            can_fit_h = False
                            break
                    if can_fit_h:
                        for i in range(size):
                            if player_field.field[y][x + i] not in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
                                self.heat_map[y][x + i] += 1
                
                # Вертикально
                can_fit_v: bool = True
                if y + size <= FIELD_SIZE:
                    for i in range(size):
                        if player_field.field[y + i][x] in [CellState.DESTROYED, CellState.MISS]:
                            can_fit_v = False
                            break
                    if can_fit_v:
                        for i in range(size):
                            if player_field.field[y + i][x] not in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
                                self.heat_map[y + i][x] += 1
    
    def process_attack_result(self, x: int, y: int, result: str, player_field: GameField) -> None:
        """
        Обрабатывает результат атаки
        
        Args:
            x, y: координаты атаки
            result: результат ("miss", "hit", "destroyed")
            player_field: игровое поле игрока
        """
        if result == "hit":
            # Переходим в режим охоты
            self.mode = "hunt"
            self.target_ship.append((x, y))
            
            # Определяем ориентацию корабля
            if len(self.target_ship) == 1:
                # Первое попадание - добавляем все 4 соседние клетки
                self.potential_targets = []
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < FIELD_SIZE and 0 <= ny < FIELD_SIZE:
                        if player_field.field[ny][nx] not in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
                            self.potential_targets.append((nx, ny))
            else:
                # Определяем ориентацию
                if self.target_ship[0][0] == self.target_ship[1][0]:
                    self.ship_orientation = "vertical"
                else:
                    self.ship_orientation = "horizontal"
                
                # Обновляем список целей с учётом ориентации
                self._update_targets_by_orientation(x, y, player_field)
        
        elif result == "destroyed":
            # Корабль уничтожен - возвращаемся в режим поиска
            if len(self.target_ship) > 0:
                ship_size: int = len(self.target_ship) + 1
                self.found_ship_sizes.append(ship_size)
            
            self.mode = "search"
            self.target_ship = []
            self.potential_targets = []
            self.ship_orientation = None
    
    def _update_targets_by_orientation(self, x: int, y: int, player_field: GameField) -> None:
        """Обновляет список целей с учётом ориентации корабля"""
        self.potential_targets = []
        
        if self.ship_orientation == "horizontal":
            # Ищем края корабля по горизонтали
            min_x: int = min(coord[0] for coord in self.target_ship)
            max_x: int = max(coord[0] for coord in self.target_ship)
            
            # Добавляем клетки слева и справа
            if min_x > 0 and player_field.field[y][min_x - 1] not in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
                self.potential_targets.append((min_x - 1, y))
            if max_x < FIELD_SIZE - 1 and player_field.field[y][max_x + 1] not in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
                self.potential_targets.append((max_x + 1, y))
        
        elif self.ship_orientation == "vertical":
            # Ищем края корабля по вертикали
            min_y: int = min(coord[1] for coord in self.target_ship)
            max_y: int = max(coord[1] for coord in self.target_ship)
            
            # Добавляем клетки сверху и снизу
            if min_y > 0 and player_field.field[min_y - 1][x] not in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
                self.potential_targets.append((x, min_y - 1))
            if max_y < FIELD_SIZE - 1 and player_field.field[max_y + 1][x] not in [CellState.HIT, CellState.DESTROYED, CellState.MISS]:
                self.potential_targets.append((x, max_y + 1))
