# tests/test_input_parser.py
import pytest
from input_parser import InputParser
from board import Board


class TestInputParser:
    def test_parses_board_section_only(self):
        raw = "Board:\nwK . . bK\n. . . .\nwR . . bR\nCommands:\nprint board"
        board = InputParser.parse(raw)
        assert isinstance(board, Board)
        assert board.rows == [["wK", ".", ".", "bK"],
                               [".", ".", ".", "."],
                               ["wR", ".", ".", "bR"]]

    def test_ignores_commands_section_content(self):
        raw = "Board:\nwK .\n. bK\nCommands:\nprint board\nmove something"
        board = InputParser.parse(raw)
        assert board.rows == [["wK", "."], [".", "bK"]]

    def test_empty_commands_section(self):
        raw = "Board:\nwK .\n. bK\nCommands:"
        board = InputParser.parse(raw)
        assert board.rows == [["wK", "."], [".", "bK"]]

    def test_single_row_board(self):
        raw = "Board:\nwK . bK\nCommands:"
        board = InputParser.parse(raw)
        assert board.rows == [["wK", ".", "bK"]]