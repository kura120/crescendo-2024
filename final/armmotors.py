'''
Arm
FRC 3340 Coding Team
'''


import robotpy, wpilib, wpilib.drive, rev, phoenix5
import math, time

class MyRobot(wpilib.TimedRobot):
    
    def robotInit(self):
        '''Runs on robot startup.'''
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

        # SETUP - Encoders
        self.encoder_A = self.motor_A.getEncoder()
        self.encoder_B = self.motor_B.getEncoder()
        self.calibrate_encoders()


        # Get Robot Controller
        self.controller = wpilib.XboxController(0)      

        # SETUP - Speed control
        self.idling_speed = 0   # Helps maintain arm position (the arm may sag due to weight)
        self.speed = 0.1    # Set percent output of motors (speed)

        # Define positional limit for robot arm on both sides.
        self.encoder_limit = 250

    def robotPeriodic(self):
        self.mean_encoder_position = (self.encoder_A.getPosition() + self.encoder_B.getPosition()) / 2

    def testInit(self):
        '''Runs when entering Test mode.'''
        self.calibrate_encoders()

    def testPeriodic(self):
        '''Test anything here. Runs periodically when Test mode is set on the Driver station.'''
        self.calibrate_encoders()

    def teleopPeriodic(self):
        '''Runs periodically during teleop phase.'''
        # REDUNDANCY - Get average encoder location for slightly better accuracy of arm location
        
        # Check if driver presses up or down on controller d-pad and if arm's location does not exceed limits
        # Motors should run at our defined speed when the d-pad is pressed, and stop when released
        if self.controller.getPOV() == 0 and (self.mean_encoder_position <= self.encoder_limit): 
            self.arm_motors.set(self.speed)
        elif self.controller.getPOV() == 180 and (self.mean_encoder_position <= -self.encoder_limit):
            self.arm_motors.set(-self.speed)
        else:
            # Run the motor backwards or forwards at a low speed to prevent the arm from lowering on its own.
            if self.mean_encoder_position < 0:
                self.arm_motors.set(self.idling_speed)
            else:
                self.arm_motors.set(-self.idling_speed)

        
    def calibrate_encoders(self):
        '''Calibrate encoders on demand. Should be called when the arm is at initial position, before autonomous, or when testing.'''
        self.encoder_A.setPosition(0)
        self.encoder_B.setPosition(0)

    def moveArm(self, direction):
        if abs(self.mean_encoder_position) <= 250:
            self.arm_motors.set(direction)
        

