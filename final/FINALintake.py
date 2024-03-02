'''
Intake Code
FRC 3340 Coding Team

What it's supposed to do:
When driver holds the intake button down on their controller, the intake motors should spin.
Upon releasing the button, the intake motors do a partial rotation to keep the note in the shooter.

Code before 2/27 WORKS
Changes untested
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
        self.intake_motor = rev.CANSparkMax(7, self.brushless)

        #Idle mode: This is a windup mechanism.
        idle_mode = rev.CANSparkMax.IdleMode.kCoast
        self.intake_motor.setIdleMode(idle_mode)
        self.intake_motor.setInverted(True)

        #check player number
        self.controller = wpilib.PS4Controller(0)      
        self.speed = 0.5 #CONTROL SPEED HERE


        # Intake-specific:
        self.intake_speed = 0.1
        self.intake_active = False            
        self.reverse_intake_timer = wpilib.Timer()
        self.reverse_intake_min = 0.2

    def robotPeriodic(self):
        pass

    def teleopPeriodic(self):
        '''
        If the left trigger is pressed, the intake motors spin to take in a note.
        After the trigger is released, the code should reverse the motors for half a second at LOW POWER to make sure the note does not touch the shooting motors.
        
        '''
        self.activateIntake(self.controller.getL2Button())

    def activateIntake(self, activate ):
        if activate:
            self.intake_active = True
            self.reverse_intake_timer.reset()
            self.intake_motor.set(self.intake_speed)

        else:
            if self.intake_active:
                self.intake_active = False
                self.reverse_intake_timer.start()
                self.intake_motor.set(-0.1)
            
            if self.reverse_intake_timer.get() >= self.reverse_intake_min:
                self.intake_motor.set(0)
                self.reverse_intake_timer.stop()
                self.reverse_intake_timer.reset()