# tests/test_game.py
import pytest
from board import Board
from game import Game
 
 
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
        assert game.board.get_token(0, 1) == "wP"
        assert game.board.get_token(1, 1) == "."
 
    def test_black_pawn_moves_down(self):
        game = make_game([[".", ".", "."], [".", "bP", "."], [".", ".", "."]])
        game.handle_click(150, 150)
        game.handle_click(150, 250)
        game.advance_clock(2000)
        assert game.board.get_token(2, 1) == "bP"
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
        assert game.board.get_token(0, 0) == "wP"
 
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