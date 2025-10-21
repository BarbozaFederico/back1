import random


class Dice:
    """
    A class used to represent two dice for Backgammon.

    Attributes
    ----------
    die1 : int
        Value of the first die (1..6)
    die2 : int
        Value of the second die (1..6)

    Methods
    -------
    roll()
        Rolls both dice and updates their values.
    get_values()
        Returns the current values of both dice.
    """

    def __init__(self) -> None:
        """Inicializa ambos dados con un valor de 1."""
        self.dice1 = 1
        self.dice2 = 1

    def roll(self) -> tuple[int, int]:
        """Lanza ambos dados y actualiza sus valores con números aleatorios entre 1 y 6.

        Returns
        -------
        tuple[int, int]
            Una tupla con los valores de ambos dados después del lanzamiento.
        """
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        return (self.dice1, self.dice2)

    def get_values(self) -> tuple[int, int]:
        """Devuelve los valores actuales de ambos dados.

        Returns
        -------
        tuple[int, int]
            Una tupla con los valores actuales de ambos dados.
        """
        return (self.dice1, self.dice2)

    def set_values(self, values: tuple[int, int]) -> None:
        """
        Sets the values of the dice for testing purposes.

        Parameters
        ----------
        values : tuple[int, int]
            The values to set for the dice.
        """
        self.dice1, self.dice2 = values
