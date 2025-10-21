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

def test_bear_off_move(monkeypatch, mock_pygame):
    """Test bearing off a checker."""
    monkeypatch.setattr('backgammon.pygame_ui.ui.pygame', mock_pygame)
    ui = PygameUI()
    game = ui.game
    player = game.get_current_player() # Assume it's White

    # 1. Setup the board for bear-off: all checkers in the home board.
    # We'll place one checker on point 23 (index 22) and the rest elsewhere in home.
    game.board.points = [[] for _ in range(24)] # Clear the board
    player_checkers = player.get_checkers()
    game.board.place_checker(player_checkers[0], 22) # Point 23
    for i in range(1, 15):
        game.board.place_checker(player_checkers[i], 18 + (i % 5)) # Other home points

    # 2. Set dice to a roll that allows bearing off from point 23 (e.g., a 2 or more).
    # White moves from high to low, but direction is positive. home_points: 18-23. Entry -1.
    # A roll of 2 from point 23 (index 22) means 22 + 2 = 24, which is off.
    game.dice.set_values((2, 1))
    ui.possible_moves = game.board.enumerar_opciones_legales(player, ui._get_current_dice())

    # 3. Simulate the player's actions:
    # - First click: select the checker on point 23.
    monkeypatch.setattr(ui, '_get_point_from_pos', lambda pos: 22)
    ui._handle_click((200, 200)) # Position doesn't matter

    # Check that the source is selected and 'bear_off' is a possible destination
    assert ui.selected_source == 22
    assert 'bear_off' in ui.possible_dests

    # - Second click: click on the bear-off area.
    monkeypatch.setattr(ui, '_get_point_from_pos', lambda pos: None) # Click is not on a point
    # Mock the bear_off_rects to return a mock rect that will register the click
    mock_bear_off_rect = Mock()
    mock_bear_off_rect.collidepoint.return_value = True
    ui.bear_off_rects[player.get_color()] = mock_bear_off_rect
    # We also need to mock _get_bear_off_from_pos to return 'bear_off'
    monkeypatch.setattr(ui, '_get_bear_off_from_pos', lambda pos: 'bear_off')
    ui._handle_click((1300, 100)) # A position in the new bear-off area

    # 4. Assert the game state has changed as expected:
    # - The checker is no longer on the board.
    assert player_checkers[0] not in game.board.points[22]
    # - The checker is in the borne_off list.
    assert player_checkers[0] in game.board.get_borne_off(player.get_color())
    # - The used dice includes 2.
    assert 2 in ui.used_dice
    # - The selection state is reset.
    assert ui.selected_source is None

def test_game_over_detection(monkeypatch, mock_pygame):
    """Test that the UI detects the game over state correctly."""
    monkeypatch.setattr('backgammon.pygame_ui.ui.pygame', mock_pygame)
    ui = PygameUI()
    game = ui.game
    player = game.get_current_player()

    # 1. Setup a game state where the current player has won
    # (all their checkers are in borne_off).
    for checker in player.get_checkers():
        game.board.bear_off_checker(checker)

    # 2. Mock the is_game_over method to return True
    # In a real scenario, this would be based on the board state.
    # The game logic is tested elsewhere, here we ensure the UI reacts to it.
    monkeypatch.setattr(game, 'is_game_over', lambda: True)

    # 3. Call _end_turn(), which should trigger the game over logic.
    ui._end_turn()

    # 4. Assert that the UI has entered the game over state.
    assert ui.game_over is True
    assert ui.winner == player
    assert ui.game_over_time is not None
