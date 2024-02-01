'''
Programming a CIM motor
CIM motors are the larger black motors connected to a Talon SRX from CTRE.
These motors are brushed and will be used in the event REV NEOs are scarce.

Things to know:
Please be using the latest version of RobotPy. If you are not, run either of these commands
    macOS: python3 -m pip install --upgrade robotpy
           python3.XX -m pip install --upgrade robotpy              # Replace XX with your version of Python (rec. 3.11)
           python -m pip install --upgrade robotpy 

    Windows: py -3 -m pip install --upgrade robotpy                 # If needed, specify version of Python, for python.org installs.
             python -m pip install --upgrade robotpy                # Run if you installed Python from the Windows Store.

Make sure the following package is installed or up-to-date: robotpy-ctre

When testing, rename this file to robot.py and make sure a joystick is connected to port 0.

'''

import robotpy, wpilib, wpilib.drive, phoenix5 


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.CIM = phoenix5.TalonSRX(0)         # Replace ID with another number if 1 does not work.
        self.joystick = wpilib.Joystick(1)

    def testPeriodic(self):
        if self.joystick.axisGreaterThan(0, 0.1):
            self.CIM.set(ControlMode.Position, rghtJoy)

            #self.CIM.set(self.joystick.getY())