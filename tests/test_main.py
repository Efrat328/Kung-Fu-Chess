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

    def test_unknown_token_prints_error(self, monkeypatch, capsys):
        input_text = "Board:\nwK xZ\n. .\nCommands:"
        monkeypatch.setattr(sys, "stdin", io.StringIO(input_text))
        main()
        captured = capsys.readouterr()
        assert captured.out.strip() == "ERROR UNKNOWN_TOKEN"

    def test_click_and_move_end_to_end(self, monkeypatch, capsys):
        input_text = "Board:\nwK . .\n. . .\n. . .\nCommands:\nclick 50 50\nclick 150 150\nwait 1000\nprint board"
        monkeypatch.setattr(sys, "stdin", io.StringIO(input_text))
        main()
        captured = capsys.readouterr()
        assert captured.out.strip() == ". . .\n. wK .\n. . ."

    def test_jump_command_end_to_end(self, monkeypatch, capsys):
        input_text = "Board:\n. . .\nwK bR .\n. . .\nCommands:\njump 50 150\nclick 150 150\nclick 50 150\nwait 1000\nprint board"
        monkeypatch.setattr(sys, "stdin", io.StringIO(input_text))
        main()
        captured = capsys.readouterr()
        assert captured.out.strip() == ". . .\nwK . .\n. . ."