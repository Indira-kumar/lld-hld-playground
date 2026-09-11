import unittest
from unittest.mock import MagicMock

from stock import *


class TestObserver(unittest.TestCase):
    def test_send_notification_method_exists(self):
        self.assertTrue(
            hasattr(Observer, "send_notification"),
            "If the Observer pattern is implemented correctly, it should have a send_notification method.",
        )

    def test_concrete_classes_inherit_and_implement_send_notification(self):
        concrete_classes = [AppService, EmailService, SmsService]
        for cls in concrete_classes:
            self.assertTrue(
                issubclass(cls, Observer),
                f"If the {cls.__name__} class is a concrete observer, it should inherit from the Observer class.",
            )
            self.assertTrue(
                hasattr(cls, "send_notification"),
                f"If the {cls.__name__} class is a concrete observer, it should implement the send_notification method.",
            )


class TestPublisher(unittest.TestCase):
    def test_parent_class(self):
        self.assertTrue(
            issubclass(Publisher, ObserverRegistry),
            "If the Observer pattern is implemented correctly, the Publisher class should inherit from the ObserverRegistry class.",
        )

    def test_methods(self):
        methods = ["add_observer", "remove_observer", "notify_observers"]
        for method in methods:
            self.assertTrue(
                hasattr(Publisher, method),
                f"If the Observer pattern is implemented correctly, the Publisher class should have a {method} method.",
            )


class TestStockTradingManager(unittest.TestCase):
    def setUp(self):
        # Create a mock observer
        self.observer_mock = MagicMock(spec=Observer)

        # Create a stock trading manager
        self.stock_manager = StockTradingManager(
            stock_name="ABC", initial_price=100.0, notification_threshold=150.0
        )

    def test_inherits_from_publisher(self):
        self.assertTrue(
            issubclass(StockTradingManager, Publisher),
            "If the Observer pattern is implemented correctly, the StockTradingManager class should inherit from the Publisher class.",
        )

    def test_add_observer(self):
        # Add the observer to the manager
        try:
            self.stock_manager.add_observer(self.observer_mock)
        except AttributeError as e:
            self.fail(
                f"If the manager is implemented correctly, it should inherit the add_observer method from the Publisher class. {e}"
            )

        # Assert that the observer is added to the observers list
        self.assertIn(
            self.observer_mock,
            self.stock_manager.observers,
            "If the observer is added to the manager, it should be in the observers list.",
        )

    def test_remove_observer(self):
        # Add the observer to the manager
        self.stock_manager.observers = [self.observer_mock]

        # Remove the observer from the manager
        try:
            self.stock_manager.remove_observer(self.observer_mock)
        except AttributeError as e:
            self.fail(
                f"If the manager is implemented correctly, it should inherit the remove_observer method from the Publisher class. {e}"
            )

        # Assert that the observer is removed from the observers list
        self.assertNotIn(
            self.observer_mock,
            self.stock_manager.observers,
            "If the observer is removed from the manager, it should not be in the observers list.",
        )

    def test_update_stock_price_notifies_observers_above_threshold(self):
        # Add the observer to the manager
        self.stock_manager.observers = [self.observer_mock]

        # Update the stock price to trigger notification
        self.stock_manager.update_stock_price(200.0)

        # Assert that the observer's send_notification method was called
        try:
            self.observer_mock.send_notification.assert_called_once_with("ABC", 200.0)
        except AttributeError as e:
            self.fail(
                f"If the observer is implemented correctly, it should have a send_notification method. {e}"
            )

    def test_update_stock_price_does_not_notify_observers_below_threshold(self):
        # Add the observer to the manager
        self.stock_manager.observers = [self.observer_mock]

        # Update the stock price below the notification threshold
        self.stock_manager.update_stock_price(100.0)

        # Assert that the observer's send_notification method was not called
        try:
            self.observer_mock.send_notification.assert_not_called()
        except AttributeError as e:
            self.fail(
                f"If the observer is implemented correctly, it should have a send_notification method. {e}"
            )


if __name__ == "__main__":
    unittest.main()
