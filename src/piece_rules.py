class PieceRule:
    """מחלקת בסיס - כל כלל תזוזה של כלי יורש ממנה ומממש את שתי המתודות."""

    def is_legal_move(self, color, from_pos, to_pos, target_occupied_by_enemy, is_start_row=False):
        """בודקת האם המהלך חוקי לפי כללי הכלי הספציפי. חייבת להיות ממומשת ע"י יורש."""
        raise NotImplementedError

    def requires_clear_path(self):
        """ברירת מחדל: הכלי דורש נתיב פנוי. עבור כלי שנע צעד אחד בלבד (מלך, חייל
        בצעד רגיל) זה לא משנה בפועל כי אין תאים 'בדרך'. רק פרש (שקופץ) חורג מכך."""
        return True


class KingRule(PieceRule):
    """מלך: צעד אחד בלבד בכל כיוון (כולל אלכסון)."""

    def is_legal_move(self, color, from_pos, to_pos, target_occupied_by_enemy, is_start_row=False):
        row_diff = to_pos[0] - from_pos[0]
        col_diff = to_pos[1] - from_pos[1]
        return max(abs(row_diff), abs(col_diff)) == 1


class RookRule(PieceRule):
    """צריח: תזוזה ישרה בלבד (שורה קבועה או עמודה קבועה), דורש נתיב פנוי."""

    def is_legal_move(self, color, from_pos, to_pos, target_occupied_by_enemy, is_start_row=False):
        row_diff = to_pos[0] - from_pos[0]
        col_diff = to_pos[1] - from_pos[1]
        return (row_diff == 0) != (col_diff == 0)


class BishopRule(PieceRule):
    """רץ: תזוזה אלכסונית טהורה בלבד, דורש נתיב פנוי."""

    def is_legal_move(self, color, from_pos, to_pos, target_occupied_by_enemy, is_start_row=False):
        row_diff = to_pos[0] - from_pos[0]
        col_diff = to_pos[1] - from_pos[1]
        return row_diff != 0 and abs(row_diff) == abs(col_diff)


class QueenRule(PieceRule):
    """מלכה: איחוד של תזוזת צריח ותזוזת רץ, דורש נתיב פנוי."""

    def __init__(self):
        self._rook = RookRule()
        self._bishop = BishopRule()

    def is_legal_move(self, color, from_pos, to_pos, target_occupied_by_enemy, is_start_row=False):
        return (
            self._rook.is_legal_move(color, from_pos, to_pos, target_occupied_by_enemy)
            or self._bishop.is_legal_move(color, from_pos, to_pos, target_occupied_by_enemy)
        )


class KnightRule(PieceRule):
    """פרש: צורת L - שילוב של 1 ו-2 בערך מוחלט (בכל סדר). לא דורש נתיב פנוי - קופץ."""

    def is_legal_move(self, color, from_pos, to_pos, target_occupied_by_enemy, is_start_row=False):
        row_diff = to_pos[0] - from_pos[0]
        col_diff = to_pos[1] - from_pos[1]
        return {abs(row_diff), abs(col_diff)} == {1, 2}

    def requires_clear_path(self):
        return False


class PawnRule(PieceRule):
    """חייל: זז צעד אחד קדימה (לבן = למעלה, שחור = למטה) לתא ריק בלבד, או שני
    תאים קדימה אם נמצא בשורת ההתחלה שלו (נתיב פנוי נבדק גנרית ב-Game).
    תופס באלכסון קדימה בלבד (רק אם יש אויב ביעד) - לא יכול לתפוס ישר קדימה."""

    def is_legal_move(self, color, from_pos, to_pos, target_occupied_by_enemy, is_start_row=False):
        row_diff = to_pos[0] - from_pos[0]
        col_diff = to_pos[1] - from_pos[1]
        forward = -1 if color == "w" else 1

        if col_diff == 0:
            if row_diff == forward:
                return not target_occupied_by_enemy
            if row_diff == 2 * forward and is_start_row:
                return not target_occupied_by_enemy
            return False
        if abs(col_diff) == 1 and row_diff == forward:
            return target_occupied_by_enemy
        return False

    @staticmethod
    def get_start_row(color, num_rows):
        """מחזירה את מספר שורת ההתחלה של חייל בצבע הנתון (לבן=תחתונה, שחור=עליונה)."""
        return num_rows - 1 if color == "w" else 0

    @staticmethod
    def get_promotion_row(color, num_rows):
        """מחזירה את מספר השורה שבה חייל בצבע הנתון מוכתר למלכה."""
        return 0 if color == "w" else num_rows - 1


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
    def is_legal_move(piece_letter, from_pos, to_pos, color=None,
                       target_occupied_by_enemy=False, is_start_row=False):
        """בודקת אם המהלך חוקי לפי סוג הכלי. color, target_occupied_by_enemy
        ו-is_start_row נדרשים בפועל רק עבור חייל; שאר הכלים מתעלמים מהם."""
        rule = PieceMovementRules._RULES.get(piece_letter)
        if rule is None:
            return False
        return rule.is_legal_move(color, from_pos, to_pos, target_occupied_by_enemy, is_start_row)

    @staticmethod
    def requires_clear_path(piece_letter):
        """בודקת האם סוג הכלי דורש נתיב פנוי."""
        rule = PieceMovementRules._RULES.get(piece_letter)
        return rule.requires_clear_path() if rule else False

    @staticmethod
    def get_path_cells(from_pos, to_pos):
        """מחזירה את כל התאים שבדרך בין from_pos ל-to_pos, לא כולל שתי הנקודות עצמן.
        מניחה מהלך ישר או אלכסוני תקין (כפי שכבר אומת ע"י is_legal_move)."""
        row_diff = to_pos[0] - from_pos[0]
        col_diff = to_pos[1] - from_pos[1]
        steps = max(abs(row_diff), abs(col_diff))

        row_step = (row_diff > 0) - (row_diff < 0)  # -1, 0 או 1
        col_step = (col_diff > 0) - (col_diff < 0)

        path_cells = []
        for i in range(1, steps):
            path_cells.append((from_pos[0] + row_step * i, from_pos[1] + col_step * i))
        return path_cells

    @staticmethod
    def is_pawn_start_row(color, row, num_rows):
        """בודקת האם השורה הנתונה היא שורת ההתחלה של חייל בצבע הנתון.
        מחזירה False עבור צבע לא מוכר (לא 'w' ולא 'b')."""
        if color not in ("w", "b"):
            return False
        return row == PawnRule.get_start_row(color, num_rows)

    @staticmethod
    def apply_promotion(token, to_pos, num_rows):
        """מחזירה טוקן מוכתר (מלכה, באותו צבע) אם הטוקן הוא חייל שהגיע לשורה
        האחרונה שלו; אחרת מחזירה את הטוקן ללא שינוי."""
        color, piece_letter = token[0], token[1]
        if piece_letter != "P":
            return token
        if to_pos[0] == PawnRule.get_promotion_row(color, num_rows):
            return color + "Q"
        return token