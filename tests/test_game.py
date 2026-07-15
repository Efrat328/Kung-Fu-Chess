# tests/test_game.py
import pytest
from board import Board
from game import Game
from piece_rules import PieceMovementRules


def make_game(rows):
    return Game(Board(rows))


class TestSelection:
    def test_click_on_piece_selects_it(self):
        game = make_game([["wK", "."], [".", "."]])
        game.handle_click(50, 50)
        assert game.selected_pos == (0, 0)

    def test_click_on_empty_cell_with_no_selection_is_ignored(self):
        game = make_game([["wK", "."], [".", "."]])
        game.handle_click(150, 50)
        assert game.selected_pos is None

    def test_click_outside_board_is_ignored(self):
        game = make_game([["wK", "."], [".", "."]])
        game.handle_click(350, 50)
        assert game.selected_pos is None

    def test_click_negative_coordinates_is_ignored(self):
        game = make_game([["wK", "."], [".", "."]])
        game.handle_click(-10, 50)
        assert game.selected_pos is None

    def test_click_friendly_piece_replaces_selection(self):
        game = make_game([["wR", ".", "wK"], [".", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(250, 50)
        assert game.selected_pos == (0, 2)


class TestMoveExecution:
    def test_legal_move_relocates_piece(self):
        game = make_game([["wK", ".", "."], [".", ".", "."], [".", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(150, 150)
        game.advance_clock(2000)
        assert game.board.get_token(1, 1) == "wK"
        assert game.board.get_token(0, 0) == "."
        assert game.selected_pos is None

    def test_illegal_move_does_not_relocate_piece(self):
        game = make_game([["wK", ".", "."], [".", ".", "."], [".", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(250, 250)
        assert game.board.get_token(0, 0) == "wK"
        assert game.board.get_token(2, 2) == "."

    def test_move_onto_enemy_piece_captures_it(self):
        game = make_game([["wR", ".", "bK"]])
        game.handle_click(50, 50)
        game.handle_click(250, 50)
        game.advance_clock(3000)
        assert game.board.get_token(0, 2) == "wR"


class TestClock:
    def test_advance_clock_accumulates_time(self):
        game = make_game([["."]])
        game.advance_clock(500)
        game.advance_clock(300)
        assert game.clock_ms == 800


class TestBoardOutput:
    def test_get_board_output_matches_canonical_string(self):
        game = make_game([["wK", "."], [".", "bK"]])
        assert game.get_board_output() == "wK .\n. bK"


class TestPathBlocking:
    def test_rook_blocked_by_own_piece_does_not_move(self):
        game = make_game([["wR", "wP", "."]])
        game.handle_click(50, 50)
        game.handle_click(250, 50)
        assert game.board.get_token(0, 0) == "wR"
        assert game.board.get_token(0, 2) == "."

    def test_bishop_blocked_by_own_piece_does_not_move(self):
        game = make_game([["wB", ".", "."], [".", "wP", "."], [".", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(250, 250)
        assert game.board.get_token(0, 0) == "wB"
        assert game.board.get_token(2, 2) == "."

    def test_knight_jumps_over_blockers(self):
        game = make_game([["wN", "wP", "."], ["wP", ".", "."], [".", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(150, 250)
        game.advance_clock(3000)
        assert game.board.get_token(2, 1) == "wN"
        assert game.board.get_token(0, 0) == "."

    def test_rook_moves_when_path_is_clear(self):
        game = make_game([["wR", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(250, 50)
        game.advance_clock(3000)
        assert game.board.get_token(0, 2) == "wR"


class TestCapture:
    def test_cannot_capture_own_piece(self):
        game = make_game([["wR", ".", "wP"]])
        game.handle_click(50, 50)
        game.handle_click(250, 50)
        assert game.board.get_token(0, 0) == "wR"
        assert game.board.get_token(0, 2) == "wP"

    def test_captures_enemy_piece_at_destination(self):
        game = make_game([["wR", ".", "bR"]])
        game.handle_click(50, 50)
        game.handle_click(250, 50)
        game.advance_clock(3000)
        assert game.board.get_token(0, 2) == "wR"
        assert game.board.get_token(0, 0) == "."


class TestPawnMovement:
    def test_white_pawn_moves_up(self):
        game = make_game([[".", ".", "."], [".", "wP", "."], [".", ".", "."]])
        game.handle_click(150, 150)
        game.handle_click(150, 50)
        game.advance_clock(2000)
        assert game.board.get_token(0, 1) == "wQ"  # הגיע לשורה 0 = שורה אחרונה ללבן -> קודם
        assert game.board.get_token(1, 1) == "."

    def test_black_pawn_moves_down(self):
        game = make_game([[".", ".", "."], [".", "bP", "."], [".", ".", "."]])
        game.handle_click(150, 150)
        game.handle_click(150, 250)
        game.advance_clock(2000)
        assert game.board.get_token(2, 1) == "bQ"  # הגיע לשורה 2 = שורה אחרונה לשחור -> קודם
        assert game.board.get_token(1, 1) == "."

    def test_white_pawn_double_step_is_illegal(self):
        game = make_game([[".", ".", "."], [".", ".", "."], [".", ".", "."], [".", "wP", "."]])
        game.handle_click(150, 350)
        game.handle_click(150, 150)
        assert game.board.get_token(3, 1) == "wP"
        assert game.board.get_token(1, 1) == "."

    def test_pawn_diagonal_capture(self):
        game = make_game([["bR", ".", "."], [".", "wP", "."], [".", ".", "."]])
        game.handle_click(150, 150)
        game.handle_click(50, 50)
        game.advance_clock(2000)
        assert game.board.get_token(0, 0) == "wQ"  # הגיע לשורה 0 = שורה אחרונה ללבן -> קודם

    def test_pawn_cannot_capture_forward(self):
        game = make_game([[".", "bR", "."], [".", "wP", "."], [".", ".", "."]])
        game.handle_click(150, 150)
        game.handle_click(150, 50)
        assert game.board.get_token(0, 1) == "bR"
        assert game.board.get_token(1, 1) == "wP"


class TestPendingMoveBehavior:
    def test_piece_stays_in_place_before_arrival(self):
        game = make_game([["wR", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(150, 50)
        game.advance_clock(500)
        assert game.board.get_token(0, 0) == "wR"
        assert game.board.get_token(0, 1) == "."

    def test_piece_arrives_after_enough_time(self):
        game = make_game([["wR", ".", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(350, 50)
        game.advance_clock(1000)
        assert game.board.get_token(0, 0) == "wR"
        game.advance_clock(2000)
        assert game.board.get_token(0, 3) == "wR"
        assert game.board.get_token(0, 0) == "."

    def test_busy_piece_ignores_click_attempts(self):
        game = make_game([["wR", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(250, 50)
        game.handle_click(50, 50)
        assert game.selected_pos is None
        game.advance_clock(3000)
        assert game.board.get_token(0, 2) == "wR"


class TestGlobalMoveLock:
    def test_second_move_request_ignored_while_first_is_pending(self):
        game = make_game([["wR", ".", "."], [".", ".", "."], ["bR", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(250, 50)
        game.handle_click(50, 250)
        game.handle_click(250, 250)
        game.advance_clock(2000)
        assert game.board.get_token(0, 2) == "wR"
        assert game.board.get_token(2, 0) == "bR"

    def test_can_move_again_immediately_after_arrival_no_cooldown(self):
        game = make_game([["wR", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(150, 50)
        game.advance_clock(1000)
        game.handle_click(150, 50)
        game.handle_click(250, 50)
        game.advance_clock(1000)
        assert game.board.get_token(0, 2) == "wR"


class TestAdvancedInteractionCases:
    def test_enemy_collision_first_mover_wins(self):
        game = make_game([["wR", ".", ".", "bR"]])
        game.handle_click(50, 50)
        game.handle_click(350, 50)
        game.handle_click(350, 50)
        game.handle_click(50, 50)
        game.advance_clock(3000)
        assert game.board.get_token(0, 3) == "wR"

    def test_enemy_collision_black_first_mover_wins(self):
        game = make_game([["wR", ".", ".", "bR"]])
        game.handle_click(350, 50)
        game.handle_click(50, 50)
        game.handle_click(50, 50)
        game.handle_click(350, 50)
        game.advance_clock(3000)
        assert game.board.get_token(0, 0) == "bR"

    def test_cannot_start_move_through_friendly_piece(self):
        game = make_game([[".", ".", "."], ["wR", "wP", "."], [".", ".", "."]])
        game.handle_click(50, 150)
        game.handle_click(250, 150)
        game.advance_clock(2000)
        assert game.board.get_token(1, 0) == "wR"
        assert game.board.get_token(1, 1) == "wP"

    def test_knight_cannot_land_on_friendly_piece(self):
        game = make_game([[".", "wP", "."], [".", ".", "."], ["wN", ".", "."]])
        game.handle_click(50, 250)
        game.handle_click(150, 50)
        game.advance_clock(1000)
        assert game.board.get_token(2, 0) == "wN"
        assert game.board.get_token(0, 1) == "wP"

    def test_premove_does_not_execute_while_first_move_pending(self):
        game = make_game([["wR", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(150, 50)
        game.handle_click(50, 50)
        game.handle_click(250, 50)
        game.advance_clock(2000)
        assert game.board.get_token(0, 1) == "wR"


class TestGameOver:
    def test_capturing_king_ends_game(self):
        game = make_game([["wR", ".", "bK"]])
        game.handle_click(50, 50)
        game.handle_click(250, 50)
        game.advance_clock(2000)
        assert game.game_over is True
        assert game.board.get_token(0, 2) == "wR"

    def test_game_not_over_before_capture_completes(self):
        game = make_game([["wR", ".", "bK"]])
        game.handle_click(50, 50)
        game.handle_click(250, 50)
        game.advance_clock(1000)
        assert game.game_over is False

    def test_capturing_non_king_does_not_end_game(self):
        game = make_game([["wR", ".", "bR"]])
        game.handle_click(50, 50)
        game.handle_click(250, 50)
        game.advance_clock(2000)
        assert game.game_over is False

    def test_clicks_ignored_after_game_over(self):
        game = make_game([["wR", ".", "bK"], ["bR", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(250, 50)
        game.advance_clock(2000)
        game.handle_click(50, 150)
        game.handle_click(150, 150)
        game.advance_clock(1000)
        assert game.board.get_token(1, 0) == "bR"
        assert game.selected_pos is None


class TestPawnPromotion:
    def test_pawn_promotes_when_reaching_last_row(self):
        game = make_game([[".", ".", "."], ["wP", ".", "."]])
        game.handle_click(50, 150)
        game.handle_click(50, 50)
        game.advance_clock(1000)
        assert game.board.get_token(0, 0) == "wQ"

    def test_black_pawn_promotes_when_reaching_last_row(self):
        game = make_game([["bP", ".", "."], [".", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(50, 150)
        game.advance_clock(1000)
        assert game.board.get_token(1, 0) == "bQ"

    def test_pawn_does_not_promote_before_reaching_last_row(self):
        game = make_game([[".", ".", "."], [".", ".", "."], [".", "wP", "."], [".", ".", "."]])
        game.handle_click(150, 250)
        game.handle_click(150, 150)
        game.advance_clock(1000)
        assert game.board.get_token(1, 1) == "wP"

    def test_pawn_double_step_from_start_row(self):
        game = make_game([[".", ".", "."], [".", ".", "."], [".", ".", "."], [".", "wP", "."]])
        game.handle_click(150, 350)
        game.handle_click(150, 150)
        game.advance_clock(2000)
        assert game.board.get_token(1, 1) == "wP"
        assert game.board.get_token(3, 1) == "."

    def test_pawn_double_step_blocked_by_piece_in_path(self):
        game = make_game([[".", ".", "."], [".", ".", "."], [".", "bR", "."], [".", "wP", "."]])
        game.handle_click(150, 350)
        game.handle_click(150, 150)
        game.advance_clock(2000)
        assert game.board.get_token(3, 1) == "wP"

    def test_pawn_double_step_not_from_start_row_is_illegal(self):
        game = make_game([[".", ".", "."], [".", ".", "."], [".", "wP", "."], [".", ".", "."]])
        game.handle_click(150, 250)
        game.handle_click(150, 50)
        game.advance_clock(2000)
        assert game.board.get_token(2, 1) == "wP"

    def test_start_row_check_for_unknown_color_is_false(self):
        assert PieceMovementRules.is_pawn_start_row("x", 0, 4) is False


class TestJump:
    def test_jump_lands_normally_when_no_enemy_arrives(self):
        game = make_game([[".", ".", "."], [".", "wK", "."], [".", ".", "."]])
        game.handle_jump(150, 150)
        game.advance_clock(1000)
        assert game.board.get_token(1, 1) == "wK"
        assert game.airborne is None

    def test_airborne_piece_captures_arriving_enemy(self):
        game = make_game([[".", ".", "."], ["wK", "bR", "."], [".", ".", "."]])
        game.handle_jump(50, 150)
        game.handle_click(150, 150)
        game.handle_click(50, 150)
        game.advance_clock(1000)
        assert game.board.get_token(1, 0) == "wK"
        assert game.board.get_token(1, 1) == "."

    def test_jump_after_piece_already_captured_has_no_effect(self):
        game = make_game([[".", ".", "."], ["wK", "bR", "."], [".", ".", "."]])
        game.handle_click(150, 150)
        game.handle_click(50, 150)
        game.advance_clock(1000)
        game.handle_jump(50, 150)
        assert game.board.get_token(1, 0) == "bR"

    def test_enemy_arrives_after_landing_captures_normally(self):
        game = make_game([[".", ".", ".", "."], ["wK", ".", ".", "bR"], [".", ".", ".", "."]])
        game.handle_jump(50, 150)
        game.advance_clock(1000)
        game.handle_click(350, 150)
        game.handle_click(50, 150)
        game.advance_clock(3000)
        assert game.board.get_token(1, 0) == "bR"
        assert game.game_over is True

    def test_cannot_jump_while_piece_is_moving(self):
        game = make_game([["wR", ".", "."]])
        game.handle_click(50, 50)
        game.handle_click(250, 50)
        game.advance_clock(500)
        game.handle_jump(50, 50)
        assert game.airborne is None
        game.advance_clock(1500)
        assert game.board.get_token(0, 2) == "wR"

    def test_airborne_does_not_affect_friendly_click(self):
        game = make_game([[".", ".", "."], ["wK", "wR", "."], [".", ".", "."]])
        game.handle_jump(50, 150)
        game.handle_click(150, 150)
        game.handle_click(50, 150)
        game.advance_clock(1000)
        assert game.board.get_token(1, 0) == "wK"
        assert game.board.get_token(1, 1) == "wR"

    def test_jump_ignored_after_game_over(self):
        game = make_game([["wR", "bK"]])
        game.handle_click(50, 50)
        game.handle_click(150, 50)
        game.advance_clock(1000)
        assert game.game_over is True
        game.handle_jump(50, 50)
        assert game.airborne is None

    def test_jump_on_empty_cell_is_ignored(self):
        game = make_game([[".", "."]])
        game.handle_jump(50, 50)
        assert game.airborne is None

    def test_jump_outside_board_is_ignored(self):
        game = make_game([["wK"]])
        game.handle_jump(500, 500)
        assert game.airborne is None

    def test_arriving_move_to_different_cell_ignores_airborne(self):
        game = make_game([["wK", ".", "wR", "."]])
        game.handle_jump(50, 50)
        game.handle_click(250, 50)
        game.handle_click(350, 50)
        game.advance_clock(1000)
        assert game.board.get_token(0, 3) == "wR"
        assert game.board.get_token(0, 0) == "wK"