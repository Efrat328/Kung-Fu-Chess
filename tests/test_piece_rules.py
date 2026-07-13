import pytest
from piece_rules import PieceMovementRules


class TestKingMove:
    def test_one_step_horizontal_is_legal(self):
        assert PieceMovementRules.is_legal_move("K", (0, 0), (0, 1)) is True

    def test_one_step_vertical_is_legal(self):
        assert PieceMovementRules.is_legal_move("K", (0, 0), (1, 0)) is True

    def test_one_step_diagonal_is_legal(self):
        assert PieceMovementRules.is_legal_move("K", (0, 0), (1, 1)) is True

    def test_two_steps_is_illegal(self):
        assert PieceMovementRules.is_legal_move("K", (0, 0), (2, 2)) is False

    def test_staying_in_place_is_illegal(self):
        assert PieceMovementRules.is_legal_move("K", (0, 0), (0, 0)) is False


class TestRookMove:
    def test_horizontal_move_is_legal(self):
        assert PieceMovementRules.is_legal_move("R", (0, 0), (0, 3)) is True

    def test_vertical_move_is_legal(self):
        assert PieceMovementRules.is_legal_move("R", (0, 0), (3, 0)) is True

    def test_diagonal_move_is_illegal(self):
        assert PieceMovementRules.is_legal_move("R", (0, 0), (1, 1)) is False

    def test_staying_in_place_is_illegal(self):
        assert PieceMovementRules.is_legal_move("R", (0, 0), (0, 0)) is False


class TestBishopMove:
    def test_diagonal_move_is_legal(self):
        assert PieceMovementRules.is_legal_move("B", (0, 0), (2, 2)) is True

    def test_horizontal_move_is_illegal(self):
        assert PieceMovementRules.is_legal_move("B", (0, 0), (0, 2)) is False

    def test_vertical_move_is_illegal(self):
        assert PieceMovementRules.is_legal_move("B", (0, 0), (2, 0)) is False

    def test_non_equal_diagonal_is_illegal(self):
        assert PieceMovementRules.is_legal_move("B", (0, 0), (2, 3)) is False


class TestQueenMove:
    def test_diagonal_move_is_legal(self):
        assert PieceMovementRules.is_legal_move("Q", (0, 0), (2, 2)) is True

    def test_horizontal_move_is_legal(self):
        assert PieceMovementRules.is_legal_move("Q", (0, 0), (0, 3)) is True

    def test_vertical_move_is_legal(self):
        assert PieceMovementRules.is_legal_move("Q", (0, 0), (3, 0)) is True

    def test_knight_shape_move_is_illegal(self):
        assert PieceMovementRules.is_legal_move("Q", (0, 0), (1, 2)) is False


class TestKnightMove:
    def test_two_one_shape_is_legal(self):
        assert PieceMovementRules.is_legal_move("N", (0, 0), (2, 1)) is True

    def test_one_two_shape_is_legal(self):
        assert PieceMovementRules.is_legal_move("N", (0, 0), (1, 2)) is True

    def test_straight_move_is_illegal(self):
        assert PieceMovementRules.is_legal_move("N", (0, 0), (2, 0)) is False

    def test_diagonal_move_is_illegal(self):
        assert PieceMovementRules.is_legal_move("N", (0, 0), (2, 2)) is False


class TestUnknownPiece:
    def test_unrecognized_letter_returns_false(self):
        assert PieceMovementRules.is_legal_move("Z", (0, 0), (1, 1)) is False