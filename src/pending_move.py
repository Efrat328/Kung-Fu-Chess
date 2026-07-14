class PendingMove:
    """מייצגת מהלך שנשלח אך טרם הסתיים - יש לו כלי, מקור, יעד וזמן הגעה
    (arrival_time, לפי שעון המשחק). עד להגעה, הלוח בפועל לא משתנה."""

    def __init__(self, from_pos, to_pos, token, arrival_time):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.token = token
        self.arrival_time = arrival_time

    def has_arrived(self, current_clock_ms):
        """בודקת האם השעון הנוכחי הגיע/עבר את זמן ההגעה של המהלך."""
        return current_clock_ms >= self.arrival_time