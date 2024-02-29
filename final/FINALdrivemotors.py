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
        self.speed = .5 #can change speed

        idle_mode = rev.CANSparkMax.IdleMode.kCoast

        # SETUP - Left Motors
        self.motor_L1 = rev.CANSparkMax(1, self.brushless) 
        self.motor_L2 = rev.CANSparkMax(3, self.brushless)
        self.motor_L1.setIdleMode(idle_mode)
        self.motor_L2.setIdleMode(idle_mode)
        self.motors_L = wpilib.MotorControllerGroup(self.motor_L1, self.motor_L2)


        # SETUP - Right Motors
        self.motor_R1 = rev.CANSparkMax(2, self.brushless) 
        self.motor_R2 = rev.CANSparkMax(4, self.brushless)
        self.motor_R1.setIdleMode(idle_mode)
        self.motor_R2.setIdleMode(idle_mode)
        self.motors_R = wpilib.MotorControllerGroup(self.motor_R1, self.motor_R2)

    

        # SETUP - Motor details

        self.leftEncoder = self.motor_L1.getEncoder()
        self.rightEncoder = self.motor_R1.getEncoder()

        self.leftEncoder.setPosition(0)
        self.rightEncoder.setPosition(0)



        self.joystick = wpilib.XboxController(0)

        self.robot = wpilib.drive.DifferentialDrive(
            self.motors_L, self.motors_R
            )
        
        self.test_timer = wpilib.Timer() 

    def robotPeriodic(self):
        pass

    def robotDisabled(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        self.robot.tankDrive(-self.joystick.getLeftY() * self.speed, -self.joystick.getRightY() * self.speed)

    def teleopExit(self):
        pass

    def autonomousExit(self):
        pass
