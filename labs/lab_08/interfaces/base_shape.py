from abc import ABC, abstractmethod


class BaseShape(ABC):
    @abstractmethod
    def get_color(self) -> str:
        pass

    @abstractmethod
    def set_color(self, color: str) -> None:
        pass

    @abstractmethod
    def get_size(self) -> float:
        pass

    @abstractmethod
    def set_size(self, size: float) -> None:
        pass

    @abstractmethod
    def get_position(self) -> tuple[float, float]:
        pass

    @abstractmethod
    def set_position(self, x: float, y: float) -> None:
        pass
