# TODO: insert robot code here
import robotpy, wpilib, phoenix5 

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.CIM = phoenix5.TalonSRX(1)

    def robotPeriodic(self):
        print(self.CIM.getSelectedSensorPosition(1))