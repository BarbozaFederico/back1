from backgammon.core.backgammon import BackgammonGame
from backgammon.core.player import OpcionMovimiento, SecuenciaMovimiento


class BackgammonCLI:
    """
    A class used to run a 2-player Backgammon game in the command line interface (CLI).

    ...

    Attributes
    ----------
    game : BackgammonGame
        Instance of the BackgammonGame logic.

    Methods
    -------
    run()
        Starts and runs the CLI game loop.
    prompt_move(player, opciones)
        Prompts the user to select a legal move.
    """

    def __init__(self) -> None:
        """
        Initializes the CLI with a BackgammonGame instance.

        Parameters
        ----------
        None
        """
        self.game = BackgammonGame()

    def run(self) -> None:
        """
        Starts and runs the CLI game loop for 2 players.

        Returns
        -------
        None
        """
        print("Bienvenido a Backgammon CLI!")
        # Configuración de jugadores
        player_configs = [
            {
                "id": "P1",
                "nombre": input("Nombre jugador 1 (blancas): ") or "Blanco",
                "color": "blancas",
                "direccion": 1,
                "home_points": [18, 19, 20, 21, 22, 23],
                "entry_point": 0,
            },
            {
                "id": "P2",
                "nombre": input("Nombre jugador 2 (negras): ") or "Negro",
                "color": "negras",
                "direccion": -1,
                "home_points": [0, 1, 2, 3, 4, 5],
                "entry_point": 23,
            },
        ]
        self.game.setup_players(player_configs)  # <-- Inicializa fichas
        self.game.start_game()

        while not self.game.is_game_over():
            self.game.cli_display()
            input("Presiona ENTER para lanzar los dados...")
            dados = self.game.roll_dice()
            print(f"Dados lanzados: {dados}")

            player = self.game.get_current_player()
            opciones = player.movimientos_legales(self.game.board, dados)
            if not opciones:
                print("No hay movimientos legales disponibles. Turno perdido.")
            else:
                print(f"{player.get_nombre()}, selecciona tu movimiento:")
                for idx, opcion in enumerate(opciones):
                    pasos = [
                        f"{'Barra' if paso.desde is None else paso.desde+1} -> "
                        f"{'Fuera' if paso.hasta is None else paso.hasta+1} (Dado: {paso.dado})"
                        + (" [Captura]" if paso.captura else "")
                        for paso in opcion.secuencia
                    ]
                    print(f"{idx+1}: {' | '.join(pasos)}")
                seleccion = self.prompt_move(player, len(opciones))
                secuencia = opciones[seleccion - 1].secuencia
                player.confirmar_movimiento(self.game.board, secuencia)
                print("Movimiento aplicado.")

            input("Presiona ENTER para finalizar tu turno...")
            self.game.next_turn()

        print("¡Fin de la partida!")
        for player in self.game.players:
            if len(player.checkers_fuera()) == 15:
                print(f"Ganador: {player.get_nombre()} ({player.get_color()})")

    def prompt_move(self, player, num_opciones: int) -> int:
        """
        Prompts the user to select a legal move.

        Parameters
        ----------
        player : Player
        num_opciones : int

        Returns
        -------
        int
            Index (1-based) of the selected move.
        """
        while True:
            try:
                seleccion = int(
                    input(f"Ingrese el número de movimiento (1-{num_opciones}): ")
                )
                if 1 <= seleccion <= num_opciones:
                    return seleccion
                else:
                    print("Selección inválida. Intente nuevamente.")
            except ValueError:
                print("Entrada inválida. Ingrese un número.")


if __name__ == "__main__":
    cli = BackgammonCLI()
    cli.run()
