
import robotpy, wpilib, phoenix5   

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.motor_timer = wpilib.Timer()
        self.CIM = phoenix5.TalonSRX(1)         # Replace ID with another number if 1 does not work.
        self.joystick = wpilib.Joystick(1)

    def testInit(self):
        self.motor_timer.start()

    def testPeriodic(self):
        if self.motor_timer.get() > 0.5: #seconds
            self.CIM.set(phoenix5.ControlMode.PercentOutput, 0)
        else:
            self.CIM.set(phoenix5.ControlMode.PercentOutput, 0.05)
        
    def testExit(self):
        self.motor_timer.stop()
        self.motor_timer.reset()