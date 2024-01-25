#SHOOTING MECHANISM - JASIERE B.

import robotpy, wpilib, wpilib.drive, rev
import math, time
import robotpy

class Shoot(wpilib.TimedRobot):
    brushless = rev.CANSparkMaxLowLevel.MotorType.kBrushless
    
    def robotInit(self):
        #two motors:
        self.motor = rev.CANSparkMax(3, self.brushless) 

        #encoder:
        self.motorEncoder = self.motor.getEncoder()

        self.motor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.motorEncoder.setPosition(0)
        self.joystick = wpilib.Joystick(0)      


    
    def testPeriodic(self):
        self.motor = rev.CANSparkMax(max, self.brushless)
        self.motorEncoder = self.motor.getEncoder()
        
        if abs(self.joystick.getRawButtonPressed(2)): 
            self.motor.set(max)
        #Max speed when pressed
        

        else:
            self.motor.setIdleMode
        #Idle mode upon button released
            




        

     
