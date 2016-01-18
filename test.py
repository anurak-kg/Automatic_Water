from time import sleep, ctime, time

import threading

exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("กำลังดูดน้ำ " + self.name)
        sleep(self.counter)
        print("ดูดน้ำเสร็จ " + self.name)


thread1 = myThread(1, "Thread-1", 4)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
# thread1.start()
water_change_run = True
water_change_start = False
while True:
    print("In Looop")
    if water_change_run:

        if not water_change_start:
            if not thread1.isAlive():
                print("เริ่มเปลียนน้ำ")
                thread1.start()
                water_change_start = True
        else:
            if thread1.isAlive():
                print("เปลียนน้ำอยุ่")
            else:
                print("เปลี่ยนน้ำเสร็จ")
                water_change_run = False
    sleep(.5)
    # thread1.join()

print("Exiting Main Thread")
