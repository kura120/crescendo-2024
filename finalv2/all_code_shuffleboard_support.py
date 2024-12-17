'''
Final code
FRC 3340 Coding

This contains all the code created in this folder complied as one to be sent to the robot.
This also has support for network tables allowing for values to be sent to the comptuer (and modified on the fly)
'''

import robotpy, wpilib, wpilib.drive, ntcore, rev

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

        # SETUP: Controlling Maximum Percent Output (Speed) of motors. Can be hotfixed using network tables.
        self.drive_speed = 0.5                  #   Robot driving speed
        self.arm_speed = 0.1                    #   Robot arm speed
        self.climber_speed = 0.1                #   Robot climber speed for switching climber position
        self.intake_speed = 0.1                 #   Robot intake speed
        self.intake_reverse_speed = 0.1         #   Robot intake speed to secure note
        self.high_shot_speed = 0.25           #   Maximum shooter speed
        self.low_shot_speed = 0.1              #   Minimum shooter speed
        self.arm_idling_speed = 0
    

        idle_mode = [rev.CANSparkMax.IdleMode.kCoast, rev.CANSparkMax.IdleMode.kBrake]

        # SETUP - Left Motors, drive
        self.drive_motor_L1 = rev.CANSparkMax(1, self.brushless) 
        self.drive_motor_L2 = rev.CANSparkMax(3, self.brushless)
        self.drive_motor_L1.setIdleMode(idle_mode[0])
        self.drive_motor_L2.setIdleMode(idle_mode[0])
        self.drive_motors_L = wpilib.MotorControllerGroup(self.drive_motor_L1, self.drive_motor_L2)


        # SETUP - Right Motors, drive
        self.drive_motor_R1 = rev.CANSparkMax(2, self.brushless) 
        self.drive_motor_R2 = rev.CANSparkMax(4, self.brushless)
        self.drive_motor_R1.setIdleMode(idle_mode[0])
        self.drive_motor_R2.setIdleMode(idle_mode[0])
        self.drive_motors_r = wpilib.MotorControllerGroup(self.drive_motor_R1, self.drive_motor_R2)


        # SETUP - Arm Motors and Climber Motor
        self.arm_motor_A = rev.CANSparkMax(5, self.brushless) 
        self.arm_motor_B = rev.CANSparkMax(6, self.brushless)
        self.arm_motor_A.IdleMode(idle_mode[1])
        self.arm_motor_B.IdleMode(idle_mode[1])
        self.arm_motors = wpilib.MotorControllerGroup(self.arm_motor_A, self.arm_motor_B)

        self.climber_motor = rev.CANSparkMax(7, self.brushless)
        self.climber_motor.IdleMode(idle_mode[1])
        

        # SETUP - Intake and Shooter Motors
        self.intake_motor = rev.CANSparkMax(8, self.brushless)
        self.intake_motor.IdleMode(idle_mode[0])

        self.shooting_motor_A = rev.CANSparkMax(9, self.brushless)
        self.shooting_motor_B = rev.CANSparkMax(10, self.brushless)

        self.shooting_motor_A.IdleMode(idle_mode[0])
        self.shooting_motor_B.IdleMode(idle_mode[0])


        # SETUP - Encoders
        self.left_encoders = [self.drive_motor_L1.getEncoder(), self.drive_motor_L2.getEncoder()]
        self.right_encoders = [self.drive_motor_R1.getEncoder(), self.drive_motor_R2.getEncoder()]
        self.arm_encoders = [self.arm_motor_A.getEncoder(), self.arm_motor_B.getEncoder()]

        
        # Setup: Robot Control
        self.joystick = wpilib.XboxController(0)    # Connect to a joystick. Specify: PS4Controller, PS5Controller Joystick (flightstick), XboxController
        self.robot = wpilib.drive.DifferentialDrive(self.drive_motors_L, self.drive_motors_r)       # Setup Robot Drive System
        

        # Timers
        self.intake_reverse_timer = wpilib.Timer()


        # Calculation parameters
        wheel_gearbox_ratio = 14
        self.wheel_rotation = (42 * wheel_gearbox_ratio) / (6 * math.pi) # Breakdown: (42 encoder counts / gearbox ratio) * wheel circumference

        arm_gearbox_ratio = 100    # TODO: Find out gearbox ratio 

    def robotPeriodic(self):
        wpilib.SmartDashboard.putNumber("E")

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

    def releaseIntake(self):
        pass