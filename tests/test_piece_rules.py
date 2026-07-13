# tests/test_piece_rules.py
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


class TestRequiresClearPath:
    def test_rook_requires_clear_path(self):
        assert PieceMovementRules.requires_clear_path("R") is True

    def test_bishop_requires_clear_path(self):
        assert PieceMovementRules.requires_clear_path("B") is True

    def test_queen_requires_clear_path(self):
        assert PieceMovementRules.requires_clear_path("Q") is True

    def test_knight_does_not_require_clear_path(self):
        assert PieceMovementRules.requires_clear_path("N") is False

    def test_king_does_not_require_clear_path(self):
        assert PieceMovementRules.requires_clear_path("K") is False


class TestGetPathCells:
    def test_horizontal_path_returns_cells_between(self):
        cells = PieceMovementRules.get_path_cells((0, 0), (0, 3))
        assert cells == [(0, 1), (0, 2)]

    def test_vertical_path_returns_cells_between(self):
        cells = PieceMovementRules.get_path_cells((0, 0), (3, 0))
        assert cells == [(1, 0), (2, 0)]

    def test_diagonal_path_returns_cells_between(self):
        cells = PieceMovementRules.get_path_cells((0, 0), (3, 3))
        assert cells == [(1, 1), (2, 2)]

    def test_adjacent_cells_have_empty_path(self):
        cells = PieceMovementRules.get_path_cells((0, 0), (0, 1))
        assert cells == []

    def test_reverse_direction_path(self):
        cells = PieceMovementRules.get_path_cells((3, 3), (0, 0))
        assert cells == [(2, 2), (1, 1)]


class TestWhitePawnMove:
    def test_single_step_forward_to_empty_is_legal(self):
        assert PieceMovementRules.is_legal_move(
            "P", (1, 1), (0, 1), color="w", target_occupied_by_enemy=False
        ) is True

    def test_double_step_forward_is_illegal(self):
        assert PieceMovementRules.is_legal_move(
            "P", (3, 1), (1, 1), color="w", target_occupied_by_enemy=False
        ) is False

    def test_backward_step_is_illegal(self):
        assert PieceMovementRules.is_legal_move(
            "P", (1, 1), (2, 1), color="w", target_occupied_by_enemy=False
        ) is False

    def test_diagonal_capture_is_legal(self):
        assert PieceMovementRules.is_legal_move(
            "P", (1, 1), (0, 0), color="w", target_occupied_by_enemy=True
        ) is True

    def test_diagonal_without_enemy_is_illegal(self):
        assert PieceMovementRules.is_legal_move(
            "P", (1, 1), (0, 0), color="w", target_occupied_by_enemy=False
        ) is False

    def test_forward_onto_enemy_is_illegal(self):
        assert PieceMovementRules.is_legal_move(
            "P", (1, 1), (0, 1), color="w", target_occupied_by_enemy=True
        ) is False


class TestBlackPawnMove:
    def test_single_step_forward_to_empty_is_legal(self):
        assert PieceMovementRules.is_legal_move(
            "P", (1, 1), (2, 1), color="b", target_occupied_by_enemy=False
        ) is True

    def test_double_step_forward_is_illegal(self):
        assert PieceMovementRules.is_legal_move(
            "P", (0, 1), (2, 1), color="b", target_occupied_by_enemy=False
        ) is False

    def test_backward_step_is_illegal(self):
        assert PieceMovementRules.is_legal_move(
            "P", (1, 1), (0, 1), color="b", target_occupied_by_enemy=False
        ) is False

    def test_diagonal_capture_is_legal(self):
        assert PieceMovementRules.is_legal_move(
            "P", (1, 1), (2, 2), color="b", target_occupied_by_enemy=True
        ) is True

    def test_forward_onto_enemy_is_illegal(self):
        assert PieceMovementRules.is_legal_move(
            "P", (1, 1), (2, 1), color="b", target_occupied_by_enemy=True
        ) is False


class TestPawnDoesNotRequireClearPath:
    def test_pawn_does_not_require_clear_path(self):
        assert PieceMovementRules.requires_clear_path("P") is False


class TestPawnInvalidColumnJump:
    def test_pawn_column_jump_of_two_is_illegal(self):
        assert PieceMovementRules.is_legal_move(
            "P", (1, 1), (0, 3), color="w", target_occupied_by_enemy=False
        ) is False


class TestPieceRuleBaseClass:
    def test_base_class_raises_not_implemented(self):
        from piece_rules import PieceRule
        with pytest.raises(NotImplementedError):
            PieceRule().is_legal_move("w", (0, 0), (0, 1), False)