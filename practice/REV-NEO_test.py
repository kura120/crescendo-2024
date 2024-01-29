'''
Programming a NEO motor with Encoder support
NEO motors are the small black motors connected to the REV Spark Max. These motors are brushless.
You can easily identify the NEO because its name is in big bold text on the motor itself.

Things to know:
Please be using the latest version of RobotPy. If you are not, run either of these commands
    macOS: python3 -m pip install --upgrade robotpy
           python3.XX -m pip install --upgrade robotpy              # Replace XX with your version of Python (rec. 3.11)
           python -m pip install --upgrade robotpy 

    Windows: py -3 -m pip install --upgrade robotpy                 # If needed, specify version of Python, for python.org installs.
             python -m pip install --upgrade robotpy                # Run if you installed Python from the Windows Store.

Make sure the following package is installed or up-to-date: robotpy-rev

When testing, rename this file to robot.py and make sure a joystick is connected to port 0.
'''

import robotpy, wpilib, wpilib.drive, rev 

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        # I understand that identifier for the motor type is long. I highly recommend assigning it to a variable "brushless"
        self.NEO = rev.CANSparkMax(1, rev.CANSparkLowLevel.MotorType.kBrushless)
        self.joystick = wpilib.Joystick(0)
        self.NEO_Encoder = self.NEO.getEncoder()

    def testPeriodic(self):
        if self.joystick.axisGreaterThan(0, 0.1):
            if self.NEO_Encoder.getPosition() < 100 and self.NEO_Encoder.getPosition() >= 0:
                # The motor will stop if you move it too much.
                self.NEO.set(self.joystick.getY())
