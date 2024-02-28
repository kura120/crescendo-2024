import robotpy, wpilib, wpilib.drive, rev, ntcore

class MyRboot(wpilib.TimedRobot):

    def robotInit(self):
        k = rev.CANSparkLowLevel.MotorType.kBrushless
        self.motor = rev.CANSparkMax(2, k)
        self.encoder = self.motor.getEncoder()

        self.speed = 0.

        wpilib.SmartDashboard.putNumber("Speed", self.speed)

    def robotPeriodic(self):
        self.speed = wpilib.SmartDashboard.getNumber("Speed", 0)
        wpilib.SmartDashboard.putNumber("Encoder", self.encoder.getPosition())

    def teleopPeriodic(self):
        self.motor.set(self.speed) 
