from backgammon.core.move import Move


def test_move_initialization():
    """Testea la inicialización de Move."""
    m = Move(1, 6, 5)
    assert m.start_point == 1
    assert m.end_point == 6
    assert m.dice_value == 5
    assert not m.is_bear_off
    assert not m.hit_opponent


def test_move_repr():
    """Testea la representación __repr__ de Move."""
    m1 = Move(2, 7, 5)
    m2 = Move(3, None, 6, is_bear_off=True)
    assert "from=2" in repr(m1)
    assert "to=7" in repr(m1)
    assert "dice=5" in repr(m1)
    assert "BearOff" in repr(m2)
    assert "dice=6" in repr(m2)


def test_move_equality_and_hash():
    """Testea igualdad y hash de Move."""
    m1 = Move(1, 6, 5)
    m2 = Move(1, 6, 5)
    m3 = Move(1, 6, 5, is_bear_off=True)
    m4 = Move(2, 6, 5)
    assert m1 == m2
    assert m1 != m3
    assert m1 != m4
    assert hash(m1) == hash(m2)
    assert hash(m1) != hash(m3)
    assert hash(m1) != hash(m4)


def test_move_hit_opponent_flag():
    """Testea el flag de captura de oponente."""
    m1 = Move(1, 6, 5, hit_opponent=True)
    m2 = Move(1, 6, 5, hit_opponent=False)
    assert m1.hit_opponent is True
    assert m2.hit_opponent is False
    assert m1 != m2


def test_move_eq_not_move_type():
    """Testea que __eq__ retorna NotImplemented si el otro objeto no es Move."""
    from backgammon.core.move import Move

    m = Move(1, 6, 5)
    assert m.__eq__("not a move") is NotImplemented
