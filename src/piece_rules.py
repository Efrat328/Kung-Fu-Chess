class PieceMovementRules:
    """מגדירה, לכל סוג כלי, האם מהלך מסוים חוקי לפי צורת התזוזה שלו בלבד
    (row_diff, col_diff) - ללא תלות בלוח, בכלים אחרים, או במיקום בפועל."""

    @staticmethod
    def is_legal_move(piece_letter, from_pos, to_pos):
        """בודקת אם המהלך חוקי לפי סוג הכלי וההפרש בין המיקום ההתחלתי ליעד."""
        row_diff = to_pos[0] - from_pos[0]
        col_diff = to_pos[1] - from_pos[1]

        if piece_letter == "K":
            return PieceMovementRules._is_king_move(row_diff, col_diff)
        if piece_letter == "R":
            return PieceMovementRules._is_rook_move(row_diff, col_diff)
        if piece_letter == "B":
            return PieceMovementRules._is_bishop_move(row_diff, col_diff)
        if piece_letter == "Q":
            return PieceMovementRules._is_queen_move(row_diff, col_diff)
        if piece_letter == "N":
            return PieceMovementRules._is_knight_move(row_diff, col_diff)
        return False

    @staticmethod
    def _is_king_move(row_diff, col_diff):
        """מלך: צעד אחד בלבד בכל כיוון (כולל אלכסון), לא נשאר במקום."""
        return max(abs(row_diff), abs(col_diff)) == 1

    @staticmethod
    def _is_rook_move(row_diff, col_diff):
        """צריח: תזוזה ישרה בלבד (שורה קבועה או עמודה קבועה), לא נשאר במקום."""
        return (row_diff == 0) != (col_diff == 0)

    @staticmethod
    def _is_bishop_move(row_diff, col_diff):
        """רץ: תזוזה אלכסונית טהורה בלבד."""
        return row_diff != 0 and abs(row_diff) == abs(col_diff)

    @staticmethod
    def _is_queen_move(row_diff, col_diff):
        """מלכה: איחוד של תזוזת צריח ותזוזת רץ."""
        return (
            PieceMovementRules._is_rook_move(row_diff, col_diff)
            or PieceMovementRules._is_bishop_move(row_diff, col_diff)
        )

    @staticmethod
    def _is_knight_move(row_diff, col_diff):
        """פרש: צורת L - שילוב של 1 ו-2 בערך מוחלט (בכל סדר)."""
        return {abs(row_diff), abs(col_diff)} == {1, 2}