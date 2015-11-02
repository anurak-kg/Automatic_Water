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


list = []


def add_add(gpio):
    list.append({'gpio': gpio, 'status': False})

def build_dict(seq, key):
    return dict((d[key], dict(d, index=i)) for (i, d) in enumerate(seq))

add_add(123)
add_add(545)
add_add(3)
d = build_dict(list, key="gpio")
print d[3]['index']

