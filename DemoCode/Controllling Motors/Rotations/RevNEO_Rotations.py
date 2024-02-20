import wpilib, rev

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.neo = rev.CANSparkMax(1, rev.CANSparkLowLevel.MotorType.kBrushless)
        