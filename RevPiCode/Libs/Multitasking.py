import time
import datetime
import ProfiBusCom

class RunProgram():
    def __init__(self, SecondsDelay):
        self.delay = SecondsDelay

    def NextRun(self, ProfiBus, y, u, AlarmList):
        now = datetime.datetime.now()
        next_minute = now.replace(second=self.delay) + datetime.timedelta(minutes=1)
        while datetime.datetime.now() < next_minute:
            time.sleep(2)  # Sleep for 1 second to avoid busy-waiting
            AlarmList[0] = not(AlarmList[0])
            ProfiBus.SendData(y,u, AlarmList)


