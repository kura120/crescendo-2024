import robotpy, wpilib, wpilib.drive, rev
import math, time


class MyRobot(wpilib.TimedRobot):
    brushless = rev.CANSparkMaxLowLevel.MotorType.kBrushless
    
    def robotInit(self):
        #two motors:
        self.motor1 = rev.CANSparkMax(1, self.brushless) 
        self.motor2 = rev.CANSparkMax(2, self.brushless) 

        #encoder:
        self.motorEncoder = self.motor.getEncoder()

        self.motor.setIdleMode(rev.CANSparkMax.IdleMode.kBrake)
        self.motorEncoder.setPosition(0)
        self.joystick = wpilib.Joystick(0)      


    def robotPeriodic(self):
        wpilib.SmartDashboard.putNumber("Encoder", self.motorEncoder.getPosition())


    def disabledInit(self):
        self.motor1.set(0)
        

    def testPeriodic(self):
        if abs(self.joystick.getY()) >= 0.1: #Analog float input 
            self.motor1.set(self.joystick.getY())
            self.motor2.set(self.joystick.getY())
            #one motor has to work in opposite direction, right?

        else:
           self.motor1.set(0)
           self.motor2.set(0)

    #Button 1 -- forward
        if self.joystick.getRawButton(1):
            self.motor1.set(0.1)
            self.motor2.set(-0.1)
        else:
            self.motor1.set(0)
            self.motor2.set(0)

    #Button 2 -- backward
        if self.joystick.getRawButton(2):
            self.motor1.set(-0.1)
            self.motor2.set(0.1)
            #need to test the values above to get motors to move the robot the correct way
        else:
            self.motor1.set(0)
            self.motor2.set(0)

    #Button 3 -- left
        if self.joystick.getRawButton(3):
            self.motor1.set(0.1)
            self.motor2.set(-0.1)
        else:
            self.motor1.set(0)
            self.motor2.set(0)

      #So on...
      #assign the number for each specific button on the controller ABOVE ^


    # kMotorPort = 0
    # kJoystickPort = 0
    # kEncoderPortA = 0
    # kEncoderPortB = 1

    # def robotInit(self):
    #     """Robot initialization function"""

    #     self.motor = wpilib.PWMSparkMax(self.kMotorPort)
    #     self.joystick = wpilib.Joystick(self.kJoystickPort)
    #     self.encoder = wpilib.Encoder(self.kEncoderPortA, self.kEncoderPortB)
    #     # Use SetDistancePerPulse to set the multiplier for GetDistance
    #     #LM: Following measurements will vary:
    #     # This is set up assuming a 6 inch wheel with a 360 CPR encoder.
    #     self.encoder.setDistancePerPulse((math.pi * 6) / 360.0)

    # def robotPeriodic(self):
    #     """The RobotPeriodic function is called every control packet no matter the robot mode."""
    #     wpilib.SmartDashboard.putNumber("Encoder", self.encoder.getDistance())

    # def teleopPeriodic(self):
    #     self.motor.set(self.joystick.getY())


if __name__ == "__main__":
    wpilib.run(MyRobot)
