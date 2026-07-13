from piece_rules import PieceMovementRules

CELL_SIZE_PX = 100  # גודל כל תא בפיקסלים - קבוע קונפיגורציה, לא hardcoded בלוגיקה


class Game:
    """מנהלת את מצב המשחק - בחירת כלים, שליחת בקשות מהלך וקידום השעון."""

    def __init__(self, board):
        self.board = board
        self.selected_pos = None
        self.clock_ms = 0

    def handle_click(self, x, y):
        """ממירה קואורדינטת פיקסלים לתא בלוח ומטפלת בבחירה/מהלך בהתאם."""
        row = y // CELL_SIZE_PX
        col = x // CELL_SIZE_PX
        if not self.board.is_within_bounds(row, col):
            return
        clicked_token = self.board.get_token(row, col)
        if self.selected_pos is None:
            self._select_if_piece(row, col, clicked_token)
        else:
            self._handle_click_with_selection(row, col, clicked_token)

    def _select_if_piece(self, row, col, token):
        """בוחרת כלי אם התא לא ריק; מתעלמת מתא ריק."""
        if token != ".":
            self.selected_pos = (row, col)

    def _handle_click_with_selection(self, row, col, token):
        """כשיש כבר בחירה - מחליפה אותה אם זה כלי ידידותי, אחרת שולחת בקשת מהלך."""
        selected_token = self.board.get_token(*self.selected_pos)
        if token != "." and self.board.get_color(token) == self.board.get_color(selected_token):
            self.selected_pos = (row, col)
        else:
            self._request_move(self.selected_pos, (row, col))
            self.selected_pos = None

    def _request_move(self, from_pos, to_pos):
        """מבצעת בקשת מהלך: בודקת אם המהלך חוקי לפי צורת התזוזה של הכלי
        ושהנתיב פנוי (עבור כלים שדורשים זאת), ואם כן - מבצעת אותו מיידית
        (ללא זמן ריצה כרגע). מהלך לא חוקי או חסום מתעלם."""
        token = self.board.get_token(*from_pos)
        piece_letter = token[1]
        if not PieceMovementRules.is_legal_move(piece_letter, from_pos, to_pos):
            return
        if PieceMovementRules.requires_clear_path(piece_letter):
            path_cells = PieceMovementRules.get_path_cells(from_pos, to_pos)
            if any(self.board.get_token(*cell) != "." for cell in path_cells):
                return
        self.board.set_token(*from_pos, ".")
        self.board.set_token(*to_pos, token)

    def advance_clock(self, ms):
        """מקדמת את שעון המשחק. כרגע אין השפעה על מהלכים ממתינים -
        באיטרציות עתידיות ישמש לחישוב זמני סיום מהלכים."""
        self.clock_ms += ms

    def get_board_output(self):
        """מחזירה את מצב הלוח הנוכחי כמחרוזת קנונית."""
        return self.board.to_canonical_string()