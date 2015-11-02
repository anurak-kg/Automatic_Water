def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
import datetime
start = datetime.time(20, 0, 0)
end = datetime.time(1, 0, 0)
on_off =  time_in_range(start, end, datetime.datetime.today().time())
if on_off :
    print "On"
else:
    print "Off"
