'''
Final code
FRC 3340 Coding

This contains all the code created in this folder complied as one to be sent to the robot.
This also has support for network tables allowing for values to be sent to the comptuer (and modified on the fly)
'''

import robotpy, wpilib, wpilib.drive, math, ntcore, rev, phoenix5


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        # Getting motors ready: each set of wheels has two motors powering it.
        # One side has to be inverted so that the robot moves forward instead of turning in place.
        self.brushless =  rev.CANSparkLowLevel.MotorType.kBrushless

        # SETUP: Controlling Default Percent Output (Speed) of motors. Some can be hotfixed using SmartDashboard, but change values here.
        self.drive_speed = 0.75                  #   Robot driving speed                                    (SmartDashboard)
        self.arm_speed = 0.2                    #   Robot arm speed                                         (SmartDashboard)
        self.intake_speed = 0.3                 #   Robot intake speed                                      (SmartDashboard)
        self.high_shot_speed_d = 0.5            #   Maximum shooter speed                                   (SmartDashboard)
        self.low_shot_speed_d = 0.2              #   Minimum shooter speed                                  (SmartDashboard)
        self.climber_speed = 0.3                #   Robot climber speed for switching climber position      (Hardcode)
        self.intake_reverse_speed = 0.1         #   Robot intake speed to secure note                       (Hardcode)
        self.intake_reverse_duration = 0.1      #   Robot intake duration to secure note                    (Hardcode)
        self.shot_delay = 3                     #   Delay between starting outtake and shot                 (Hardcode)
        self.low_arm_encoder_limit = 250            #                                                           (Hardcode)

        self.camera = wpilib.CameraServer.launch()      

        idle_mode = [rev.CANSparkMax.IdleMode.kCoast, rev.CANSparkMax.IdleMode.kBrake, phoenix5.NeutralMode.Coast, phoenix5.NeutralMode.Brake]

        '''
        Motor ID guide:
        1-4: Drive (odd for left, even for right)
        5-7: Arm/Climber
        8-10: Intake/Outtake

        Be sure to reflash any motor controllers using REV client (orange R) if necessary, or switch IDs.

        CIMs: 1x climber, 2x shooter, IDs 7, 9, 10
        Use Phoenix tuner X to change IDs
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
        self.drive_motors_R.setInverted(True)                   # Comment out if drive acts funny


        # SETUP - Arm Motors
        self.arm_motor_A = rev.CANSparkMax(5, self.brushless) 
        self.arm_motor_B = rev.CANSparkMax(6, self.brushless)
        self.arm_motor_A.setIdleMode(idle_mode[1])
        self.arm_motor_B.setIdleMode(idle_mode[1])
        self.arm_motor_A.setInverted(True)
        self.arm_motor_B.setInverted(False)
        self.arm_motors = wpilib.MotorControllerGroup(self.arm_motor_A, self.arm_motor_B)


        self.climber_motor = phoenix5.TalonSRX(7)
        self.climber_motor.setNeutralMode(idle_mode[3])
        

        # SETUP - Intake and Shooter Motors
        self.intake_motor = rev.CANSparkMax(8, self.brushless)
        self.intake_motor.setIdleMode(idle_mode[0])
        self.intake_motor.setInverted(True)

        self.shooting_motor_A = phoenix5.TalonSRX(9)
        self.shooting_motor_B = phoenix5.TalonSRX(10)

        self.shooting_motor_A.setNeutralMode(idle_mode[2])
        self.shooting_motor_B.setNeutralMode(idle_mode[2])

        self.shooting_motor_B.set(phoenix5.ControlMode.Follower, 9)

        self.shooting_motor_A.setInverted(True)
        self.shooting_motor_B.setInverted(True)

        # SETUP - Encoders
        self.left_encoders = [self.drive_motor_L1.getEncoder(), self.drive_motor_L2.getEncoder()]
        self.right_encoders = [self.drive_motor_R1.getEncoder(), self.drive_motor_R2.getEncoder()]
        self.arm_encoders = [self.arm_motor_A.getEncoder(), self.arm_motor_B.getEncoder()]

        # Setup: Robot Control
        self.controller = wpilib.PS4Controller(0)    # Connect to a joystick. Specify: PS4Controller, PS5Controller
        self.robot = wpilib.drive.DifferentialDrive(self.drive_motors_L, self.drive_motors_R)       # Setup Robot Drive System
        
        # Timers
        self.intake_reverse_timer = wpilib.Timer()
        self.shot_timer = wpilib.Timer() 

        # Calculation parameters
        self.wheel_distance_per_rotation = (42 * 14) / (6 * math.pi) # Breakdown: (42 encoder counts / gearbox ratio) * wheel circumference, inches

        # Boolean values
        self.note_shot = False
        self.intake_active = False            

        # Parameters that can be modified on SmartDashboard
        wpilib.SmartDashboard.putNumber("Maximum Drive Speed", (self.drive_speed * 100))
        wpilib.SmartDashboard.putNumber("Maximum Arm Power", (self.arm_speed * 100))
        wpilib.SmartDashboard.putNumber("Low Shot Max Power", self.low_shot_speed_d)
        wpilib.SmartDashboard.putNumber("High Shot Max Power", self.high_shot_speed_d)

        # Limit Switch for Arm
        self.limit_switch_high_arm = wpilib.DigitalInput(9)



    def robotPeriodic(self):
        # Update Average Encoder Information
        self.mean_encoder_position = (self.arm_encoders[0].getPosition() + self.arm_encoders[1].getPosition()) / 2
        self.mean_drive_encoder_distance = (self.left_encoders[1].getPosition() + self.left_encoders[0].getPosition() 
                                       + self.right_encoders[0].getPosition() + self.right_encoders[1].getPosition() / 4)

        # SmartDashboard Stats
        wpilib.SmartDashboard.putNumber("Arm Encoder Average", self.mean_encoder_position)
        wpilib.SmartDashboard.putNumber("Shot Timer", (self.shot_delay - (self.shot_timer.get()) / self.shot_delay) * 100) 
        wpilib.SmartDashboard.putNumber("Outtake Power", (self.shooting_motor_A.getStatorCurrent() * 100))
        wpilib.SmartDashboard.putNumber("Intake Power", (self.intake_motor.get() * 100))
        wpilib.SmartDashboard.putNumber("Left Speed", self.drive_motors_L.get() * 100) 
        wpilib.SmartDashboard.putNumber("Right Speed", self.drive_motors_R.get() * 100) 
        wpilib.SmartDashboard.putNumber("Arm Power", self.arm_motors.get() * 100)   
        wpilib.SmartDashboard.putBoolean("Intake mode", self.intake_active)

        # Get number and update values
        self.robot_speed = wpilib.SmartDashboard.getNumber("Maximum Drive Speed", self.drive_speed)
        self.arm_speed = wpilib.SmartDashboard.getNumber("Maximum Arm Power", self.arm_speed)
        self.low_shot_speed = wpilib.SmartDashboard.getNumber("Low Shot Power", self.low_shot_speed_d) 
        self.high_shot_speed = wpilib.SmartDashboard.getNumber("High Shot Power", self.high_shot_speed_d)


    def autonomousInit(self):
        self.auto_program = "simple move"           # Copy and paste case statements
        self.autonomous_stage = 1
        self.end_autonomous = False
        self.arm_encoders[0].setPosition(0)
        self.arm_encoders[1].setPosition(0)


    def autonomousPeriodic(self):
        def move_robot(distance):
            if self.mean_drive_encoder_distance * self.wheel_distance_per_rotation < distance:    # inchess
                self.drive_motors_L.set(0.5)
                self.drive_motors_R.set(0.5)
            else:
                self.drive_motors_L.set(0.)
                self.drive_motors_R.set(0.)
                self.autonomous_stage += 1

        '''
        Alliance area is 26 feet 11.128 inches wide, 9 ft 10.25 ft deep
        '''
        match self.auto_program:
            case "simple move":                 # case 1
                match self.autonomous_stage:
                    case 1:
                        move_robot(20)

            case "shoot notes to speaker, assuming robot preloaded":            # case 2
                match self.autonomous_stage:
                    case 1:
                        self.autonomous_stage += 1

                    case 2:
                        self.shootRing(self.high_shot_speed_d, 2)

                        if self.note_shot:
                            self.note_shot = False
                            self.shot_timer.reset()
                            self.shooting_motor_A.set(phoenix5.ControlMode.PercentOutput, 0)
                            self.intake_motor.set(0)
                            
                            if self.end_autonomous:
                                self.autonomous_stage = 0
                            else:
                                self.autonomous_stage += 1
                    
                    case 3:
                        pass
                        
            case "amp":
                match self.autonomous_stage:
                    case 1:
                        pass


    def teleopPeriodic(self):
        self.robot.tankDrive(-self.controller.getLeftY() * self.robot_speed, self.controller.getRightY() * self.robot_speed)
        
        if self.controller.getPOV() == 0: 
            self.moveArm(-self.arm_speed)
        elif self.controller.getPOV() == 180:
            self.moveArm(self.arm_speed)
        else:
            self.moveArm(0)
        
        self.activateIntake(self.controller.getL2Button())

        self.turnClimber((-self.controller.getCircleButton() + 0 + self.controller.getCrossButton()) * self.climber_speed)

        if not(self.intake_active):
           # if self.controller.getR2Button():
            if self.controller.getR1ButtonPressed():
                self.shootRing(self.high_shot_speed, self.shot_delay)
                
            elif self.controller.getR2ButtonPressed():
                self.shootRing(self.low_shot_speed, self.shot_delay)
            
            else:
                self.intake_motor.set(0)   
                self.shooting_motor_A.set(phoenix5.ControlMode.PercentOutput, 0)
                self.note_shot = False
                self.shot_timer.stop()
                self.shot_timer.reset()
                print("Shooter Disabled")

        
        else:
             pass
            
        
    # RUN TEST TO CALIBRATE EVERYTHING!!!!!! INCLUDING THE ARM AND CLIMBER!!
    def testPeriodic(self):
        self.turnClimber(-self.climber_speed)
        self.moveArm(self.arm_speed)


    def testExit(self):
        self.arm_encoders[0].setPosition(0)
        self.arm_encoders[1].setPosition(0)

    
    def moveArm(self, direction):  
        if abs(self.mean_encoder_position) <= self.low_arm_encoder_limit:
            # Check if the limit switch located at highest point of arm is not activated.
            if direction < 0 and self.limit_switch_high_arm.get():
                self.arm_motors.set(0)
            else:
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
        self.shooting_motor_A.set(phoenix5.ControlMode.PercentOutput, speed)

        if self.shot_timer.get() == 0:
            self.shot_timer.start()
        
        if self.shot_timer.get() == fire_delay:
            self.note_shot = True
            self.intake_motor.set(speed)
            self.shot_timer.stop()
    
    
    def turnClimber(self, speed):
        self.climber_motor.set(phoenix5.ControlMode.PercentOutput, speed)