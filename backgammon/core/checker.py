from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from backgammon.core.player import Player


class Checker:
    """
    A class used to represent a Backgammon checker (ficha).

    ...

    Attributes
    ----------
    color : str
        The color of the checker ("blancas" or "negras")
    owner : Optional["Player"]
        The player who owns the checker (optional)
    posicion : Optional[int]
        The position index on the board (0..23) if on board, None otherwise
    en_barra : bool
        Whether the checker is on the bar
    fuera : bool
        Whether the checker has been borne off (removed from board)
    id : Optional[str]
        Optional identifier for the checker

    Methods
    -------
    en_tablero()
        Returns True if the checker is on the board (position 0..23)
    en_barra()
        Returns True if the checker is on the bar
    fuera()
        Returns True if the checker has been borne off
    get_posicion()
        Returns the position index if on board, None otherwise
    get_color()
        Returns the color of the checker
    get_owner()
        Returns the owner of the checker
    colocar_en_posicion(posicion)
        Places the checker at a given board position
    mover_a(posicion)
        Moves the checker to another board position
    enviar_a_barra()
        Sends the checker to the bar
    sacar()
        Marks the checker as borne off
    resetear()
        Resets the checker state for a new game
    """

    def __init__(
        self,
        color: str,
        player: Optional["Player"] = None,
        posicion: Optional[int] = None,
        identificador: Optional[str] = None,
    ) -> None:
        """
        Crea la ficha.
        - color: "blancas" o "negras".
        - owner: referencia al Player dueño (opcional).
        - posicion: índice 0..23 si está en el tablero; None si no aplica.
        - identificador: id opcional para distinguir fichas.
        """
        self._color = color
        self._player = player
        self._posicion = posicion  # 0..23 si está en tablero, None si no aplica
        self._en_barra = False
        self._fuera = False
        self._id = identificador

    # ------------------------
    # Consultas de estado
    # ------------------------
    def en_tablero(self) -> bool:
        """Devuelve True si la ficha está sobre una posición 0..23."""
        return self._posicion is not None and not self._en_barra and not self._fuera

    def en_barra(self) -> bool:
        """Devuelve True si la ficha está en la barra."""
        return self._en_barra

    def fuera(self) -> bool:
        """Devuelve True si la ficha ya fue retirada del tablero (bear off)."""
        return self._fuera

    def get_posicion(self) -> Optional[int]:
        """Devuelve la posición (0..23) si está en tablero; None si no aplica."""
        return self._posicion if self.en_tablero() else None

    def get_color(self) -> str:
        """Devuelve el color de la ficha."""
        return self._color

    def get_owner(self) -> Optional["Player"]:
        """Devuelve el jugador dueño de la ficha (si fue asignado)."""
        return self._player

    # ------------------------
    # Cambios de estado (sin validar reglas)
    # Estas acciones normalmente las orquesta Game/Board.
    # ------------------------
    def colocar_en_posicion(self, posicion: int) -> None:
        """Coloca la ficha en una posición 0..23 (sin validar reglas)."""
        self._posicion = posicion
        self._en_barra = False
        self._fuera = False

    def mover_a(self, posicion: int) -> None:
        """Mueve la ficha a otra posición 0..23 (sin validar reglas)."""
        self.colocar_en_posicion(posicion)

    def enviar_a_barra(self) -> None:
        """Envía la ficha a la barra."""
        self._posicion = None
        self._en_barra = True
        self._fuera = False

    def sacar(self) -> None:
        """Marca la ficha como 'fuera' (bear off)."""
        self._posicion = None
        self._en_barra = False
        self._fuera = True

    # ------------------------
    # Utilidades
    # ------------------------
    def resetear(self) -> None:
        """Resetea estado (por ejemplo, para nueva partida)."""
        self._posicion = None
        self._en_barra = False
        self._fuera = False

    def __str__(self) -> str:
        """Texto amigable (color, estado)."""
        estado = (
            "fuera"
            if self._fuera
            else (
                "barra"
                if self._en_barra
                else (
                    f"pos {self._posicion + 1}"
                    if self._posicion is not None
                    else "sin posición"
                )
            )
        )
        return f"Checker({self._color}, {estado})"

    def __repr__(self) -> str:
        """Texto técnico para debugging."""
        return f"Checker(color={self._color}, owner={self._player}, posicion={self._posicion}, barra={self._en_barra}, fuera={self._fuera}, id={self._id})"
