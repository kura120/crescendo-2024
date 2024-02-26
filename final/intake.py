'''
Intake Code
FRC 3340 Coding Team

What it's supposed to do:
When driver holds the intake button down on their controller, the intake motors should spin.
Upon releasing the button, the intake motors do a partial rotation to keep the note in the shooter.
'''


import robotpy, wpilib, wpilib.drive, rev

class MyRobot(wpilib.TimedRobot):
    
    def robotInit(self):
        # Getting motors ready: each set of wheels has two motors powering it.
        # One side has to be inverted so that the robot moves forward instead of turning in place.
        #intake = 2 ways
        #output = 1 way (forward-sync 2 motors)
        self.brushless =  rev.CANSparkLowLevel.MotorType.kBrushless

        # SETUP - NEED TO ASSIGN CORRECT ID TO MOTOR CONTROLLER!!!
        self.intake_motor = rev.CANSparkMax(6, self.brushless)

        #Idle mode: This is a windup mechanism.
        idle_mode = rev.CANSparkMax.IdleMode.kCoast
        self.intake_motor.setIdleMode(idle_mode)

        #check player number
        self.controller = wpilib.PS4Controller(0)      
        self.speed = 0.5 #CONTROL SPEED HERE
        self.drive = wpilib.drive.DifferentialDrive(
            self.outmotor_L, self.outmotor_R
           )

        # Intake-specific:
        self.intake_speed = 0.25
        self.intake_active = False            
        self.reverse_intake_timer = wpilib.Timer()

    def robotPeriodic(self):
        wpilib.SmartDashboard.putNumber("Left Encoder", self.outputEncoder.getPosition())
        wpilib.SmartDashboard.putNumber("Right Encoder", self.rightEncoder.getPosition())


    def teleopPeriodic(self):
        '''
        If the left trigger is pressed, the intake motors spin to take in a note.
        After the trigger is released, the code should reverse the motors for half a second at LOW POWER to make sure the note does not touch the shooting motors.
        
        '''
        if self.controller.getL2Button():
            self.intake_active = True
            self.reverse_intake_timer.reset()
            self.intake_motor.set(self.intake_speed)

        else:
            if self.intake_active:
                self.intake_active = False
                self.reverse_intake_timer.start()
                self.intake_motor.set(-0.1)
            
            if self.reverse_intake_timer >= 0.5:
                self.intake_motor(0)
                self.reverse_intake_timer.stop()
                self.reverse_intake_timer.reset()