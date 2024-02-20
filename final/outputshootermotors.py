'''
FINAL CODE
FRC 3340 Coding Team
'''


import robotpy, wpilib, wpilib.drive, rev, phoenix5
import math, time

class MyRobot(wpilib.TimedRobot):
    
    def robotInit(self):
        # Getting motors ready: each set of wheels has two motors powering it.
        # One side has to be inverted so that the robot moves forward instead of turning in place.
        self.brushless =  rev.CANSparkLowLevel.MotorType.kBrushless

        # SETUP - Left Motor
        self.motor_L1 = rev.CANSparkMax(5, self.brushless) 

        # SETUP - Right Motor
        self.motor_R1 = rev.CANSparkMax(6, self.brushless) 
        self.motors_R.setInverted(True)

        # SETUP - Motor details
        self.leftEncoder = self.motor_L1.getEncoder()
        self.rightEncoder = self.motor_R1.getEncoder()

        self.leftEncoder.setPosition(0)
        self.rightEncoder.setPosition(0)

        self.motor_L1.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)
        self.motor_R1.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)

        self.joystick = wpilib.Joystick(0)      


    def robotPeriodic(self):
        wpilib.SmartDashboard.putNumber("Left Encoder", self.leftEncoder.getPosition())
        wpilib.SmartDashboard.putNumber("Right Encoder", self.rightEncoder.getPosition())


    def disabledInit(self):
        self.motor_L1.set(0)
        

    def testPeriodic(self):
        if abs(self.joystick.getY()) > 0.1: #Analog input with floats
            self.motor_L1.set(self.joystick.getY())
        else:
             self.motor_L1.set(0)
        if self.joystick.getRawButton(1):
            self.motor_L1.set(0.1)
        else:
            self.motor_L1.set(0)


if __name__ == "__main__":
    wpilib.run(MyRobot)