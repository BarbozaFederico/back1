import pytest
from backgammon.core.player import (
    Player,
    PoliticaNula,
    PasoMovimiento,
    OpcionMovimiento,
)
from backgammon.core.checker import Checker


class DummyTablero:
    """Tablero simulado para pruebas de Player."""

    def __init__(self):
        self.bar = False
        self.home = False
        self.pip = 42
        self.legal_moves = [OpcionMovimiento([PasoMovimiento(0, 1, 2)], "hash", 1.0)]
        self.applied = False

    def jugador_tiene_en_barra(self, jugador):
        return self.bar

    def jugador_todo_en_home(self, jugador):
        return self.home

    def oponente_en_cuadrante(self, jugador):
        return False

    def jugador_pip_count(self, jugador):
        return self.pip

    def enumerar_opciones_legales(self, jugador, dados):
        return self.legal_moves

    def aplicar_movimiento(self, jugador, secuencia):
        self.applied = True


def make_player():
    checkers = [Checker("blancas"), Checker("blancas"), Checker("blancas")]
    return Player(
        player_id="P1",
        nombre="Ricardo",
        color="blancas",
        direccion=1,
        home_points=[0, 1, 2, 3, 4, 5],
        entry_point=0,
        checkers=checkers,
        politica=None,
    )


def test_player_initialization():
    """Testea la inicialización y getters básicos de Player."""
    p = make_player()
    assert p.get_id() == "P1"
    assert p.get_nombre() == "Ricardo"
    assert p.get_color() == "blancas"
    assert p.get_direccion() == 1
    assert 0 in p.get_home_points()
    assert p.get_entry_point() == 0
    assert len(p.get_checkers()) == 3


def test_player_checkers_management():
    """Testea métodos de gestión de fichas en Player."""
    p = make_player()
    c = p.get_checkers()[0]
    p.colocar_checker_en_posicion(c, 5)
    assert c.get_posicion() == 5
    p.mover_checker_a(c, 7)
    assert c.get_posicion() == 7
    p.enviar_checker_a_barra(c)
    assert c.en_barra()
    p.sacar_checker(c)
    assert c.fuera()


def test_player_checkers_filters():
    """Testea los métodos para filtrar fichas por estado."""
    p = make_player()
    c1, c2, c3 = p.get_checkers()
    p.colocar_checker_en_posicion(c1, 1)
    p.enviar_checker_a_barra(c2)
    p.sacar_checker(c3)
    tablero = p.checkers_en_tablero()
    barra = p.checkers_en_barra()
    fuera = p.checkers_fuera()
    assert c1 in tablero and len(tablero) == 1
    assert c2 in barra and len(barra) == 1
    assert c3 in fuera and len(fuera) == 1


def test_player_tablero_delegation():
    """Testea delegación de consultas al tablero."""
    p = make_player()
    dummy = DummyTablero()
    dummy.bar = True
    dummy.home = True
    assert p.tiene_en_barra(dummy) is True
    assert p.todas_en_home(dummy) is True
    assert p.pip_count(dummy) == 42


def test_player_movimientos_legales():
    """Testea obtención de movimientos legales desde el tablero."""
    p = make_player()
    dummy = DummyTablero()
    moves = p.movimientos_legales(dummy, [2, 3])
    assert isinstance(moves, list)
    assert isinstance(moves[0], OpcionMovimiento)


def test_player_elegir_movimiento():
    """Testea selección de movimiento usando la política."""
    p = make_player()
    dummy = DummyTablero()
    opciones = dummy.legal_moves
    secuencia = p.elegir_movimiento(opciones)
    assert secuencia is None  # PoliticaNula no elige


def test_player_confirmar_movimiento():
    """Testea confirmación de movimiento y aplicación en tablero."""
    p = make_player()
    dummy = DummyTablero()
    secuencia = [PasoMovimiento(0, 1, 2)]
    p.confirmar_movimiento(dummy, secuencia)
    assert dummy.applied is True


def test_player_puede_bear_off():
    """Testea la consulta de si el jugador puede hacer bear off."""
    p = make_player()
    dummy = DummyTablero()
    dummy.home = True
    dummy.bar = False
    assert p.puede_bear_off(dummy) is True
    dummy.bar = True
    assert p.puede_bear_off(dummy) is False

def test_puede_bear_off_con_oponente_en_cuadrante():
    """Testea que no se pueda hacer bear off con oponente en el cuadrante."""
    p = make_player()

    class DummyTableroConOponente(DummyTablero):
        def __init__(self):
            super().__init__()
            self.oponente_presente = False

        def oponente_en_cuadrante(self, jugador):
            return self.oponente_presente

    dummy = DummyTableroConOponente()
    dummy.home = True
    dummy.bar = False

    # Escenario 1: Oponente presente, no se puede hacer bear off
    dummy.oponente_presente = True
    assert p.puede_bear_off(dummy) is False

    # Escenario 2: Oponente no presente, se puede hacer bear off
    dummy.oponente_presente = False
    assert p.puede_bear_off(dummy) is True


def test_player_getters_setters():
    """Testea todos los getters y atributos de Player."""
    p = make_player()
    assert isinstance(p.get_id(), str)
    assert isinstance(p.get_nombre(), str)
    assert p.get_color() in ("blancas", "negras")
    assert p.get_direccion() in (1, -1)
    assert isinstance(p.get_home_points(), frozenset)
    assert isinstance(p.get_entry_point(), int)
    assert isinstance(p.get_checkers(), list)


def test_player_politica_default():
    """Testea que la política por defecto es PoliticaNula."""
    p = make_player()
    assert isinstance(p.__politica__, PoliticaNula)


def test_player_repr_str():
    """Testea __repr__ y __str__ de Player."""
    p = make_player()
    s = str(p)
    r = repr(p)
    assert "Player(" in s
    assert "Player(" in r
    assert p.get_nombre() in s


def test_player_movimientos_legales_empty():
    """Testea movimientos_legales cuando no hay opciones."""
    p = make_player()

    class DummyTableroEmpty:
        def enumerar_opciones_legales(self, jugador, dados):
            return []

    dummy = DummyTableroEmpty()
    moves = p.movimientos_legales(dummy, [1, 2])
    assert moves == []


def test_player_elegir_movimiento_none():
    """Testea elegir_movimiento cuando no hay opciones."""
    p = make_player()
    secuencia = p.elegir_movimiento([])
    assert secuencia is None


def test_player_confirmar_movimiento_calls_tablero():
    """Testea que confirmar_movimiento llama a aplicar_movimiento en tablero."""
    p = make_player()
    called = {}

    class DummyTableroApply:
        def aplicar_movimiento(self, jugador, secuencia):
            called["ok"] = True

    dummy = DummyTableroApply()
    p.confirmar_movimiento(dummy, [PasoMovimiento(0, 1, 2)])
    assert called.get("ok") is True


def test_player_checkers_en_tablero_barra_fuera():
    """Testea los métodos checkers_en_tablero, checkers_en_barra y checkers_fuera."""
    p = make_player()
    c1, c2, c3 = p.get_checkers()
    p.colocar_checker_en_posicion(c1, 1)
    p.enviar_checker_a_barra(c2)
    p.sacar_checker(c3)
    assert p.checkers_en_tablero() == [c1]
    assert p.checkers_en_barra() == [c2]
    assert p.checkers_fuera() == [c3]
