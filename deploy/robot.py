'''
Intake
FRC 3340 Coding Team
'''


import robotpy, wpilib, wpilib.drive, rev, phoenix5
import math, time

class MyRobot(wpilib.TimedRobot):
    
    def robotInit(self):
        # Getting motors ready: each set of wheels has two motors powering it.
        # One side has to be inverted so that the robot moves forward instead of turning in place.
        self.brushless =  rev.CANSparkLowLevel.MotorType.kBrushless

        # SETUP - Motors
        self.motor_A = rev.CANSparkMax(2, self.brushless) 
        self.motor_B = rev.CANSparkMax(4, self.brushless)

        #Idle mode: brake
        idle_mode = rev.CANSparkMax.IdleMode.kBrake
        self.motor_A.setIdleMode(idle_mode)
        self.motor_B.setIdleMode(idle_mode)

        self.arm_motors = wpilib.MotorControllerGroup(self.motor_A, self.motor_B)

        self.encoder_A = self.motor_A.getEncoder()
        self.encoder_B = self.motor_B.getEncoder()


        #check player number
        self.controller = wpilib.XboxController(0)      
        self.speed = 0.1 #CONTROL SPEED HERE

        self.encoder_limit = 250
        self.hit_limit = False


    def teleopInit(self):
        self.calibrate_encoders()

    def teleopPeriodic(self):

        
        if self.controller.getPOV() == 0 and ((self.encoder_A.getPosition() + self.encoder_B.getPosition())/2 <= 250): 
            self.arm_motors.set(self.speed)
        elif self.controller.getPOV() == 180 and ((self.encoder_A.getPosition() + self.encoder_B.getPosition())/2 >= -250):
            self.arm_motors.set(-self.speed)
        else:
            self.arm_motors.set(0)

        if abs((self.encoder_A.getPosition() + self.encoder_B.getPosition())/2) >= 250 and not(self.hit_limit): 
            self.controller.setRumble(self.controller.RumbleType.kLeftRumble, 0.01)
            self.hit_limit = True
        else:
            self.controller.setRumble(self.controller.RumbleType.kLeftRumble, 0)
            self.hit_limit = False
        

        

    def calibrate_encoders(self):
        self.encoder_A.setPosition(0)
        self.encoder_B.setPosition(0)
