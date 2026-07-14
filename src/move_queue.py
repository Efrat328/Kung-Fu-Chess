class MoveQueue:
    """מנהלת את רשימת המהלכים הממתינים (pending moves) - הוספה, קידום לפי זמן,
    ובדיקה האם מיקום מסוים 'תפוס' עקב מהלך ממתין שמקורו בו. Game לא ניגשת
    לרשימה הפנימית ישירות - רק דרך המתודות הציבוריות כאן."""

    def __init__(self):
        self._pending_moves = []

    def is_empty(self):
        """בודקת האם אין כרגע אף מהלך ממתין."""
        return len(self._pending_moves) == 0

    def add(self, move):
        """מוסיפה מהלך חדש לתור הממתינים."""
        self._pending_moves.append(move)

    def is_position_busy(self, position):
        """בודקת האם יש מהלך ממתין שמקורו במיקום הנתון (כלי 'בדרך')."""
        return any(move.from_pos == position for move in self._pending_moves)

    def advance(self, current_clock_ms):
        """מסירה מהתור את כל המהלכים שהגיע זמנם (לפי השעון הנוכחי) ומחזירה אותם."""
        arrived = [m for m in self._pending_moves if m.has_arrived(current_clock_ms)]
        for move in arrived:
            self._pending_moves.remove(move)
        return arrived