import robotpy, wpilib, wpilib.drive, rev, math, phoenix5

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.cim_motor = phoenix5.TalonSRX(0)

    def testPeriodic(self):
        self.cim_motor.set(0.1) 