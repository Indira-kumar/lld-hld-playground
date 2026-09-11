from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def send_notification(self, stock_name: str , current_price: float) -> None:
        raise NotImplementedError()


class AppService(Observer):
    def send_push(self, stock_name: str, current_price: float) -> None:
        subject = "Price update for " + stock_name
        message = "New price is " + str(current_price)
        print(f"App notification: {subject} - {message}")
    
    def send_notification(self, stock_name: str, current_price: float) -> None:
        self.send_push(stock_name, current_price)


class EmailService(Observer):
    def send_email(self, stock_name: str, current_price: float) -> None:
        subject = "Price update for " + stock_name
        message = "New price is " + str(current_price)
        print(f"Email notification: {subject} - {message}")

    def send_notification(self, stock_name: str, current_price: float) -> None:
        self.send_email(stock_name, current_price)


class SmsService(Observer):
    def send_sms(self, stock_name: str, current_price: float) -> None:
        subject = "Price update for " + stock_name
        message = "New price is " + str(current_price)
        print(f"SMS notification: {subject} - {message}")

    def send_notification(self, stock_name: str, current_price: float) -> None:
        self.send_sms(stock_name, current_price)