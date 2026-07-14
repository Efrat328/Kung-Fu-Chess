from piece_rules import PieceMovementRules
from pending_move import PendingMove

CELL_SIZE_PX = 100  # גודל כל תא בפיקסלים - קבוע קונפיגורציה, לא hardcoded בלוגיקה
MOVE_DURATION_MS_PER_CELL = 1000  # זמן ריצה (מ"ש) לכל תא מרחק במהלך - קבוע קונפיגורציה


class Game:
    """מנהלת את מצב המשחק - בחירת כלים, שליחת בקשות מהלך, מהלכים בתהליך (over time)
    וקידום השעון."""

    def __init__(self, board):
        self.board = board
        self.selected_pos = None
        self.clock_ms = 0
        self.pending_moves = []
        self.game_over = False

    def handle_click(self, x, y):
        """ממירה קואורדינטת פיקסלים לתא בלוח ומטפלת בבחירה/מהלך בהתאם.
        כלי שנמצא כרגע 'בתנועה' (יש לו מהלך ממתין) מתעלם מקליקים - לא ניתן
        להסיט אותו עד שהמהלך הנוכחי שלו מסתיים. אחרי סיום המשחק, כל קליק מתעלם."""
        if self.game_over:
            return
        row = y // CELL_SIZE_PX
        col = x // CELL_SIZE_PX
        if not self.board.is_within_bounds(row, col):
            return
        if self._is_busy(row, col):
            return
        clicked_token = self.board.get_token(row, col)
        if self.selected_pos is None:
            self._select_if_piece(row, col, clicked_token)
        else:
            self._handle_click_with_selection(row, col, clicked_token)

    def _is_busy(self, row, col):
        """בודקת האם יש מהלך ממתין שמקורו בתא הזה (כלי 'בדרך')."""
        return any(move.from_pos == (row, col) for move in self.pending_moves)

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
        """מבצעת בקשת מהלך: בודקת שאין כבר מהלך אחר פעיל על הלוח (רק מהלך אחד
        מותר בו-זמנית, לא משנה איזה כלי/צבע), שהמהלך חוקי לפי צורת התזוזה של
        הכלי, ושהנתיב פנוי (עבור כלים שדורשים זאת). אם הכל תקין - יוצרת
        PendingMove שיושלם בפועל רק כשהשעון יגיע לזמן ההגעה שלו."""
        if self.pending_moves:
            return
        token = self.board.get_token(*from_pos)
        piece_letter = token[1]
        color = self.board.get_color(token)
        target_occupied_by_enemy = self.board.get_token(*to_pos) != "."

        is_legal = PieceMovementRules.is_legal_move(
            piece_letter, from_pos, to_pos,
            color=color, target_occupied_by_enemy=target_occupied_by_enemy
        )
        if not is_legal:
            return
        if PieceMovementRules.requires_clear_path(piece_letter):
            path_cells = PieceMovementRules.get_path_cells(from_pos, to_pos)
            if any(self.board.get_token(*cell) != "." for cell in path_cells):
                return

        distance = max(abs(to_pos[0] - from_pos[0]), abs(to_pos[1] - from_pos[1]))
        arrival_time = self.clock_ms + distance * MOVE_DURATION_MS_PER_CELL
        self.pending_moves.append(PendingMove(from_pos, to_pos, token, arrival_time))

    def advance_clock(self, ms):
        """מקדמת את שעון המשחק, ומשלימה בפועל כל מהלך ממתין שהגיע זמנו."""
        self.clock_ms += ms
        arrived_moves = [m for m in self.pending_moves if m.has_arrived(self.clock_ms)]
        for move in arrived_moves:
            self._complete_move(move)
            self.pending_moves.remove(move)

    def _complete_move(self, move):
        """מבצעת בפועל על הלוח מהלך ממתין שהגיע זמנו. אם הכלי שנתפס הוא מלך,
        המשחק מסתיים - כל קליק עתידי יתעלם."""
        captured_token = self.board.get_token(*move.to_pos)
        if captured_token != "." and captured_token[1] == "K":
            self.game_over = True
        self.board.set_token(*move.from_pos, ".")
        self.board.set_token(*move.to_pos, move.token)

    def get_board_output(self):
        """מחזירה את מצב הלוח הנוכחי כמחרוזת קנונית (לא כולל מהלכים ממתינים)."""
        return self.board.to_canonical_string()