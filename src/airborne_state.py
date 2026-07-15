class AirborneState:
    """מייצגת כלי שנמצא כרגע 'באוויר' (קפיצה) - נשאר פיזית באותו תא,
    אך פגיע/מגן במובן מיוחד עד לזמן הנחיתה (until_time)."""

    def __init__(self, position, color, until_time):
        self.position = position
        self.color = color
        self.until_time = until_time

    def is_active(self, current_clock_ms):
        """בודקת האם עדיין נמצא באוויר בשעון הנתון (כולל בדיוק ברגע הנחיתה)."""
        return current_clock_ms <= self.until_time