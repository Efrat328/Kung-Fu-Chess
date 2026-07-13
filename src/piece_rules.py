class PieceRule:
    """מחלקת בסיס - כל כלל תזוזה של כלי יורש ממנה ומממש את שתי המתודות."""

    def is_legal_move(self, color, from_pos, to_pos, target_occupied_by_enemy):
        """בודקת האם המהלך חוקי לפי כללי הכלי הספציפי. חייבת להיות ממומשת ע"י יורש."""
        raise NotImplementedError

    def requires_clear_path(self):
        """ברירת מחדל: הכלי לא דורש נתיב פנוי."""
        return False


class KingRule(PieceRule):
    def is_legal_move(self, color, from_pos, to_pos, target_occupied_by_enemy):
        row_diff = to_pos[0] - from_pos[0]
        col_diff = to_pos[1] - from_pos[1]
        return max(abs(row_diff), abs(col_diff)) == 1


class RookRule(PieceRule):
    def is_legal_move(self, color, from_pos, to_pos, target_occupied_by_enemy):
        row_diff = to_pos[0] - from_pos[0]
        col_diff = to_pos[1] - from_pos[1]
        return (row_diff == 0) != (col_diff == 0)

    def requires_clear_path(self):
        return True


class BishopRule(PieceRule):
    def is_legal_move(self, color, from_pos, to_pos, target_occupied_by_enemy):
        row_diff = to_pos[0] - from_pos[0]
        col_diff = to_pos[1] - from_pos[1]
        return row_diff != 0 and abs(row_diff) == abs(col_diff)

    def requires_clear_path(self):
        return True


class QueenRule(PieceRule):
    """מלכה: איחוד של תזוזת צריח ותזוזת רץ, דורש נתיב פנוי."""

    def __init__(self):
        self._rook = RookRule()
        self._bishop = BishopRule()

    def is_legal_move(self, color, from_pos, to_pos, target_occupied_by_enemy):
        return (
            self._rook.is_legal_move(color, from_pos, to_pos, target_occupied_by_enemy)
            or self._bishop.is_legal_move(color, from_pos, to_pos, target_occupied_by_enemy)
        )

    def requires_clear_path(self):
        return True


class KnightRule(PieceRule):
    def is_legal_move(self, color, from_pos, to_pos, target_occupied_by_enemy):
        row_diff = to_pos[0] - from_pos[0]
        col_diff = to_pos[1] - from_pos[1]
        return {abs(row_diff), abs(col_diff)} == {1, 2}


class PawnRule(PieceRule):
    """חייל: זז צעד אחד קדימה (לבן = למעלה, שחור = למטה) לתא ריק בלבד,
    או תופס באלכסון קדימה (רק אם יש אויב ביעד). לא יכול לתפוס ישר קדימה."""

    def is_legal_move(self, color, from_pos, to_pos, target_occupied_by_enemy):
        row_diff = to_pos[0] - from_pos[0]
        col_diff = to_pos[1] - from_pos[1]
        forward = -1 if color == "w" else 1

        if row_diff != forward:
            return False
        if col_diff == 0:
            return not target_occupied_by_enemy
        if abs(col_diff) == 1:
            return target_occupied_by_enemy
        return False


class PieceMovementRules:
    """נקודת גישה יחידה לכללי התזוזה - ממפה כל אות כלי לאובייקט הכלל שלה (Polymorphism)."""

    _RULES = {
        "K": KingRule(),
        "R": RookRule(),
        "B": BishopRule(),
        "Q": QueenRule(),
        "N": KnightRule(),
        "P": PawnRule(),
    }

    @staticmethod
    def is_legal_move(piece_letter, from_pos, to_pos, color=None, target_occupied_by_enemy=False):
        """color ו-target_occupied_by_enemy נדרשים בפועל רק עבור חייל;
        שאר הכלים מתעלמים מהם."""
        rule = PieceMovementRules._RULES.get(piece_letter)
        if rule is None:
            return False
        return rule.is_legal_move(color, from_pos, to_pos, target_occupied_by_enemy)

    @staticmethod
    def requires_clear_path(piece_letter):
        rule = PieceMovementRules._RULES.get(piece_letter)
        return rule.requires_clear_path() if rule else False

    @staticmethod
    def get_path_cells(from_pos, to_pos):
        row_diff = to_pos[0] - from_pos[0]
        col_diff = to_pos[1] - from_pos[1]
        steps = max(abs(row_diff), abs(col_diff))
        row_step = (row_diff > 0) - (row_diff < 0)
        col_step = (col_diff > 0) - (col_diff < 0)
        path_cells = []
        for i in range(1, steps):
            path_cells.append((from_pos[0] + row_step * i, from_pos[1] + col_step * i))
        return path_cells