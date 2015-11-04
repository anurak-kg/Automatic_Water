import datetime

__author__ = 'Anurak'


def build_dict(seq, key):
    return dict((d[key], dict(d, index=i)) for (i, d) in enumerate(seq))


def time_in_range(start, end):
    current_time = datetime.datetime.today().time()
    if start <= end:
        return start <= current_time <= end
    else:
        return start <= current_time or current_time <= end


def print_terminal(ultra_sensor, water_temp, temperature, huminity):
    print(datetime.datetime.today())
    print "Distance : \t\t %.1f   Water Temp :\t %.1f  " % (ultra_sensor, water_temp)
    print "Temperature : \t %.1f   Humidity : \t %.1f " % (temperature, huminity)
