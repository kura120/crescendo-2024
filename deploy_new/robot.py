# Shooter inherits intake

import wpilib
from components.test_cim_drive import CIMDrive
from components.shooter import Shooter
from components.climber import Climber


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.drive = CIMDrive()
        self.shooter = Shooter()
        self.climber = Climber()

        self.controller = wpilib.Joystick(0)

        self.button_mappings = {
            "AD Forward Axis": self.controller.getRawAxis(0),
            "AD Rotate Axis": self.controller.getRawAxis(1),
            "TD Left": self.controller.getRawAxis(0),
            "TD Right": self.controller.getRawAxis(5),
            "Shooter Low": self.controller.getRawButton(4),
            "Shooter High": self.controller.getRawButton(5),

        }

    def teleopPeriodic(self):
        self.drive.arcade_drive(self.button_mappings["AD Forward Axis"], self.button_mappings["AD Rotate Axis"])


    def testPeriodic(self):
        self.drive.tank_drive(self.button_mappings["TD Left"], self.button_mappings["TD Right"])
        
