from piece_rules import PieceMovementRules
from pending_move import PendingMove
from move_queue import MoveQueue
from airborne_state import AirborneState

CELL_SIZE_PX = 100  # גודל כל תא בפיקסלים - קבוע קונפיגורציה, לא hardcoded בלוגיקה
MOVE_DURATION_MS_PER_CELL = 1000  # זמן ריצה (מ"ש) לכל תא מרחק במהלך - קבוע קונפיגורציה
JUMP_DURATION_MS = 1000  # משך זמן קפיצה (מ"ש) - קבוע קונפיגורציה


class Game:
    """מתאמת בין קליקים/קפיצות של המשתמש, כללי התזוזה של הכלים ותור המהלכים
    הממתינים. לא מכילה ידע ספציפי על סוגי כלים (זה ב-piece_rules) ולא על ניהול
    התור הפנימי (זה ב-move_queue) - רק את זרימת המשחק עצמה."""

    def __init__(self, board):
        self.board = board
        self.selected_pos = None
        self.clock_ms = 0
        self.move_queue = MoveQueue()
        self.game_over = False
        self.airborne = None

    def handle_click(self, x, y):
        """ממירה קואורדינטת פיקסלים לתא בלוח ומטפלת בבחירה/מהלך בהתאם.
        כלי שנמצא כרגע 'בתנועה' מתעלם מקליקים. אחרי סיום המשחק, כל קליק מתעלם."""
        if self.game_over:
            return
        row, col = self._pixels_to_cell(x, y)
        if not self.board.is_within_bounds(row, col):
            return
        if self.move_queue.is_position_busy((row, col)):
            return
        clicked_token = self.board.get_token(row, col)
        if self.selected_pos is None:
            self._select_if_piece(row, col, clicked_token)
        else:
            self._handle_click_with_selection(row, col, clicked_token)

    def handle_jump(self, x, y):
        """ממירה קואורדינטת פיקסלים לתא בלוח ומנסה להתחיל קפיצה של הכלי שם.
        כלי בתנועה לא יכול לקפוץ (חוק 5), ותא ריק (כולל כלי שכבר נתפס - חוק 6)
        מתעלם. הכלי נשאר פיזית באותו תא - רק 'מסומן' כבאוויר עד לזמן הנחיתה."""
        if self.game_over:
            return
        row, col = self._pixels_to_cell(x, y)
        if not self.board.is_within_bounds(row, col):
            return
        if self.move_queue.is_position_busy((row, col)):
            return
        token = self.board.get_token(row, col)
        if token == ".":
            return
        color = self.board.get_color(token)
        self.airborne = AirborneState((row, col), color, self.clock_ms + JUMP_DURATION_MS)

    def _pixels_to_cell(self, x, y):
        """ממירה קואורדינטת פיקסלים למספר שורה/עמודה בלוח."""
        return y // CELL_SIZE_PX, x // CELL_SIZE_PX

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
        """מבצעת בקשת מהלך: בודקת שאין כבר מהלך אחר פעיל על הלוח, שהמהלך חוקי
        לפי צורת התזוזה של הכלי, ושהנתיב פנוי (עבור כלים שדורשים זאת). אם הכל
        תקין - מוסיפה PendingMove לתור, שיושלם בפועל כשהשעון יגיע לזמן ההגעה שלו."""
        if not self.move_queue.is_empty():
            return
        token = self.board.get_token(*from_pos)
        piece_letter = token[1]
        color = self.board.get_color(token)
        target_occupied_by_enemy = self.board.get_token(*to_pos) != "."
        is_start_row = PieceMovementRules.is_pawn_start_row(color, from_pos[0], self.board.num_rows)

        is_legal = PieceMovementRules.is_legal_move(
            piece_letter, from_pos, to_pos,
            color=color, target_occupied_by_enemy=target_occupied_by_enemy,
            is_start_row=is_start_row
        )
        if not is_legal:
            return
        if PieceMovementRules.requires_clear_path(piece_letter):
            path_cells = PieceMovementRules.get_path_cells(from_pos, to_pos)
            if any(self.board.get_token(*cell) != "." for cell in path_cells):
                return

        distance = max(abs(to_pos[0] - from_pos[0]), abs(to_pos[1] - from_pos[1]))
        arrival_time = self.clock_ms + distance * MOVE_DURATION_MS_PER_CELL
        self.move_queue.add(PendingMove(from_pos, to_pos, token, arrival_time))

    def advance_clock(self, ms):
        """מקדמת את שעון המשחק, ומשלימה בפועל כל מהלך ממתין שהגיע זמנו - תוך
        בדיקה האם מהלך כלשהו 'נבלם' ע"י כלי באוויר (תפיסה הפוכה). אחרי הטיפול
        במהלכים, בודקת אם הכלי הקופץ נחת (חלון הקפיצה הסתיים)."""
        self.clock_ms += ms
        arrived_moves = self.move_queue.advance(self.clock_ms)
        for move in arrived_moves:
            if self._is_blocked_by_airborne(move):
                self._resolve_airborne_capture(move)
            else:
                self._complete_move(move)
        self._land_airborne_if_expired()

    def _is_blocked_by_airborne(self, move):
        """בודקת האם המהלך שהגיע מתנגש בכלי אויב שנמצא באוויר ביעד שלו."""
        if self.airborne is None:
            return False
        if self.airborne.position != move.to_pos:
            return False
        moving_color = self.board.get_color(move.token)
        return moving_color != self.airborne.color and self.airborne.is_active(self.clock_ms)

    def _resolve_airborne_capture(self, move):
        """מסירה מהלוח את הכלי המגיע (הוא נתפס ע"י הכלי הקופץ), שנשאר במקומו."""
        self.board.set_token(*move.from_pos, ".")

    def _land_airborne_if_expired(self):
        """מנקה את מצב ה'באוויר' אם חלון הקפיצה הסתיים - הכלי נוחת (נשאר במקומו)."""
        if self.airborne is not None and self.clock_ms >= self.airborne.until_time:
            self.airborne = None

    def _complete_move(self, move):
        """מבצעת בפועל על הלוח מהלך שהגיע זמנו. אם הכלי שנתפס הוא מלך,
        המשחק מסתיים. הכתרת חייל (אם רלוונטי) מטופלת ע"י PieceMovementRules."""
        captured_token = self.board.get_token(*move.to_pos)
        if captured_token != "." and captured_token[1] == "K":
            self.game_over = True
        self.board.set_token(*move.from_pos, ".")
        final_token = PieceMovementRules.apply_promotion(move.token, move.to_pos, self.board.num_rows)
        self.board.set_token(*move.to_pos, final_token)

    def get_board_output(self):
        """מחזירה את מצב הלוח הנוכחי כמחרוזת קנונית (לא כולל מהלכים ממתינים)."""
        return self.board.to_canonical_string()