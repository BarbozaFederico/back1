import pytest
from backgammon.core.backgammon import BackgammonGame


def get_player_configs():
    return [
        {
            "id": "P1",
            "nombre": "Blanco",
            "color": "blancas",
            "direccion": 1,
            "home_points": [18, 19, 20, 21, 22, 23],
            "entry_point": 0,
        },
        {
            "id": "P2",
            "nombre": "Negro",
            "color": "negras",
            "direccion": -1,
            "home_points": [0, 1, 2, 3, 4, 5],
            "entry_point": 23,
        },
    ]


def test_game_initialization():
    """Testea la inicialización básica del juego."""
    game = BackgammonGame()
    assert game.board is not None
    assert game.players == []
    assert game.dice is not None
    assert game.current_player_idx == 0
    assert game.started is False


def test_setup_players():
    """Testea la configuración de jugadores y fichas."""
    game = BackgammonGame()
    configs = get_player_configs()
    game.setup_players(configs)
    assert len(game.players) == 2
    for player, cfg in zip(game.players, configs):
        assert player.get_id() == cfg["id"]
        assert player.get_color() == cfg["color"]
        assert len(player.get_checkers()) == 15
        # Check owner assignment
        for checker in player.get_checkers():
            assert checker.get_owner() == player


def test_start_game_positions():
    """Testea el inicio del juego y la colocación inicial de fichas."""
    game = BackgammonGame()
    game.setup_players(get_player_configs())
    game.start_game()
    # Verifica que las fichas estén en las posiciones iniciales
    blancos = game.players[0].get_checkers()
    negras = game.players[1].get_checkers()
    # Blancas: 2 en 0, 5 en 11, 3 en 16, 5 en 18
    assert sum(1 for c in blancos if c.get_posicion() == 0) == 2
    assert sum(1 for c in blancos if c.get_posicion() == 11) == 5
    assert sum(1 for c in blancos if c.get_posicion() == 16) == 3
    assert sum(1 for c in blancos if c.get_posicion() == 18) == 5
    # Negras: 2 en 23, 5 en 12, 3 en 7, 5 en 5
    assert sum(1 for c in negras if c.get_posicion() == 23) == 2
    assert sum(1 for c in negras if c.get_posicion() == 12) == 5
    assert sum(1 for c in negras if c.get_posicion() == 7) == 3
    assert sum(1 for c in negras if c.get_posicion() == 5) == 5


def test_next_turn_and_get_current_player():
    """Testea el avance de turnos y obtención del jugador actual."""
    game = BackgammonGame()
    game.setup_players(get_player_configs())
    assert game.get_current_player().get_id() == "P1"
    game.next_turn()
    assert game.get_current_player().get_id() == "P2"
    game.next_turn()
    assert game.get_current_player().get_id() == "P1"


def test_roll_dice_and_cli_display(capsys):
    """Testea el lanzamiento de dados y la visualización CLI."""
    game = BackgammonGame()
    game.setup_players(get_player_configs())
    vals = game.roll_dice()
    assert isinstance(vals, tuple)
    assert len(vals) == 2
    assert all(1 <= v <= 6 for v in vals)
    game.cli_display()
    captured = capsys.readouterr()
    assert "Turno de:" in captured.out
    assert "Dados:" in captured.out
    assert "Tablero:" in captured.out


def test_is_game_over_false_true():
    """Testea la detección de fin de partida."""
    game = BackgammonGame()
    game.setup_players(get_player_configs())
    assert not game.is_game_over()
    # Simula que un jugador tiene todas las fichas fuera
    player = game.players[0]
    for checker in player.get_checkers():
        checker.sacar()
    assert game.is_game_over()
