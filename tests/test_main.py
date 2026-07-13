# tests/test_main.py
import io
import sys
from main import main


class TestMainIntegration:
    def test_valid_board_prints_canonical_form(self, monkeypatch, capsys):
        input_text = "Board:\nwK . . bK\n. . . .\nwR . . bR\nCommands:\nprint board"
        monkeypatch.setattr(sys, "stdin", io.StringIO(input_text))

        main()

        captured = capsys.readouterr()
        assert captured.out.strip() == "wK . . bK\n. . . .\nwR . . bR"

    def test_piece_tokens_and_colors_prints_canonical_form(self, monkeypatch, capsys):
        input_text = "Board:\nwK . bQ\n. wN .\nbP . wR\nCommands:\nprint board"
        monkeypatch.setattr(sys, "stdin", io.StringIO(input_text))

        main()

        captured = capsys.readouterr()
        assert captured.out.strip() == "wK . bQ\n. wN .\nbP . wR"

    def test_unknown_token_prints_error(self, monkeypatch, capsys):
        input_text = "Board:\nwK xZ\n. .\nCommands:"
        monkeypatch.setattr(sys, "stdin", io.StringIO(input_text))

        main()

        captured = capsys.readouterr()
        assert captured.out.strip() == "ERROR UNKNOWN_TOKEN"

    def test_row_width_mismatch_prints_error(self, monkeypatch, capsys):
        input_text = "Board:\nwK . .\n. bK\nCommands:"
        monkeypatch.setattr(sys, "stdin", io.StringIO(input_text))

        main()

        captured = capsys.readouterr()
        assert captured.out.strip() == "ERROR ROW_WIDTH_MISMATCH"

    def test_click_and_move_end_to_end(self, monkeypatch, capsys):
        input_text = "Board:\nwK . .\n. . .\n. . .\nCommands:\nclick 50 50\nclick 150 150\nwait 1000\nprint board"
        monkeypatch.setattr(sys, "stdin", io.StringIO(input_text))

        main()

        captured = capsys.readouterr()
        assert captured.out.strip() == ". . .\n. wK .\n. . ."