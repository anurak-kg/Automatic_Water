from MainApplication import MainApplication
from RedisDatabase import RedisDatabase

if __name__ == "__main__":
    database = RedisDatabase()
    database.set_app_running(True)
    try:
        MainApplication()

    except KeyboardInterrupt:
        database.set_app_running(False)
        print("Exiting....")
        print("Current App Status = " + str(database.get_app_running()))
        raise
