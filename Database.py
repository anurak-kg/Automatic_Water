import redis as client

from DisplayScreen import DisplayScreen


class Database:
    server_ip = "localhost"
    server_port = 6379
    SCREEN_MODE = "screen_location"
    WATER_LEVEL = "water_level"
    SCREEN_RUNNING = "screen_running"

    def __init__(self, server_ip="localhost", port=6379, db=0):
        self.redis = client.StrictRedis(server_ip, port)

    def test_connect(self):
        self.redis.set(self.SCREEN_MODE, DisplayScreen.MAIN)
        print(self.redis.get(self.SCREEN_MODE))

    def set_water_level(self, level):
        self.redis.set(self.WATER_LEVEL, level)

    def get_water_level(self):
        return self.redis.get(self.WATER_LEVEL)

    def set_screen_mode(self, mode):
        self.redis.set(self.SCREEN_MODE, mode)

    def get_screen_mode(self):
        return int(self.redis.get(self.SCREEN_MODE))

    def set_screen_running(self, mode):
        if mode:
            self.redis.set(self.SCREEN_RUNNING, "True")
        else:
            self.redis.set(self.SCREEN_RUNNING, "False")

    def get_screen_running(self):
        if self.redis.get(self.SCREEN_RUNNING) == "True":
            return True
        else:
            return False
