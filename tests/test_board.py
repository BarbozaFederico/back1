import pytest
from backgammon.core.board import Board
from backgammon.core.checker import Checker


class DummyPlayer:
    """Dummy player for board tests."""

    def __init__(self, color="blancas", direccion=1, home_points=None, entry_point=0):
        self._color = color
        self._direccion = direccion
        self._home_points = home_points or (
            [18, 19, 20, 21, 22, 23] if color == "blancas" else [0, 1, 2, 3, 4, 5]
        )
        self._entry_point = entry_point
        self._checkers = [Checker(color) for _ in range(15)]

    def get_color(self):
        return self._color

    def get_direccion(self):
        return self._direccion

    def get_home_points(self):
        return set(self._home_points)

    def get_entry_point(self):
        return self._entry_point

    def get_checkers(self):
        return self._checkers

    def puede_bear_off(self, board):
        # Simula que puede hacer bear-off si todas en home y ninguna en barra
        return all(
            (c.get_posicion() in self._home_points or c.fuera()) for c in self._checkers
        ) and not board.jugador_tiene_en_barra(self)


def make_checker(color="blancas"):
    return Checker(color)


def test_board_initialization():
    """Testea que el tablero se inicializa correctamente."""
    board = Board()
    assert isinstance(board.points, list)
    assert len(board.points) == 24
    assert all(isinstance(point, list) and len(point) == 0 for point in board.points)
    assert isinstance(board.bar, dict)
    assert isinstance(board.borne_off, dict)
    assert board.players == []
    assert board.dice is None


def test_add_player():
    """Testea agregar jugadores al tablero."""
    board = Board()
    p1 = DummyPlayer("blancas")
    p2 = DummyPlayer("negras")
    board.add_player(p1)
    board.add_player(p2)
    assert p1 in board.players
    assert p2 in board.players
    assert len(board.players) == 2


def test_place_checker_and_move_checker():
    """Testea colocar una ficha en una punta específica y moverla."""
    board = Board()
    checker = Checker("blancas")
    board.place_checker(checker, 5)
    assert checker in board.points[5]
    assert checker.get_posicion() == 5
    board.move_checker(checker, 5, 10)
    assert checker in board.points[10]
    assert checker.get_posicion() == 10
    assert checker not in board.points[5]


def test_send_to_bar_and_bear_off_checker():
    """Testea enviar una ficha a la barra y sacarla del tablero (bear off)."""
    board = Board()
    checker = Checker("negras")
    board.send_to_bar(checker)
    assert checker in board.bar["negras"]
    assert checker.en_barra()
    board.bear_off_checker(checker)
    assert checker in board.borne_off["negras"]
    assert checker.fuera()


def test_get_checkers_on_point():
    """Testea obtener fichas en una punta específica."""
    board = Board()
    checker1 = Checker("blancas")
    checker2 = Checker("blancas")
    board.place_checker(checker1, 0)
    board.place_checker(checker2, 0)
    result = board.get_checkers_on_point(0)
    assert checker1 in result and checker2 in result
    assert len(result) == 2
    assert board.get_checkers_on_point(23) == []
    assert board.get_checkers_on_point(24) == []


def test_get_bar_and_borne_off():
    """Testea obtener fichas en barra y fuera."""
    board = Board()
    c1 = Checker("blancas")
    c2 = Checker("negras")
    board.send_to_bar(c1)
    board.send_to_bar(c2)
    board.bear_off_checker(c1)
    assert c1 in board.get_bar("blancas")
    assert c2 in board.get_bar("negras")
    assert c1 in board.get_borne_off("blancas")
    assert board.get_borne_off("negras") == []


def test_display(capsys):
    """Testea que el método display imprime el estado del tablero."""
    board = Board()
    c1 = Checker("blancas")
    c2 = Checker("negras")
    board.place_checker(c1, 0)
    board.place_checker(c2, 23)
    board.send_to_bar(c1)
    board.bear_off_checker(c2)
    board.display()
    captured = capsys.readouterr()
    assert "Tablero:" in captured.out
    assert "Barra:" in captured.out
    assert "Fuera (Bear Off):" in captured.out
    assert "Punta 1:" in captured.out
    assert "Punta 24:" in captured.out
    assert "blancas:" in captured.out
    assert "negras:" in captured.out


def test_reset():
    """Testea el reseteo del tablero."""
    board = Board()
    c1 = Checker("blancas")
    board.place_checker(c1, 5)
    board.send_to_bar(c1)
    board.bear_off_checker(c1)
    board.add_player(DummyPlayer())
    board.dice = "dummy"
    board.reset()
    assert all(len(point) == 0 for point in board.points)
    assert board.bar["blancas"] == []
    assert board.bar["negras"] == []
    assert board.borne_off["blancas"] == []
    assert board.borne_off["negras"] == []
    assert board.players == []
    assert board.dice is None


def test_jugador_tiene_en_barra():
    board = Board()
    p = DummyPlayer("blancas")
    board.add_player(p)
    checker = p.get_checkers()[0]
    board.send_to_bar(checker)
    assert board.jugador_tiene_en_barra(p) is True


def test_jugador_todo_en_home():
    board = Board()
    p = DummyPlayer("blancas")
    board.add_player(p)
    # Todas en home
    for c in p.get_checkers():
        board.place_checker(c, 18)
    assert board.jugador_todo_en_home(p) is True
    # Una en barra
    board.send_to_bar(p.get_checkers()[0])
    assert board.jugador_todo_en_home(p) is False
    # Una fuera de home
    board.reset()
    board.add_player(p)
    for c in p.get_checkers():
        board.place_checker(c, 5)
    assert board.jugador_todo_en_home(p) is False


def test_jugador_pip_count():
    board = Board()
    p = DummyPlayer("blancas")
    board.add_player(p)
    # Todas en home, posición 18
    for c in p.get_checkers():
        board.place_checker(c, 18)
    pip = board.jugador_pip_count(p)
    assert isinstance(pip, int)
    assert pip >= 0


def test_aplicar_movimiento_and_enumerar_opciones_legales():
    board = Board()
    p = DummyPlayer("blancas")
    board.add_player(p)
    # Coloca todas las fichas en el home area para permitir bear-off
    # Coloca una ficha en 18 y el resto en otras posiciones home
    checkers = p.get_checkers()
    board.place_checker(checkers[0], 18)  # Esta es la que vamos a mover
    # Coloca las otras fichas en posiciones home para permitir bear-off
    for i, c in enumerate(checkers[1:]):
        board.place_checker(c, 19 + (i % 5))  # Distribuye en posiciones 19-23

    opciones = board.enumerar_opciones_legales(p, [6])
    assert isinstance(opciones, list)
    assert opciones
    secuencia = opciones[0].secuencia
    board.aplicar_movimiento(p, secuencia)
    # La ficha debe haber sido sacada (bear-off) ya que 18+6=24 que está fuera
    assert checkers[0].fuera()  # Debe estar fuera del tablero


def test__es_movimiento_valido_and__es_captura():
    board = Board()
    p = DummyPlayer("blancas")
    board.add_player(p)
    # Coloca ficha rival en destino
    c1 = p.get_checkers()[0]
    c2 = Checker("negras")
    board.place_checker(c1, 10)
    board.place_checker(c2, 16)
    # Movimiento válido y captura
    assert board._es_movimiento_valido(p, 10, 16, board) is True
    assert board._es_captura(p, 16, board) is True
    # Movimiento inválido (2 fichas rivales)
    c3 = Checker("negras")
    board.place_checker(c3, 16)
    assert board._es_movimiento_valido(p, 10, 16, board) is False


def test_place_checker_invalid_point():
    """Testea que place_checker no agregue ficha en punto inválido."""
    board = Board()
    checker = Checker("blancas")
    board.place_checker(checker, -1)
    board.place_checker(checker, 24)
    assert checker not in board.points[0]
    assert checker not in board.points[-1]


def test_move_checker_invalid_points():
    """Testea que move_checker no mueva si los puntos son inválidos."""
    board = Board()
    checker = Checker("blancas")
    board.place_checker(checker, 5)
    board.move_checker(checker, -1, 10)
    board.move_checker(checker, 5, 24)
    # Debe seguir en la posición original
    assert checker in board.points[5]


def test_get_checkers_on_point_out_of_range():
    """Testea get_checkers_on_point para puntos fuera de rango."""
    board = Board()
    assert board.get_checkers_on_point(-1) == []
    assert board.get_checkers_on_point(24) == []


def test_aplicar_paso_movimiento_no_checker_found():
    """Testea error si no se encuentra ficha para mover."""
    board = Board()
    from backgammon.core.player import PasoMovimiento

    class DummyPlayer:
        def get_color(self):
            return "blancas"

    paso = PasoMovimiento(desde=0, hasta=1, dado=1, captura=False)
    with pytest.raises(ValueError):
        board._aplicar_paso_movimiento(DummyPlayer(), paso)


def test_aplicar_paso_movimiento_captura():
    """Testea captura de ficha rival en destino."""
    board = Board()
    from backgammon.core.player import PasoMovimiento

    class DummyPlayer:
        def get_color(self):
            return "blancas"

    checker_blanca = Checker("blancas")
    checker_negra = Checker("negras")
    board.place_checker(checker_blanca, 0)
    board.place_checker(checker_negra, 1)
    paso = PasoMovimiento(desde=0, hasta=1, dado=1, captura=True)
    board._aplicar_paso_movimiento(DummyPlayer(), paso)
    assert checker_negra in board.bar["negras"]
    assert checker_blanca in board.points[1]


def test_enumerar_opciones_legales_invalid_dados():
    """Testea enumerar_opciones_legales con dados inválidos."""
    board = Board()

    class DummyPlayer:
        def get_color(self):
            return "blancas"

        def get_home_points(self):
            return set([18, 19, 20, 21, 22, 23])

        def get_direccion(self):
            return 1

        def get_entry_point(self):
            return 0

        def get_checkers(self):
            return [Checker("blancas") for _ in range(15)]

        def puede_bear_off(self, b):
            return False

    with pytest.raises(ValueError):
        board.enumerar_opciones_legales(DummyPlayer(), "invalid")


def test__generar_secuencias_movimiento_no_dice():
    """Testea _generar_secuencias_movimiento sin dados restantes."""
    board = Board()

    class DummyPlayer:
        def get_color(self):
            return "blancas"

        def get_home_points(self):
            return set([18, 19, 20, 21, 22, 23])

        def get_direccion(self):
            return 1

        def get_entry_point(self):
            return 0

        def get_checkers(self):
            return [Checker("blancas") for _ in range(15)]

        def puede_bear_off(self, b):
            return False

    result = board._generar_secuencias_movimiento(DummyPlayer(), [], [], board)
    assert result == []


def test__generar_movimientos_posibles_barra_bloqueada():
    """Testea entrada desde barra bloqueada."""
    board = Board()
    from backgammon.core.player import PasoMovimiento

    class DummyPlayer:
        def get_color(self):
            return "blancas"

        def get_home_points(self):
            return set([18, 19, 20, 21, 22, 23])

        def get_direccion(self):
            return 1

        def get_entry_point(self):
            return 0

        def get_checkers(self):
            return [Checker("blancas") for _ in range(15)]

        def puede_bear_off(self, b):
            return False

    # Simula ficha en barra y destino bloqueado
    board.bar["blancas"].append(Checker("blancas"))
    board.points[6].extend([Checker("negras"), Checker("negras")])
    moves = board._generar_movimientos_posibles(DummyPlayer(), 6, board)
    assert moves == []


def test__es_movimiento_valido_bear_off():
    """Testea _es_movimiento_valido para bear-off."""
    board = Board()

    class DummyPlayer:
        def get_color(self):
            return "blancas"

        def puede_bear_off(self, b):
            return True

    assert board._es_movimiento_valido(DummyPlayer(), 0, None, board) is True


def test__es_movimiento_valido_out_of_range():
    """Testea _es_movimiento_valido para destino fuera de rango."""
    board = Board()

    class DummyPlayer:
        def get_color(self):
            return "blancas"

        def puede_bear_off(self, b):
            return False

    assert board._es_movimiento_valido(DummyPlayer(), 0, -1, board) is False
    assert board._es_movimiento_valido(DummyPlayer(), 0, 24, board) is False


def test__es_captura_false_cases():
    """Testea _es_captura para casos que no son captura."""
    board = Board()

    class DummyPlayer:
        def get_color(self):
            return "blancas"

    # Sin fichas en destino
    assert board._es_captura(DummyPlayer(), 5, board) is False
    # Ficha propia en destino
    checker = Checker("blancas")
    board.place_checker(checker, 6)
    assert board._es_captura(DummyPlayer(), 6, board) is False
    # Más de una ficha rival
    board.points[7].extend([Checker("negras"), Checker("negras")])
    assert board._es_captura(DummyPlayer(), 7, board) is False


def test__calcular_hash_secuencia_empty():
    """Testea _calcular_hash_secuencia con secuencia vacía."""
    board = Board()

    class DummyPlayer:
        def get_color(self):
            return "blancas"

    h = board._calcular_hash_secuencia(DummyPlayer(), [])
    assert isinstance(h, str)
    assert h.startswith("blancas:")


def test_place_checker_none_checker():
    """Testea que place_checker no falle si checker es None."""
    board = Board()
    board.place_checker(None, 5)
    # No debe agregar nada ni fallar
    assert all(None not in point for point in board.points)


def test_move_checker_checker_not_in_from_point():
    """Testea que move_checker no falle si checker no está en from_point."""
    board = Board()
    checker = Checker("blancas")
    board.place_checker(checker, 5)
    board.move_checker(checker, 4, 10)  # checker no está en 4
    # Debe seguir en la posición original
    assert checker in board.points[5]


def test_send_to_bar_checker_none():
    """Testea que send_to_bar no falle si checker es None."""
    board = Board()
    board.send_to_bar(None)
    # No debe agregar nada ni fallar
    assert None not in board.bar["blancas"]
    assert None not in board.bar["negras"]


def test_bear_off_checker_checker_none():
    """Testea que bear_off_checker no falle si checker es None."""
    board = Board()
    board.bear_off_checker(None)
    assert None not in board.borne_off["blancas"]
    assert None not in board.borne_off["negras"]


def test_get_bar_invalid_color():
    """Testea get_bar con color inválido."""
    board = Board()
    assert board.get_bar("rojo") == []


def test_get_borne_off_invalid_color():
    """Testea get_borne_off con color inválido."""
    board = Board()
    assert board.get_borne_off("rojo") == []


def test_display_empty_board(capsys):
    """Testea display con tablero vacío."""
    board = Board()
    board.display()
    captured = capsys.readouterr()
    assert "Tablero:" in captured.out
    assert "Picos:" in captured.out


def test_reset_multiple_times():
    """Testea reset varias veces consecutivas."""
    board = Board()
    board.reset()
    board.reset()
    assert all(len(point) == 0 for point in board.points)
    assert board.bar["blancas"] == []
    assert board.bar["negras"] == []
    assert board.borne_off["blancas"] == []
    assert board.borne_off["negras"] == []
    assert board.players == []
    assert board.dice is None


def test_aplicar_movimiento_empty_secuencia():
    """Testea aplicar_movimiento con secuencia vacía."""
    board = Board()

    class DummyPlayer:
        pass

    board.aplicar_movimiento(DummyPlayer(), [])
    # No debe fallar ni modificar el tablero


def test_enumerar_opciones_legales_empty_dados():
    """Testea enumerar_opciones_legales con dados vacíos."""
    board = Board()

    class DummyPlayer:
        def get_color(self):
            return "blancas"

        def get_home_points(self):
            return set([18, 19, 20, 21, 22, 23])

        def get_direccion(self):
            return 1

        def get_entry_point(self):
            return 0

        def get_checkers(self):
            return [Checker("blancas") for _ in range(15)]

        def puede_bear_off(self, b):
            return False

    opciones = board.enumerar_opciones_legales(DummyPlayer(), [])
    assert opciones == []


def test__generar_secuencias_movimiento_no_checkers():
    """Testea _generar_secuencias_movimiento sin fichas."""
    board = Board()

    class DummyPlayer:
        def get_color(self):
            return "blancas"

        def get_home_points(self):
            return set([18, 19, 20, 21, 22, 23])

        def get_direccion(self):
            return 1

        def get_entry_point(self):
            return 0

        def get_checkers(self):
            return []

        def puede_bear_off(self, b):
            return False

    result = board._generar_secuencias_movimiento(DummyPlayer(), [1], [], board)
    assert result == []


def test__generar_movimientos_posibles_no_checkers():
    """Testea _generar_movimientos_posibles sin fichas."""
    board = Board()

    class DummyPlayer:
        def get_color(self):
            return "blancas"

        def get_home_points(self):
            return set([18, 19, 20, 21, 22, 23])

        def get_direccion(self):
            return 1

        def get_entry_point(self):
            return 0

        def get_checkers(self):
            return []

        def puede_bear_off(self, b):
            return False

    moves = board._generar_movimientos_posibles(DummyPlayer(), 6, board)
    assert moves == []


def test__es_movimiento_valido_checker_none():
    """Testea _es_movimiento_valido con checker None."""
    board = Board()

    class DummyPlayer:
        def get_color(self):
            return "blancas"

        def puede_bear_off(self, b):
            return False

    # No hay fichas en origen
    assert board._es_movimiento_valido(DummyPlayer(), 5, 6, board) is False


def test__es_captura_checker_none():
    """Testea _es_captura con destino vacío."""
    board = Board()

    class DummyPlayer:
        def get_color(self):
            return "blancas"

    assert board._es_captura(DummyPlayer(), 8, board) is False


def test__calcular_hash_secuencia_none_player():
    """Testea _calcular_hash_secuencia con player None."""
    board = Board()
    from backgammon.core.player import PasoMovimiento

    secuencia = [PasoMovimiento(0, 5, 5, False)]
    h = board._calcular_hash_secuencia(None, secuencia)
    assert isinstance(h, str)
    assert h.startswith("None:")
