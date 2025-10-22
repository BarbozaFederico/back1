from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Optional, List, Iterable, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from backgammon.core.checker import Checker

ValorDado = int  # 1..6


@dataclass(frozen=True)
class PasoMovimiento:
    """
    Qué recibe:
      - desde: índice 0..23 o None si entra desde barra.
      - hasta: índice 0..23 o None si es bear-off (fuera).
      - dado: valor del dado usado (1..6).
      - captura: True si captura una ficha rival.

    Qué hace: representa un paso individual de movimiento.
    Qué devuelve: contenedor inmutable.
    """

    desde: Optional[int]
    hasta: Optional[int]
    dado: ValorDado
    captura: bool = False


SecuenciaMovimiento = List[PasoMovimiento]


@dataclass(frozen=True)
class OpcionMovimiento:
    """
    Qué recibe:
      - secuencia: pasos válidos (1..4).
      - hash_tablero: firma/hash del estado simulado.
      - puntaje: heurística para ranking (mayor = mejor).

    Qué hace: encapsula una jugada completa válida.
    Qué devuelve: contenedor inmutable.
    """

    secuencia: SecuenciaMovimiento
    hash_tablero: str
    puntaje: float = 0.0


class TableroFachada(Protocol):
    """
    Contrato mínimo que Player necesita de Board.
    La implementación concreta vive en core/board.py.
    """

    def jugador_tiene_en_barra(self, jugador: "Player") -> bool: ...
    def jugador_todo_en_home(self, jugador: "Player") -> bool: ...
    def oponente_en_cuadrante(self, jugador: "Player") -> bool: ...
    def jugador_pip_count(self, jugador: "Player") -> int: ...
    def enumerar_opciones_legales(
        self, jugador: "Player", dados: Sequence[ValorDado]
    ) -> List[OpcionMovimiento]: ...

    def aplicar_movimiento(
        self, jugador: "Player", secuencia: SecuenciaMovimiento
    ) -> None: ...


class Politica(Protocol):
    """
    Estrategia de selección de jugada.
    Útil para Humano/CPU; Player no depende de UI.
    """

    def elegir(
        self, opciones: List[OpcionMovimiento]
    ) -> Optional[SecuenciaMovimiento]: ...


class PoliticaNula:
    """
    Política por defecto: no decide.
    Qué recibe: lista de opciones legales.
    Qué hace: no elige nada (delega a UI/Game).
    Qué devuelve: None.
    """

    def elegir(self, opciones: List[OpcionMovimiento]) -> Optional[SecuenciaMovimiento]:
        return None


class Player:
    """
    A class used to represent a Backgammon player.

    ...

    Attributes
    ----------
    __id__ : str
        Logical identifier for the player (e.g., "P1")
    __nombre__ : str
        Display name of the player
    __color__ : str
        Color of the player's checkers ("blancas" or "negras")
    __direccion__ : int
        Direction of movement (+1 or -1)
    __home_points__ : frozenset[int]
        Set of board indices (0..23) that form the player's home
    __entry_point__ : int
        Entry point index for re-entering from the bar
    __checkers__ : list[Checker]
        List of Checker objects owned by the player
    __politica__ : Politica
        Strategy for move selection

    Methods
    -------
    get_id()
        Returns the logical identifier of the player
    get_nombre()
        Returns the display name of the player
    get_color()
        Returns the color of the player's checkers
    get_direccion()
        Returns the direction of movement (+1 or -1)
    get_home_points()
        Returns the set of home point indices
    get_entry_point()
        Returns the entry point index
    get_checkers()
        Returns a defensive copy of the player's checkers
    tiene_en_barra(tablero)
        Returns True if the player has checkers on the bar
    todas_en_home(tablero)
        Returns True if all checkers are in the home area
    pip_count(tablero)
        Returns the pip count for the player
    movimientos_legales(tablero, dados)
        Returns a list of legal move options for the player
    elegir_movimiento(opciones)
        Selects a move sequence from available options using the player's strategy
    confirmar_movimiento(tablero, secuencia)
        Applies a move sequence to the board
    puede_bear_off(tablero)
        Returns True if the player can bear off checkers
    colocar_checker_en_posicion(checker, posicion)
        Places a checker at a given board position
    mover_checker_a(checker, posicion)
        Moves a checker to another board position
    enviar_checker_a_barra(checker)
        Sends a checker to the bar
    sacar_checker(checker)
        Marks a checker as borne off
    checkers_en_tablero()
        Returns a list of checkers currently on the board
    checkers_en_barra()
        Returns a list of checkers currently on the bar
    checkers_fuera()
        Returns a list of checkers that have been borne off
    __str__()
        Returns a friendly string representation of the player
    __repr__()
        Returns a technical string representation for debugging
    """

    __slots__ = (
        "__id__",
        "__nombre__",
        "__color__",
        "__direccion__",
        "__home_points__",
        "__entry_point__",
        "__checkers__",
        "__politica__",
    )

    def __init__(
        self,
        player_id: str,
        nombre: str,
        color: str,
        direccion: int,
        home_points: Iterable[int],
        entry_point: int,
        checkers: Iterable["Checker"],
        politica: Optional[Politica] = None,
    ) -> None:
        """
        Parameters
        ----------
        player_id : str
            Logical identifier for the player (e.g., "P1")
        nombre : str
            Display name of the player
        color : str
            Color of the player's checkers ("blancas" or "negras")
        direccion : int
            Direction of movement (+1 or -1)
        home_points : Iterable[int]
            Indices (0..23) forming the player's home area
        entry_point : int
            Entry point index for re-entering from the bar
        checkers : Iterable[Checker]
            Iterable of Checker objects owned by the player
        politica : Optional[Politica], optional
            Strategy for move selection (default is PoliticaNula)
        """
        self.__id__ = player_id
        self.__nombre__ = nombre
        self.__color__ = color
        self.__direccion__ = 1 if direccion >= 0 else -1
        self.__home_points__ = frozenset(int(p) for p in home_points)
        self.__entry_point__ = int(entry_point)
        self.__checkers__ = list(checkers)
        self.__politica__ = politica if politica is not None else PoliticaNula()

    def get_id(self) -> str:
        """
        Returns the logical identifier of the player.

        Returns
        -------
        str
            The player's logical identifier
        """
        return self.__id__

    def get_nombre(self) -> str:
        """
        Returns the display name of the player.

        Returns
        -------
        str
            The player's display name
        """
        return self.__nombre__

    def get_color(self) -> str:
        """
        Returns the color of the player's checkers.

        Returns
        -------
        str
            The color ("blancas" or "negras")
        """
        return self.__color__

    def get_direccion(self) -> int:
        """
        Returns the direction of movement (+1 or -1).

        Returns
        -------
        int
            The direction of movement
        """
        return self.__direccion__

    def get_home_points(self) -> frozenset[int]:
        """
        Returns the set of home point indices.

        Returns
        -------
        frozenset[int]
            Indices forming the player's home area
        """
        return self.__home_points__

    def get_entry_point(self) -> int:
        """
        Returns the entry point index.

        Returns
        -------
        int
            The entry point index for re-entering from the bar
        """
        return self.__entry_point__

    def get_checkers(self) -> List["Checker"]:
        """
        Returns a defensive copy of the player's checkers.

        Returns
        -------
        list[Checker]
            List of Checker objects
        """
        return list(self.__checkers__)  # copia defensiva

    def tiene_en_barra(self, tablero: TableroFachada) -> bool:
        """
        Returns True if the player has checkers on the bar.

        Parameters
        ----------
        tablero : TableroFachada
            Board facade implementing required methods

        Returns
        -------
        bool
            True if any checker is on the bar
        """
        return tablero.jugador_tiene_en_barra(self)

    def todas_en_home(self, tablero: TableroFachada) -> bool:
        """
        Returns True if all checkers are in the home area.

        Parameters
        ----------
        tablero : TableroFachada

        Returns
        -------
        bool
        """
        return tablero.jugador_todo_en_home(self)

    def pip_count(self, tablero: TableroFachada) -> int:
        """
        Returns the pip count for the player.

        Parameters
        ----------
        tablero : TableroFachada

        Returns
        -------
        int
        """
        return tablero.jugador_pip_count(self)

    def movimientos_legales(
        self, tablero: TableroFachada, dados: Sequence[ValorDado]
    ) -> List[OpcionMovimiento]:
        """
        Returns a list of legal move options for the player.

        Parameters
        ----------
        tablero : TableroFachada
        dados : Sequence[ValorDado]

        Returns
        -------
        list[OpcionMovimiento]
        """
        return tablero.enumerar_opciones_legales(self, dados)

    def elegir_movimiento(
        self, opciones: List[OpcionMovimiento]
    ) -> Optional[SecuenciaMovimiento]:
        """
        Selects a move sequence from available options using the player's strategy.

        Parameters
        ----------
        opciones : list[OpcionMovimiento]

        Returns
        -------
        Optional[SecuenciaMovimiento]
        """
        if not opciones:
            return None
        return self.__politica__.elegir(opciones)

    def confirmar_movimiento(
        self, tablero: TableroFachada, secuencia: SecuenciaMovimiento
    ) -> None:
        """
        Applies a move sequence to the board.

        Parameters
        ----------
        tablero : TableroFachada
        secuencia : SecuenciaMovimiento
        """
        tablero.aplicar_movimiento(self, secuencia)

    def puede_bear_off(self, tablero: TableroFachada) -> bool:
        """
        Returns True if the player can bear off checkers.

        Parameters
        ----------
        tablero : TableroFachada

        Returns
        -------
        bool
        """
        return (
            self.todas_en_home(tablero)
            and not self.tiene_en_barra(tablero)
            and not tablero.oponente_en_cuadrante(self)
        )

    def colocar_checker_en_posicion(self, checker: "Checker", posicion: int) -> None:
        """
        Places a checker at a given board position.

        Parameters
        ----------
        checker : Checker
        posicion : int
        """
        checker.colocar_en_posicion(posicion)

    def mover_checker_a(self, checker: "Checker", posicion: int) -> None:
        """
        Moves a checker to another board position.

        Parameters
        ----------
        checker : Checker
        posicion : int
        """
        checker.mover_a(posicion)

    def enviar_checker_a_barra(self, checker: "Checker") -> None:
        """
        Sends a checker to the bar.

        Parameters
        ----------
        checker : Checker
        """
        checker.enviar_a_barra()

    def sacar_checker(self, checker: "Checker") -> None:
        """
        Marks a checker as borne off.

        Parameters
        ----------
        checker : Checker
        """
        checker.sacar()

    def checkers_en_tablero(self) -> List["Checker"]:
        """
        Returns a list of checkers currently on the board.

        Returns
        -------
        list[Checker]
        """
        return [c for c in self.__checkers__ if c.en_tablero()]

    def checkers_en_barra(self) -> List["Checker"]:
        """
        Returns a list of checkers currently on the bar.

        Returns
        -------
        list[Checker]
        """
        return [c for c in self.__checkers__ if c.en_barra()]

    def checkers_fuera(self) -> List["Checker"]:
        """
        Returns a list of checkers that have been borne off.

        Returns
        -------
        list[Checker]
        """
        return [c for c in self.__checkers__ if c.fuera()]

    def __str__(self) -> str:
        """
        Returns a friendly string representation of the player.

        Returns
        -------
        str
        """
        return f"Player({self.__nombre__}, {self.__color__}, dir={self.__direccion__})"

    def __repr__(self) -> str:
        """
        Returns a technical string representation for debugging.

        Returns
        -------
        str
        """
        return (
            "Player("
            f"id={self.__id__!r}, nombre={self.__nombre__!r}, color={self.__color__!r}, "
            f"direccion={self.__direccion__!r}, home_points={sorted(self.__home_points__)!r}, "
            f"entry_point={self.__entry_point__!r}, checkers={len(self.__checkers__)!r})"
        )
