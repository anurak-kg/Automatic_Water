import datetime

from Class.TimeOnOff import TimeOnOff
from Module.DHT11 import DHT11
from Module.Relay import Relay
from Module.UltraSensor import UltraSensor

relay_list = [Relay(name="Relay1",
                    gpio=26,
                    status=Relay.ACTIVATE,
                    time=[TimeOnOff(127, datetime.time(1, 0, 0), datetime.time(1, 20, 0))]),
              Relay(name="Relay2",
                    gpio=11,
                    status=Relay.ACTIVATE,
                    time=[TimeOnOff(128, datetime.time(3, 0, 0), datetime.time(3, 0, 0))])
              ]

relay = Relay(name="Relay2",
              gpio=11,
              status=Relay.ACTIVATE,
              time=[TimeOnOff(128, datetime.time(3, 0, 0), datetime.time(3, 0, 0)),
                    TimeOnOff(1, datetime.time(3, 0, 0), datetime.time(3, 0, 0))])

# print(Relay.insert_new_relay())
lists = Relay.get_relay_list()
#print len(lists)
for document in lists:
    print document
# print(datetime.time(3, 0, 0).strftime("%H:%M:%S"))
# print("logout: %i" % getattr(flags, day))
# print(type(getattr(flags, day)))
# print("ss")
# timer = Timer(relay_list=relay_list)
#
# statistic = Statistic()
# Log.new("Test")
# for i in range(1, 100):
#     statistic.update_and_save()
#     print("Saved!")
# # while True:
# #     timer.check()
# #     sleep(1)
#

#print TimeOnOff(128, datetime.time(3, 0, 0), datetime.time(3, 0, 0)).get_data_dict()
# print(dht11.get_temperature())
