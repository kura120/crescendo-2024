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
        #intake = 2 ways
        #output = 1 way (forward-sync 2 motors)
        self.brushless =  rev.CANSparkLowLevel.MotorType.kBrushless

        # SETUP - NEED TO ASSIGN CORRECT IDEA TO MOTOR CONTROLLER!!!
        self.climber = rev.CANSparkMax(5, self.brushless) 
    
     
      #  self.outmotors = wpilib.MotorControllerGroup(self.outmotor_R, self.outmotor_L)
        # SETUP - Motor details

        self.climberEncoder = self.climber.getEncoder()

        self.climberEncoder.setPosition(0)

#cc - up 
#ccw - down

        #Idle mode: brake
        idle_mode = rev.CANSparkMax.IdleMode.kBrake
        self.climber.setIdleMode(idle_mode)
       
        #check player number/ change button no.
        self.controller = wpilib.XboxControllerController(0)      
    """  self.speed = 0.5 #CONTROL SPEED HERE
        self.drive = wpilib.drive.DifferentialDrive(
            self.climber
           )"""
        

    def robotPeriodic(self):
        wpilib.SmartDashboard.putNumber("Left Encoder", self.outputEncoder.getPosition())
        wpilib.SmartDashboard.putNumber("Right Encoder", self.rightEncoder.getPosition())

    def teleopPeriodic(self):
        if self.controller.Button.int(0):
           self.speed = self.speed.set(0.5)

        else:
            self.speed = self.speed.set(-0.5)
        
        #CHANGE NUMBER BUTTON
          

if __name__ == "__main__":
    wpilib.run(MyRobot)