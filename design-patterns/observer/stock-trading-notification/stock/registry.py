from abc import ABC, abstractmethod

from .observer import Observer


class ObserverRegistry(ABC):
    @abstractmethod
    def add_observer(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def remove_observer(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify_observers(self, name, price) -> None:
        pass
