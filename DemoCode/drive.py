'''
FINAL CODE 2/8/24
FRC 3340 Coding Team
'''


import robotpy, wpilib, wpilib.drive, rev, phoenix5
import math, time

class MyRobot(wpilib.TimedRobot):
    
    def robotInit(self):
        # Getting motors ready: each set of wheels has two motors powering it.
        # One side has to be inverted so that the robot moves forward instead of turning in place.
        self.brushless =  rev.CANSparkLowLevel.MotorType.kBrushless

        # SETUP - Left Motors
        self.motor_L1 = rev.CANSparkMax(1, self.brushless) 
        self.motor_L2 = rev.CANSparkMax(2, self.brushless)

        self.motors_L = wpilib.MotorControllerGroup(self.motor_L1, self.motor_L2)

        # SETUP - Right Motors
        self.motor_R1 = rev.CANSparkMax(3, self.brushless) 
        self.motor_R2 = rev.CANSparkMax(4, self.brushless)
        self.motors_R = wpilib.MotorControllerGroup(self.motor_R1, self.motor_R2)

        self.motors_R.setInverted(True)

        # SETUP - Motor details

        self.leftEncoder = self.motor_L1.getEncoder()
        self.rightEncoder = self.motor_R1.getEncoder()

        self.leftEncoder.setPosition(0)
        self.rightEncoder.setPosition(0)


        #Idle mode: brake
        idle_mode = rev.CANSparkMax.IdleMode.kBrake
        self.motor_L1.setIdleMode(idle_mode)
        self.motor_R1.setIdleMode(idle_mode)
       
        #check player number
        self.controller = wpilib.PS4Controller(0)      
        self.speed = 0.5 #speed control
        self.drive = wpilib.drive.DifferentialDrive(
           self.motors_L, self.motors_R
           )

    def robotPeriodic(self):
        wpilib.SmartDashboard.putNumber("Left Encoder", self.leftEncoder.getPosition())
        wpilib.SmartDashboard.putNumber("Right Encoder", self.rightEncoder.getPosition())
        

    def teleopPeriodic(self):
        self.drive.tankDrive(
            self.controller.getLeftY()*self.speed,
            self.controller.getRightY()*self.speed
        )


    


if __name__ == "__main__":
    wpilib.run(MyRobot)