import robotpy, wpilib, rev, ntcore

class MyRboot(wpilib.TimedRobot):

    def robotInit(self):
        self.motor = rev.CANSparkMax(1, rev.CANSparkLowLevel.MotorType.kBrushless)
        self.encoder = self.motor.getEncoder()

        self.speed = 0

        wpilib.SmartDashboard.putNumber("Speed", self.speed)

    def teleopPeriodic(self):
        self.motor.set(self.speed)
