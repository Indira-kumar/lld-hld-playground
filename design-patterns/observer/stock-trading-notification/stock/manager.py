from .observer import *
from .publisher import Publisher

class StockTradingManager(Publisher):
    def __init__(
        self, stock_name: str, initial_price: float, notification_threshold: float
    ):
        super().__init__()
        self.stock_name = stock_name
        self.current_price = initial_price
        self.notification_threshold = notification_threshold
        self.add_observer(EmailService())
        self.add_observer(SmsService())
        self.add_observer(AppService())

    def update_stock_price(self, new_price: float) -> None:
        self.current_price = new_price
        if self.current_price > self.notification_threshold:
            self.notify_observers(self.stock_name, new_price)