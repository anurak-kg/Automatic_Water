from Class.Log import Log
from Class.RedisDatabase import RedisDatabase
from MainApplication import MainApplication
from Module.Relay import Relay

if __name__ == "__main__":
    database = RedisDatabase()
    database.set_app_running(True)
    try:
        MainApplication()

    except KeyboardInterrupt:
        database.set_app_running(False)
        Log.new(Log.DEBUG, "###  Exit application! ###")
        print("Exiting....")
        print("Current App Status = " + str(database.get_app_running()))
        print("##########################")
        Relay.clear_relay()
        print("####### Clear relay ######")
        print("##########################")
        print("#######  Goodbye !!#######")
        print("##########################")
        raise
