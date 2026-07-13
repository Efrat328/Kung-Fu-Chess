class BoardParseError(Exception):
    def __init__(self, error_code):
        self.error_code = error_code


class Board:
    def __init__(self, rows):
        """מקבלת רשימת שורות (list of lists של טוקנים) ומחשבת את מספר השורות/עמודות."""
        self.rows = rows
        self.num_rows = len(self.rows)
        self.num_cols = len(self.rows[0]) if self.num_rows > 0 else 0

    def validate(self):
        """בודקת שכל הטוקנים בלוח חוקיים וכל השורות באותו אורך.
        זורקת BoardParseError אם משהו לא תקין."""
        for row in self.rows:
            for token in row:
                if not self._is_valid_token(token):
                    raise BoardParseError("UNKNOWN_TOKEN")
        expected_width = self.num_cols
        for i, row in enumerate(self.rows):
            if len(row) != expected_width:
                raise BoardParseError("ROW_WIDTH_MISMATCH")

    def to_canonical_string(self):
        """מחזירה את הלוח כמחרוזת בפורמט הפלט (שורות מופרדות ב-\\n, טוקנים ברווח)."""
        return "\n".join(" ".join(row) for row in self.rows)

    def _is_valid_token(self, token):
        """בודקת האם טוקן בודד חוקי - '.' או צירוף צבע+סוג כלי (למשל 'wK')."""
        if token == ".":
            return True
        if len(token) != 2:
            return False
        color, piece = token[0], token[1]
        return color in {"w", "b"} and piece in {"K", "Q", "R", "B", "N", "P"}

    def is_within_bounds(self, row, col):
        """בודקת אם קואורדינטת שורה/עמודה נמצאת בתוך גבולות הלוח."""
        return 0 <= row < self.num_rows and 0 <= col < self.num_cols

    def get_token(self, row, col):
        """מחזירה את הטוקן בתא נתון."""
        return self.rows[row][col]

    def set_token(self, row, col, token):
        """מעדכנת את הטוקן בתא נתון."""
        self.rows[row][col] = token

    def get_color(self, token):
        """מחזירה את צבע הכלי ('w'/'b') או None אם התא ריק."""
        return None if token == "." else token[0]