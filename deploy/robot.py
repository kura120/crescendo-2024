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
        self.speed = .5

        # SETUP - Left Motors
        self.motor_L1 = rev.CANSparkMax(1, self.brushless) 
        self.motor_L2 = rev.CANSparkMax(3, self.brushless)
        self.motors_L = wpilib.MotorControllerGroup(self.motor_L1, self.motor_L2)

        # SETUP - Right Motors
        self.motor_R1 = rev.CANSparkMax(2, self.brushless) 
        self.motor_R2 = rev.CANSparkMax(4, self.brushless)
        self.motors_R = wpilib.MotorControllerGroup(self.motor_R1, self.motor_R2)

        self.motors_R.setInverted(True)

        # SETUP - Motor details

        self.leftEncoder = self.motor_L1.getEncoder()
        self.rightEncoder = self.motor_R1.getEncoder()

        self.leftEncoder.setPosition(0)
        self.rightEncoder.setPosition(0)

        self.motor_L1.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)
        self.motor_R1.setIdleMode(rev.CANSparkMax.IdleMode.kCoast)

        self.joystick = wpilib.Joystick(0)

        self.drive = wpilib.drive.DifferentialDrive(self.motors_L, self.motors_R)     

        self.test_timer = wpilib.Timer() 

    def robotInit(self):
        pass

    def robotPeriodic(self):
        pass

    def robotDisabled(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        self.drive.tankDrive(self.joystick.getY() * self.speed, self.joystick.getRawAxis(5) * self.speed)

    def teleopExit(self):
        pass

    def autonomousExit(self):
        pass
