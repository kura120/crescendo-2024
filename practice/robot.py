# THIS IS OUR PRACTICE PROJECT TO SPIN A MOTOR!!!!!!!!

import robotpy, wpilib, wpilib.drive, rev
import math, time


class MyRobot(wpilib.TimedRobot):
    brushless = rev.CANSparkMaxLowLevel.MotorType.kBrushless
    
    def robotInit(self):
        #MOTOR CONTROLS _ LEFT
        self.motor_L1 = rev.CANSparkMax(1, self.brushless) 
        # self.motor_L2 = rev.CANSparkMax(1, self.brushless)

            
        # self.motors_L = wpilib.MotorControllerGroup(self.motor_L1, self.motor_L2)

            #MOTOR CONTROL _ RIGHT

            #self.motor_R1 = rev.CANSparkMax(3, self.brushless) 
            #self.motor_R2 = rev.CANSparkMax(4, self.brushless)

            
        # self.motors_R = wpilib.MotorControllerGroup(self.motor_R1, self.motor_R2)





        self.motorEncoder = self.motor.getEncoder()
        self.motor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.motorEncoder.setPosition(0)
        self.joystick = wpilib.Joystick(0)      


    def robotPeriodic(self):
        wpilib.SmartDashboard.putNumber("Encoder", self.motorEncoder.getPosition())


    def disabledInit(self):
        self.motor.set(0)
        

    def testPeriodic(self):
        if abs(self.joystick.getY()) > 0.1: #Analog input with floats
            self.motor.set(self.joystick.getY())
        else:
             self.motor.set(0)
        if self.joystick.getRawButton(1):
            self.motor.set(0.1)
        else:
            self.motor.set(0)


if __name__ == "__main__":
    wpilib.run(MyRobot)