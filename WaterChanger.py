from time import sleep


class WaterChanger:
    def __init__(self, max_water_level, min_water_level):
        self.SLEEP_TIME = 2
        self.CURRENT_WATER_LEVEL = None
        self.MIN_WATER_LEVEL = min_water_level
        self.MAX_WATER_LEVEL = max_water_level

    def get_max_water_level(self):
        return self.MAX_WATER_LEVEL

    def start(self):
        print("Start Water Change!")
        print"Current Water Level : %.1f" % self.get_water_level_current()
        self.start_water_out()
        self.start_water_in()

    def start_water_out(self):
        print("Water Out Process!")
        while True:
            print(self.get_water_level_current())
            if self.get_water_level_current() >= self.MIN_WATER_LEVEL:
                print("Stop Water Change!")
                self.stop_water_out()
                break
            sleep(self.SLEEP_TIME)

    def start_water_in(self):
        print("Water In Process!")
        while True:
            print(self.get_water_level_current())
            if self.get_water_level_current() >= self.MAX_WATER_LEVEL:
                print("Stop Water In!")
                self.stop_water_out()
                break
            sleep(self.SLEEP_TIME)

    def get_water_level_current(self):
        return self.get_test_current()

    def get_test_current(self):
        with open("file.txt", "r") as f:
            test_value = f.readline()
        return float(test_value)

    def stop(self):
        pass

    def stop_water_out(self):
        print("Water Out Stopped!")
        pass
