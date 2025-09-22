from backgammon.core.board import Board
from backgammon.core.dice import Dice


def test_import_board_and_dice():
    assert Board is not None
    assert Dice is not None


def test_dice_initialization():
    """Testea la inicialización de los dados."""
    dice = Dice()
    # Los valores iniciales deben ser 1
    assert dice.dice1 == 1
    assert dice.dice2 == 1
    assert dice.get_values() == (1, 1)


def test_dice_roll_changes_values():
    """Testea que el método roll cambia los valores y estén en el rango 1..6."""
    dice = Dice()
    for _ in range(10):
        val1, val2 = dice.roll()
        assert 1 <= val1 <= 6
        assert 1 <= val2 <= 6
        # Los valores internos deben coincidir con lo retornado
        assert dice.get_values() == (val1, val2)


def test_dice_get_values_consistency():
    """Testea que get_values retorna los valores actuales de los dados."""
    dice = Dice()
    dice.dice1 = 4
    dice.dice2 = 5
    assert dice.get_values() == (4, 5)
