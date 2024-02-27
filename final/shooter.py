'''
Shooting
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

        self.intake_motor = rev.CANSparkMax(7, self.brushless)
        self.shooting_motor_A = rev.CANSparkMax(6, self.brushless)
        self.shooting_motor_B = rev.CANSparkMax(5, self.brushless)
        self.shooting_motors = wpilib.MotorControllerGroup(self.shooting_motor_A, self.shooting_motor_B)
        self.shooting_motors.setInverted(True)

        #Idle mode: This is a windup mechanism.
        idle_mode = rev.CANSparkMax.IdleMode.kCoast
        self.shooting_motor_A.setIdleMode(idle_mode)
        self.shooting_motor_B.setIdleMode(idle_mode)
        self.intake_motor.setIdleMode(idle_mode)
        
        self.intake_motor.setInverted(True)


        #check player number
        self.controller = wpilib.PS4Controller(0)      
        self.speed = 0.5 #CONTROL SPEED HERE

        # Intake-specific:
        self.high_shooting_speed = 0.9
        self.low_shooting_speed = 0.4
        self.shoot_delay = 5

        self.shooting_cooldown = wpilib.Timer()
        self.is_shooting = False

    def robotPeriodic(self):
        pass

    def teleopPeriodic(self):
        '''
        If the left trigger is pressed, the intake motors spin to take in a note.
        After the trigger is released, the code should reverse the motors for half a second at LOW POWER to make sure the note does not touch the shooting motors.
        
        '''
        if self.controller.getR2Button():
            self.shootRing(self.high_shooting_speed, self.shoot_delay)

        elif self.controller.getR1Button():
            self.shootRing(self.low_shooting_speed, self.shoot_delay)
        
        else:
            self.shooting_cooldown.stop()
            self.shooting_cooldown.reset()
            self.shooting_motors.set(0)
            self.intake_motor.set(0)

    def shootRing(self, speed, fire_delay):
        self.shooting_motors.set(speed)

        if self.shooting_cooldown.get() == 0:
            self.shooting_cooldown.start()

        if self.shooting_cooldown.get() >= fire_delay:
            self.intake_motor.set(speed)

    def resetShooter(self):
        self.shooting_cooldown.stop()
        self.shooting_cooldown.reset()
        self.shooting_motors.set(0)
        self.intake_motor.set(0)
        