'''
Final code
FRC 3340 Coding

This contains all the code created in this folder complied as one to be sent to the robot.
This also has support for network tables allowing for values to be sent to the comptuer (and modified on the fly)
'''

import robotpy, wpilib, wpilib.drive, math, ntcore, rev


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Getting motors ready: each set of wheels has two motors powering it.
        # One side has to be inverted so that the robot moves forward instead of turning in place.
        self.brushless =  rev.CANSparkLowLevel.MotorType.kBrushless

        # SETUP: Controlling Default Percent Output (Speed) of motors. Some can be hotfixed using SmartDashboard, but change values here.
        self.drive_speed = 0.5                  #   Robot driving speed                                     (SmartDashboard)
        self.arm_speed = 0.1                    #   Robot arm speed                                         (SmartDashboard)
        self.climber_speed = 0.1                #   Robot climber speed for switching climber position      (Hardcode)
        self.intake_speed = 0.1                 #   Robot intake speed                                      (SmartDashboard)
        self.intake_reverse_speed = 0.1         #   Robot intake speed to secure note                       (Hardcode)
        self.intake_reverse_duration = 0.1      #   Robot intake duration to secure note                    (Hardcode)
        self.strong_shot_speed = 0.25           #   Maximum shooter speed                                   (Hardcode)
        self.weak_shot_speed = 0.1              #   Minimum shooter speed                                   (Hardcode)
        self.shot_delay = 5                     #   Delay between starting outtake and shot                 (Hardcode)
        self.arm_idling_speed = 0

        self.arm_encoder_limit = 250            # (Hardcode)

        self.camera = wpilib.CameraServer.launch()      

        idle_mode = [rev.CANSparkMax.IdleMode.kCoast, rev.CANSparkMax.IdleMode.kBrake]

        '''
        Motor ID guide:
        1-4: Drive
        5-7: Arm/Climber
        8-10: Intake/Outtake

        Be sure to reflash any motor controllers using REV client (orange R) if necessary, or switch IDs.
        '''

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
        self.drive_motors_R = wpilib.MotorControllerGroup(self.drive_motor_R1, self.drive_motor_R2)


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
        self.intake_motor.setInverted(True)

        self.shooting_motor_A = rev.CANSparkMax(9, self.brushless)
        self.shooting_motor_B = rev.CANSparkMax(10, self.brushless)

        self.shooting_motor_A.IdleMode(idle_mode[0])
        self.shooting_motor_B.IdleMode(idle_mode[0])

        self.shooting_motors = wpilib.MotorControllerGroup(self.shooting_motor_A, self.shooting_motor_B)
        self.shooting_motors.setInverted(True)


        # SETUP - Encoders
        self.left_encoders = [self.drive_motor_L1.getEncoder(), self.drive_motor_L2.getEncoder()]
        self.right_encoders = [self.drive_motor_R1.getEncoder(), self.drive_motor_R2.getEncoder()]
        self.arm_encoders = [self.arm_motor_A.getEncoder(), self.arm_motor_B.getEncoder()]
        self.climber_encoder = self.climber_motor.getEncoder()
        
        # Setup: Robot Control
        self.controller = wpilib.PS4Controller(0)    # Connect to a joystick. Specify: PS4Controller, PS5Controller Joystick (flightstick), XboxController
        self.robot = wpilib.drive.DifferentialDrive(self.drive_motors_L, self.drive_motors_R)       # Setup Robot Drive System
        
        # Timers
        self.intake_reverse_timer = wpilib.Timer()
        self.shot_timer = wpilib.Timer()

        # Calculation parameters
        wheel_gearbox_ratio = 14
        self.wheel_distance_per_rotation = (42 * wheel_gearbox_ratio) / (6 * math.pi) # Breakdown: (42 encoder counts / gearbox ratio) * wheel circumference, inches

        # Boolean values
        self.note_shot = False
        self.intake_active = False            

        # Parameters that can be modified on SmartDashboard
        wpilib.SmartDashboard.putNumber("Maximum Drive Speed", (self.drive_speed * 100))
        wpilib.SmartDashboard.putNumber("Maximum Arm Power", (self.arm_speed * 100))
        wpilib.SmartDashboard.putNumber("Shot Timer", 5 - self.shot_timer.get())


    def robotPeriodic(self):
        # SmartDashboard Stats
        wpilib.SmartDashboard.putNumber("Left Encoder Average", (self.left_encoders[0].getPosition() + self.left_encoders[1].getPosition() / 2))
        wpilib.SmartDashboard.putNumber("Right Encoder Average", (self.right_encoders[0].getPosition() + self.right_encoders[1].getPosition() / 2))
        wpilib.SmartDashboard.putNumber("Arm Encoder Average", (self.arm_encoders[0].getPosition() + self.arm_encoders[1].getPosition() / 2))
        wpilib.SmartDashboard.putNumber("Climber Encoder", self.climber_encoder.getPosition())

        wpilib.SmartDashboard.putNumber("Outtake Power", (self.shooting_motors.get() * 100))
        wpilib.SmartDashboard.putNumber("Intake Power", (self.intake_motor.get() * 100))
        wpilib.SmartDashboard.putNumber("Drive Speed", self.drive_motors_L.get() * 100) 
        wpilib.SmartDashboard.putNumber("Arm Power", self.arm_motors.get() * 100)
        wpilib.SmartDashboard.putBoolean("Note Shot", self.note_shot)
        wpilib.SmartDashboard.putBoolean("Intake mode", self.intake_active)

        # Get number and update values
        self.robot_speed = wpilib.SmartDashboard.getNumber("Maximum Drive Speed", self.drive_speed) / 100
        self.arm_speed = wpilib.SmartDashboard.getNumber("Maximum Arm Power", self.arm_speed) / 100


    def robotDisabled(self):
        pass

    def teleopInit(self):
        pass

    def teleopPeriodic(self):
        self.robot.tankDrive(-self.controller.getLeftY() * self.robot_speed, -self.controller.getRightY() * self.robot_speed)
        
        if self.controller.getPOV() == 0: 
            self.moveArm(-self.arm_speed)
        elif self.controller.getPOV() == 180:
            self.moveArm(self.arm_speed)
        
        self.activateIntake(self.controller.getL2Button())


        if self.controller.getR2Button():
            self.shootRing(self.strong_shot_speed, self.shot_delay)

        elif self.controller.getR1Button():
            self.shootRing(self.weak_shot_speed, self.shot_delay)
        
        else:
            self.shot_timer.stop()
            self.shot_timer.reset()
            self.shooting_motors.set(0)
            self.intake_motor.set(0)
        

    def teleopExit(self):
        pass

    def autonomousExit(self):
        pass

    def moveArm(self, direction):
        mean_encoder_position = (self.arm_encoders[0].getPosition() + self.arm_encoders[1].getPosition()) / 2
        
        if abs(mean_encoder_position) <= self.arm_encoder_limit:
            self.arm_motors.set(direction)

        
    def activateIntake(self, activate):
        def halt_timer():
            self.intake_reverse_timer.stop()
            self.intake_reverse_timer.reset()

        if activate:
            self.intake_active = True
            halt_timer()
            self.intake_motor.set(self.intake_speed)

        else:
            if self.intake_active:
                self.intake_active = False
                self.intake_reverse_timer.start()
                self.intake_motor.set(-self.intake_reverse_speed)
            
            if self.intake_reverse_timer.get() >= self.intake_reverse_duration:
                self.intake_motor.set(0)
                halt_timer()


    def shootRing(self, speed, fire_delay):
        self.shooting_motors.set(speed)

        if self.shot_timer.get() == 0:
            self.shot_timer.start()

        if self.shot_timer.get() == fire_delay:
            self.intake_motor.set(speed)
            self.shot_timer.stop()

    def calibrate_all_encoders(self):
        '''        
        self.left_encoders[0].setPosition(0)
        self.left_encoders[1].setPosition(0)
        self.right_encoders[0].setPosition(0)
        self.right_encoders[1].setPosition(0)
        self.arm_encoders[0].setPosition(0)
        self.arm_encoders[1].setPosition(0)
        self.climber_encoder.setPosition(0)
        '''
        all_encoders = self.left_encoders + self.right_encoders + self.arm_encoders + [self.climber_encoder]

        for encoder in all_encoders:
            encoder.setPosition(0)