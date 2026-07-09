# tests/test_board.py
import pytest
from board import Board, BoardParseError


class TestBoardDimensions:
    def test_infers_correct_num_rows_and_cols(self):
        rows = [["wK", ".", ".", "bK"], [".", ".", ".", "."], ["wR", ".", ".", "bR"]]
        board = Board(rows)
        assert board.num_rows == 3
        assert board.num_cols == 4

    def test_empty_board_has_zero_dimensions(self):
        board = Board([])
        assert board.num_rows == 0
        assert board.num_cols == 0


class TestValidateValidTokens:
    def test_valid_board_passes_validation(self):
        rows = [["wK", ".", "bQ"], [".", "wN", "."], ["bP", ".", "wR"]]
        board = Board(rows)
        board.validate()  # לא אמור לזרוק exception

    def test_all_piece_types_are_valid(self):
        rows = [["wK", "wQ", "wR", "wB", "wN", "wP"],
                ["bK", "bQ", "bR", "bB", "bN", "bP"]]
        board = Board(rows)
        board.validate()

    def test_empty_squares_are_valid(self):
        rows = [[".", "."], [".", "."]]
        board = Board(rows)
        board.validate()


class TestValidateUnknownToken:
    def test_raises_on_unknown_token(self):
        rows = [["wK", "xZ"], [".", "."]]
        board = Board(rows)
        with pytest.raises(BoardParseError) as exc_info:
            board.validate()
        assert exc_info.value.error_code == "UNKNOWN_TOKEN"

    def test_raises_on_invalid_color_prefix(self):
        rows = [["zK", "."]]
        board = Board(rows)
        with pytest.raises(BoardParseError) as exc_info:
            board.validate()
        assert exc_info.value.error_code == "UNKNOWN_TOKEN"

    def test_raises_on_invalid_piece_letter(self):
        rows = [["wZ", "."]]
        board = Board(rows)
        with pytest.raises(BoardParseError) as exc_info:
            board.validate()
        assert exc_info.value.error_code == "UNKNOWN_TOKEN"

    def test_raises_on_wrong_length_token(self):
        rows = [["wKing", "."]]
        board = Board(rows)
        with pytest.raises(BoardParseError) as exc_info:
            board.validate()
        assert exc_info.value.error_code == "UNKNOWN_TOKEN"


class TestValidateRowWidthMismatch:
    def test_raises_when_row_shorter_than_others(self):
        rows = [["wK", ".", "."], [".", "bK"]]
        board = Board(rows)
        with pytest.raises(BoardParseError) as exc_info:
            board.validate()
        assert exc_info.value.error_code == "ROW_WIDTH_MISMATCH"

    def test_raises_when_row_longer_than_others(self):
        rows = [["wK", "."], [".", "bK", "."]]
        board = Board(rows)
        with pytest.raises(BoardParseError) as exc_info:
            board.validate()
        assert exc_info.value.error_code == "ROW_WIDTH_MISMATCH"

    def test_single_row_board_is_valid(self):
        rows = [["wK", ".", "bK"]]
        board = Board(rows)
        board.validate()


class TestCanonicalString:
    def test_returns_correct_format(self):
        rows = [["wK", ".", ".", "bK"], [".", ".", ".", "."], ["wR", ".", ".", "bR"]]
        board = Board(rows)
        expected = "wK . . bK\n. . . .\nwR . . bR"
        assert board.to_canonical_string() == expected

    def test_single_row(self):
        rows = [["wK", "."]]
        board = Board(rows)
        assert board.to_canonical_string() == "wK ."

    def test_all_empty_squares(self):
        rows = [[".", "."], [".", "."]]
        board = Board(rows)
        assert board.to_canonical_string() == ". .\n. ."