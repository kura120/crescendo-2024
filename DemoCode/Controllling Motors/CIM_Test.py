import wpilib, phoenix5   

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.CIM = phoenix5.TalonSRX(1)         # Replace ID with another number if 1 does not work.
        self.joystick = wpilib.Joystick(1)

    def testPeriodic(self):
        self.CIM.set(phoenix5.ControlMode.PercentOutput, 0.1)