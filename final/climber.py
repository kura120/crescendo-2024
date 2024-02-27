'''
Climber
FRC 3340 Coding Team
'''


import robotpy, wpilib, wpilib.drive, rev, phoenix5
import math, time

class MyRobot(wpilib.TimedRobot):
    
    def robotInit(self):
        # SETUP - Defining motor type.
        self.brushless =  rev.CANSparkLowLevel.MotorType.kBrushless

        # SETUP - Creating motor controller object to interact with climber.
        climber_id = 1  # CHANGE TO MATCH ACTUAL ID OF CLIMBER MOTOR!!!
        self.climber_motor = rev.CANSparkMax(climber_id, self.brushless) 
    
        # SETUP - Getting the encoder so that we can measure rotations of the climber.

        self.climber_encoder = self.climber_motor.getEncoder()
        self.climber_encoder.setPosition(0)                         # Calibrate climber encoder

        #Idle mode: brake
        idle_mode = rev.CANSparkMax.IdleMode.kBrake
        self.climber_motor.setIdleMode(idle_mode)
       
        # Get controller
        self.controller = wpilib.PS4Controller(0)      

        # Climber-specific controls:
        self.climber_speed = 0.2            # Percent output to climber motor to determine how fast the climber moves from unhooked to hooked position.
        self.is_climber_down = False        # By default, climber is off.
        self.climber_encoder_limit = 100    # Maximum encoder position for climber down position.

    def robotPeriodic(self):
        pass
    def teleopPeriodic(self):
        if self.controller.getCircleButton(0):                         # TODO: Change button later.
            # Reverse the climber bool. False => True, True => False.
            self.is_climber_down = not(self.is_climber_down)
        
        # TODO: Condense this code if possible. See if you can use limit switches to avoid relying on the encoders entirely.
        if self.is_climber_down:
            if self.climber_encoder.getPosition() < self.climber_encoder_limit:
                self.climber_motor.set(self.climber_speed)
            else:
                self.climber_motor.set(0)
        else:
            if self.climber_encoder.getPosition() > -self.climber_encoder_limit:
                self.climber_motor.set(-self.climber_speed)
            else:
                self.climber_motor.set(0)                    
          

if __name__ == "__main__":

    wpilib.run(MyRobot)