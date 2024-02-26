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
        self.outmotor_L = rev.CANSparkMax(5, self.brushless) 
    
        # SETUP - Right Motor
        self.outmotor_R = rev.CANSparkMax(6, self.brushless) 
        self.outmotor_R.setInverted(True)
      #  self.outmotors = wpilib.MotorControllerGroup(self.outmotor_R, self.outmotor_L)
        # SETUP - Motor details

        self.outleftEncoder = self.outmotor_L.getEncoder()
        self.outrightEncoder = self.outmotor_R.getEncoder()

        self.outleftEncoder.setPosition(0)
        self.outrightEncoder.setPosition(0)


        #Idle mode: brake
        idle_mode = rev.CANSparkMax.IdleMode.kBrake
        self.outmotor_L.setIdleMode(idle_mode)
        self.outmotor_R.setIdleMode(idle_mode)
       
        #check player number
        self.controller = wpilib.PS4Controller(0)      
        self.speed = 0.5 #CONTROL SPEED HERE
        self.drive = wpilib.drive.DifferentialDrive(
            self.outmotor_L, self.outmotor_R
           )
        

    def robotPeriodic(self):
        wpilib.SmartDashboard.putNumber("Left Encoder", self.outputEncoder.getPosition())
        wpilib.SmartDashboard.putNumber("Right Encoder", self.rightEncoder.getPosition())

    def teleopPeriodic(self):
        self.drive.tankDrive(
           self.controller.getLeftY()*self.speed,
           self.controller.getRightY()*self.speed
            
        )
        


if __name__ == "__main__":
    wpilib.run(MyRobot)