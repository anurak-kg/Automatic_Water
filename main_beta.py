from Class.Log import Log
from Class.RedisDatabase import RedisDatabase
from MainApplication import MainApplication
from Module.Relay import Relay

if __name__ == "__main__":
    database = RedisDatabase()
    database.set_app_running(True)


    def exit_application():
        database.set_app_running(False)
        Log.new(Log.DEBUG, "###  Exit application! ###")
        Relay.clear_relay()

        print("Exiting....")
        print("Current App Status = " + str(database.get_app_running()))
        print("##########################")
        print("####### Clear relay ######")
        print("##########################")
        print("#######  Goodbye !!#######")
        print("##########################")


    try:
        MainApplication()

    except Exception, e:
        exit_application()
        print(e)
        raise
    finally:
        print("final")
        exit_application()
