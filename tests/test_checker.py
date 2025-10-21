from backgammon.core.checker import Checker


def test_checker_initial_state():
    """Testea que una ficha recién creada esté fuera del tablero, barra y bear off."""
    checker = Checker(color="blancas")
    assert not checker.en_tablero()
    assert not checker.en_barra()
    assert not checker.fuera()
    assert checker.get_color() == "blancas"
    assert checker.get_posicion() is None


def test_colocar_en_posicion():
    """Testea colocar la ficha en una posición válida."""
    checker = Checker(color="negras")
    checker.colocar_en_posicion(5)
    assert checker.en_tablero()
    assert checker.get_posicion() == 5
    assert not checker.en_barra()
    assert not checker.fuera()


def test_enviar_a_barra():
    """Testea enviar la ficha a la barra."""
    checker = Checker(color="blancas")
    checker.colocar_en_posicion(10)
    checker.enviar_a_barra()
    assert checker.en_barra()
    assert not checker.en_tablero()
    assert not checker.fuera()
    assert checker.get_posicion() is None


def test_sacar():
    """Testea sacar la ficha del tablero (bear off)."""
    checker = Checker(color="negras")
    checker.colocar_en_posicion(23)
    checker.sacar()
    assert checker.fuera()
    assert not checker.en_tablero()
    assert not checker.en_barra()
    assert checker.get_posicion() is None


def test_resetear():
    """Testea el reseteo de estado de la ficha."""
    checker = Checker(color="blancas")
    checker.colocar_en_posicion(7)
    checker.enviar_a_barra()
    checker.sacar()
    checker.resetear()
    assert not checker.en_tablero()
    assert not checker.en_barra()
    assert not checker.fuera()
    assert checker.get_posicion() is None


def test_get_owner():
    """Testea el método get_owner para obtener el dueño de la ficha."""

    class DummyPlayer:
        pass

    owner = DummyPlayer()
    checker = Checker(color="blancas", player=owner)
    assert checker.get_owner() is owner


def test_str_repr():
    """Testea las representaciones __str__ y __repr__ de Checker."""
    checker = Checker(color="negras", posicion=3, identificador="A1")
    s = str(checker)
    r = repr(checker)
    assert "Checker(" in s
    assert "negras" in s
    assert "pos 4" in s
    assert "Checker(color=negras" in r
    assert "id='A1'" in r or "id=A1" in r
