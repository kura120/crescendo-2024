#SHOOTING MECHANISM - JASIERE B.

import robotpy, wpilib, wpilib.drive, rev
import math, time
import robotpy

class Shoot(wpilib.TimedRobot):
    brushless = rev.CANSparkMaxLowLevel.MotorType.kBrushless

#sets motor speed to max speed for shooting
    def robotShoot(self):
        self.motor = rev.CANSparkMax(max, self.brushless)
        self.motorEncoder = self.motor.getEncoder()