from board import Board


class InputParser:
    """אחראית לקרוא stdin ולהפריד Board: מ-Commands:"""

    @staticmethod
    def _split_sections(raw_text):
        """מפצלת את הטקסט הגולמי לשורות הלוח ולשורות הפקודות."""
        lines = [line.strip() for line in raw_text.strip().splitlines()]
        board_index = lines.index("Board:")
        commands_index = lines.index("Commands:")
        board_lines = lines[board_index + 1 : commands_index]
        command_lines = lines[commands_index + 1 :]
        return board_lines, command_lines

    @staticmethod
    def parse(raw_text):
        """מקבלת טקסט גולמי, מחזירה Board object (עוד לא validated)"""
        board_lines, _ = InputParser._split_sections(raw_text)
        rows = [line.split() for line in board_lines]
        return Board(rows)

    @staticmethod
    def parse_commands(raw_text):
        """מקבלת טקסט גולמי, מחזירה רשימת פקודות כמחרוזות (בלי שורות ריקות)."""
        _, command_lines = InputParser._split_sections(raw_text)
        return [line for line in command_lines if line]