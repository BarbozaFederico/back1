from typing import Optional


class Move:
    def __init__(
        self,
        start_point: int,
        end_point: int,
        dice_value: int,
        is_bear_off: bool = False,
        hit_opponent: bool = False,
    ):
        self.start_point = start_point
        self.end_point = end_point
        self.dice_value = dice_value
        self.is_bear_off = is_bear_off
        self.hit_opponent = hit_opponent

    def __repr__(self):
        if self.is_bear_off:
            return f"Move(from={self.start_point}, to=BearOff, dice={self.dice_value})"
        return f"Move(from={self.start_point}, to={self.end_point}, dice={self.dice_value})"

    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return (
            self.start_point == other.start_point
            and self.end_point == other.end_point
            and self.dice_value == other.dice_value
            and self.is_bear_off == other.is_bear_off
            and self.hit_opponent == other.hit_opponent
        )

    def __hash__(self):
        return hash(
            (
                self.start_point,
                self.end_point,
                self.dice_value,
                self.is_bear_off,
                self.hit_opponent,
            )
        )
