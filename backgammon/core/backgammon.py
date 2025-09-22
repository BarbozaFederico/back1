from typing import List, Optional
from backgammon.core.player import Player
from backgammon.core.checker import Checker
from backgammon.core.dice import Dice
from backgammon.core.board import Board


class BackgammonGame:
    """
    A class used to represent a Backgammon game session.

    ...

    Attributes
    ----------
    board : Board
        The Backgammon board instance.
    players : List[Player]
        List of Player objects participating in the game.
    dice : Dice
        Dice object used for rolling moves.
    current_player_idx : int
        Index of the player whose turn it is.
    started : bool
        Indicates if the game has started.

    Methods
    -------
    setup_players(player_configs)
        Initializes players and their checkers.
    start_game()
        Starts the game and sets up initial positions.
    next_turn()
        Advances to the next player's turn.
    get_current_player()
        Returns the current Player object.
    roll_dice()
        Rolls the dice and returns their values.
    cli_display()
        Prints the current game state for CLI.
    is_game_over()
        Checks if the game has ended.
    """

    def __init__(self) -> None:
        """
        Initializes the Backgammon game with an empty board, dice, and no players.

        Parameters
        ----------
        None
        """
        self.board = Board()
        self.players: List[Player] = []
        self.dice = Dice()
        self.current_player_idx: int = 0
        self.started: bool = False

    def setup_players(self, player_configs: List[dict]) -> None:
        """
        Initializes players and their checkers based on configuration.

        Parameters
        ----------
        player_configs : List[dict]
            List of dicts with keys: id, nombre, color, direccion, home_points, entry_point

        Examples
        --------
        game.setup_players([
            {"id": "P1", "nombre": "Blanco", "color": "blancas", ...},
            {"id": "P2", "nombre": "Negro", "color": "negras", ...}
        ])
        """
        self.players = []
        for cfg in player_configs:
            checkers = [Checker(cfg["color"], None) for _ in range(15)]
            player = Player(
                player_id=cfg["id"],
                nombre=cfg["nombre"],
                color=cfg["color"],
                direccion=cfg["direccion"],
                home_points=cfg["home_points"],
                entry_point=cfg["entry_point"],
                checkers=checkers,
                politica=None,
            )
            self.players.append(player)
            self.board.add_player(player)
        # Optionally assign owner to checkers
        for player in self.players:
            for checker in player.get_checkers():
                checker._player = player  # direct assignment for owner reference

    def start_game(self) -> None:
        """
        Starts the game and sets up initial positions for all checkers.

        Returns
        -------
        None
        """
        self.started = True
        # Example initial positions (standard Backgammon setup)
        # This can be customized per rules
        setup = [
            (0, "blancas", 2),
            (11, "blancas", 5),
            (16, "blancas", 3),
            (18, "blancas", 5),
            (23, "negras", 2),
            (12, "negras", 5),
            (7, "negras", 3),
            (5, "negras", 5),
        ]
        for player in self.players:
            color = player.get_color()
            placed = 0
            for point, c, count in setup:
                if c == color:
                    for i in range(count):
                        checker = player.get_checkers()[placed]
                        self.board.place_checker(checker, point)
                        placed += 1

    def next_turn(self) -> None:
        """
        Advances to the next player's turn.

        Returns
        -------
        None
        """
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def get_current_player(self) -> Player:
        """
        Returns the current Player object.

        Returns
        -------
        Player
        """
        return self.players[self.current_player_idx]

    def roll_dice(self) -> tuple[int, int]:
        """
        Rolls the dice and returns their values.

        Returns
        -------
        tuple[int, int]
            Values of die1 and die2.
        """
        return self.dice.roll()

    def cli_display(self) -> None:
        """
        Prints the current game state for CLI.

        Returns
        -------
        None
        """
        print(
            f"Turno de: {self.get_current_player().get_nombre()} ({self.get_current_player().get_color()})"
        )
        print(f"Dados: {self.dice.get_values()}")
        self.board.display()

    def is_game_over(self) -> bool:
        """
        Checks if the game has ended (all checkers borne off for any player).

        Returns
        -------
        bool
        """
        for player in self.players:
            if len(player.checkers_fuera()) == 15:
                return True
        return False
