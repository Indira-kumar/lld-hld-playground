from .registry import ObserverRegistry
from .observer import Observer

class Publisher(ObserverRegistry):
    def __init__(self):
        self.observers = []
    def add_observer(self, observer: Observer) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: Observer) -> None:
        self.observers.remove(observer)

    def notify_observers(self, stock_name, price) -> None:
        for observer in self.observers:
            observer.send_notification(stock_name, price)