import datetime
import os
import time
from functools import wraps

from dateutil import parser

from Class.RedisDatabase import RedisDatabase

__author__ = 'Anurak'


def build_dict(seq, key):
    return dict((d[key], dict(d, index=i)) for (i, d) in enumerate(seq))


def time_in_range(start, end):
    # current_time = datetime.datetime.today().time()
    database = RedisDatabase()

    current_time = parser.parse(database.get("current_time")).time()
    print current_time
    if start <= end:
        return start <= current_time <= end
    else:
        return start <= current_time or current_time <= end


def print_terminal(ultra_sensor, water_temp, temperature, huminity):
    print(datetime.datetime.today())
    print "Distance : \t\t %.1f   Water Temp :\t %.1f  " % (ultra_sensor, water_temp)
    print "Temperature : \t %.1f   Humidity : \t %.1f " % (temperature, huminity)


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print("Total time running %s: %s seconds" % (function.func_name, str(t1 - t0)))
        return result

    return function_timer

def initial_mongodb():
    try:
        print("Initial Mongodb")
        # call("")
        os.system('sudo rm /var/lib/mongodb/mongod.lock')
        os.system('sudo service mongodb start')
    except Exception, e:
        print("That's work!")
        print(e)

def mode(nums):
    corresponding = {}
    occurances = []
    for i in nums:
        count = nums.count(i)
        corresponding.update({i: count})

    for i in corresponding:
        freq = corresponding[i]
        occurances.append(freq)

    maxFreq = max(occurances)

    keys = corresponding.keys()
    values = corresponding.values()

    index_v = values.index(maxFreq)
    global mode
    mode = keys[index_v]
    return mode
