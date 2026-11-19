import pytest

from legko.domain.weights import WeightInput, WeightRecalcError, distribute_total_among_equal_slots, recalculate_weights


def test_distribute_three_equal():
    assert distribute_total_among_equal_slots(3, 100) == [34, 33, 33]


def test_distribute_two_remainder():
    assert sum(distribute_total_among_equal_slots(2, 75)) == 75
    assert sorted(distribute_total_among_equal_slots(2, 75)) == [37, 38]


def test_recalculate_three_active():
    slots = [
        WeightInput("a", True, False, None),
        WeightInput("b", True, False, None),
        WeightInput("c", True, False, None),
    ]
    out = recalculate_weights(slots)
    assert sum(out.values()) == 100
    assert sorted(out.values()) == [33, 33, 34]


def test_recalculate_pin_25_two_others():
    slots = [
        WeightInput("p", True, True, 25, 25),
        WeightInput("a", True, False, None),
        WeightInput("b", True, False, None),
    ]
    out = recalculate_weights(slots)
    assert out["p"] == 25
    assert out["a"] + out["b"] == 75
    assert sorted([out["a"], out["b"]]) == [37, 38]


def test_removed_get_zero():
    slots = [
        WeightInput("a", True, False, None),
        WeightInput("b", False, False, None, 40),
    ]
    out = recalculate_weights(slots)
    assert out["b"] == 0
    assert out["a"] == 100


def test_pinned_sum_over_100_raises():
    slots = [
        WeightInput("a", True, True, 60),
        WeightInput("b", True, True, 50),
    ]
    with pytest.raises(WeightRecalcError):
        recalculate_weights(slots)