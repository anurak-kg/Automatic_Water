class TimeOnOff(object):
    time_on = None
    time_off = None
    day = None

    def __init__(self, day, time_on, time_off):
        self.time_off = time_off
        self.time_on = time_on
        self.day = day

    def get_data_dict(self):
        return {'day': self.day, 'time_off': self.time_on.strftime("%H:%M:%S"),
                'time_on': self.time_off.strftime("%H:%M:%S")}
