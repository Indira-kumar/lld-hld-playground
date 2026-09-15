from abc import ABC, abstractmethod
from random import randint

class DiceStrategy(ABC):

    @abstractmethod
    def roll_dice() -> int:
        raise NotImplementedError()


class DefaultDiceStrategy(DiceStrategy):
    def roll_dice() -> int:
        return randint(1, 12)