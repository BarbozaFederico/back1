import pytest
from unittest.mock import Mock, MagicMock
from backgammon.pygame_ui.ui import PygameUI
from backgammon.core.backgammon import BackgammonGame

@pytest.fixture
def mock_pygame():
    """Mock pygame to avoid display initialization."""
    pygame = Mock()
    pygame.Rect.return_value = MagicMock()
    return pygame

def test_move_from_bar(monkeypatch, mock_pygame):
    """Test moving a checker from the bar to the board."""
    # Mock pygame to avoid display initialization
    monkeypatch.setattr('backgammon.pygame_ui.ui.pygame', mock_pygame)

    # Initialize UI
    ui = PygameUI()
    game = ui.game
    player = game.get_current_player()
    opponent_color = "negras" if player.get_color() == "blancas" else "blancas"

    # 1. Setup the board:
    # - Place one of the current player's checkers on the bar.
    # - Place an opponent's checker on point 23 to be "captured".
    # - Clear point 2, so it's a valid destination.
    checker_to_bar = player.get_checkers()[0]
    game.board.send_to_bar(checker_to_bar)

    opponent_checker = next(p.get_checkers()[0] for p in game.players if p.get_color() == opponent_color)
    game.board.place_checker(opponent_checker, 23)

    game.board.points[2] = [] # Ensure point 3 (index 2) is open

    # 2. Set dice to a specific roll (e.g., 3) that allows re-entry.
    # White player's entry is -1. So -1 + 3 = 2, which is point 3.
    game.dice.set_values((3, 4))
    ui.possible_moves = game.board.enumerar_opciones_legales(player, ui._get_current_dice())

    # 3. Simulate the player's actions:
    # - First click: on the bar to select the checker.
    # The bar's rect for the current player is needed. Let's assume a click is within it.
    ui.bar_rects[player.get_color()] = Mock(collidepoint=lambda pos: True)
    ui._handle_click((0, 0)) # Position doesn't matter due to mocking

    # Check that the bar is now selected
    assert ui.selected_source == 'bar'
    assert 2 in ui.possible_dests # Destination for die '3'

    # - Second click: on the destination point (point 3, which is index 2).
    # We need to mock _get_point_from_pos to return the correct point index.
    monkeypatch.setattr(ui, '_get_point_from_pos', lambda pos: 2)
    ui._handle_click((100, 100)) # Position doesn't matter

    # 4. Assert the game state has changed as expected:
    # - The checker is no longer on the bar.
    assert not game.board.jugador_tiene_en_barra(player)
    # - The checker is on point 3 (index 2).
    assert any(c == checker_to_bar for c in game.board.points[2])
    # - The used dice includes 3.
    assert 3 in ui.used_dice
    # - The selection state is reset.
    assert ui.selected_source is None
    assert not ui.possible_dests
