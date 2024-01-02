# THIS IS OUR PRACTICE PROJECT TO SPIN A MOTOR!!!!!!!!

import robotpy, wpilib, wpilib.drive, rev
import math, time


class MyRobot(wpilib.TimedRobot):
    motorID = 0
    motorType = rev.kBrushless

    
    def robotInit(self):
        motor = rev.CANSparkMax(self.motorID, self.motorType) 

    def disabledInit(self):
        return super().disabledInit()

    def testPeriodic(self):
        pass


