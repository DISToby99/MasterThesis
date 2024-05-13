import time
import datetime
import ProfiBusCom

class RunProgram():
    def __init__(self, SecondsDelay):
        """Initialize the RunProgram class."""
        self.delay = SecondsDelay  # Set the delay in seconds

    def NextRun(self, ProfiBus, y, u, AlarmList):
        """Schedule the next run of the program."""
        now = datetime.datetime.now()  # Get current time
        # Calculate the time of the next run
        next_minute = now.replace(second=self.delay) + datetime.timedelta(minutes=1)
        # Wait until the next minute
        while datetime.datetime.now() < next_minute:
            time.sleep(2)  # Sleep for 2 seconds to avoid busy-waiting
            # Toggle the first element of AlarmList (The watchDog)
            AlarmList[0] = not AlarmList[0]
            # Send data over ProfiBus
            ProfiBus.SendData(y, u, AlarmList)
