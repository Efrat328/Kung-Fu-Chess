# tests/test_airborne_state.py
from airborne_state import AirborneState


class TestAirborneState:
    def test_is_active_before_until_time(self):
        state = AirborneState((0, 0), "w", 1000)
        assert state.is_active(500) is True

    def test_is_active_exactly_at_until_time(self):
        state = AirborneState((0, 0), "w", 1000)
        assert state.is_active(1000) is True

    def test_is_not_active_after_until_time(self):
        state = AirborneState((0, 0), "w", 1000)
        assert state.is_active(1001) is False

    def test_stores_position_and_color(self):
        state = AirborneState((2, 3), "b", 500)
        assert state.position == (2, 3)
        assert state.color == "b"
        assert state.until_time == 500