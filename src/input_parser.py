from board import Board
class InputParser:
    """אחראית לקרוא stdin ולהפריד Board: מ-Commands:"""
    
    @staticmethod
    def parse(raw_text):
        """מקבלת טקסט גולמי, מחזירה Board object (עוד לא validated)"""
        lines = raw_text.strip().splitlines()
        
        board_index = lines.index("Board:")
        commands_index = lines.index("Commands:")
        
        board_lines = lines[board_index + 1 : commands_index]
        
        rows = [line.split() for line in board_lines]
        return Board(rows)