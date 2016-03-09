class TimeOnOff:
    time_on = None
    time_off = None
    day = None

    def __init__(self, day, time_on, time_off):
        self.time_off = time_off
        self.time_on = time_on
        self.day = day
