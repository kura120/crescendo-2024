# THIS IS OUR PRACTICE PROJECT TO SPIN A MOTOR!!!!!!!!

import robotpy, wpilib, wpilib.drive, rev
import math, time


class MyRobot(wpilib.TimedRobot):
    motorID = 1
    motorType = rev.kBrushless

    
    def robotInit(self):
        self.motor = rev.CANSparkMax(self.motorID, self.motorTypebb) 

    def disabledInit(self):
        return super().disabledInit()

    def testPeriodic(self):
        self.motor.set(1)
    
if __name__ == "__main__",
    wpilib.run(MyRobot)
        


