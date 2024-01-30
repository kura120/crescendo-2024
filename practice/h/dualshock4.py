import robotpy, wpilib

class MyRobot(wpilib.TimedRobot):
    
    def robotInit(self):
        self.dualshock = wpilib.PS4Controller(0)
        