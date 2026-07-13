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