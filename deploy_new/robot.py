# Shooter inherits intake

import wpilib
from components.test_cim_drive import CIMDrive
from components.shooter import Shooter
from components.climber import Climber
from components.dashboard import Dashboard


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.drive = CIMDrive()
        # self.shooter = Shooter()
        # self.climber = Climber()
        # self.dashboard = Dashboard()

        self.controller = wpilib.Joystick(0)


        self.dashboard_log = {
            "Left Drive Power": self.drive.left_drive_train.get(),
            "Right Drive Power": self.drive.right_drive_train.get(),
            # "Climber State": self.climber.climber_state,
        }

    def robotPeriodic(self):

        self.button_mappings = {
            "AD Forward Axis": -self.controller.getRawAxis(1),
            "AD Rotate Axis": self.controller.getRawAxis(2),
            "TD Left": self.controller.getRawAxis(5),
            "TD Right": self.controller.getRawAxis(1),
            "Shooter Low": self.controller.getRawButton(4),
            "Shooter High": self.controller.getRawButton(5),
            "Intake": self.controller.getRawButton(6),
            "Climber Up": self.controller.getRawButton(7),
            "Climber Down": self.controller.getRawButton(8)
        }

        self.dashboard_log = {
            "Left Drive Power": self.drive.left_drive_train.get(),
            "Right Drive Power": self.drive.right_drive_train.get(),
            # "Climber State": self.climber.climber_state,
        }

    def teleopPeriodic(self):
        self.drive.arcade_drive(self.button_mappings["AD Forward Axis"], self.button_mappings["AD Rotate Axis"])
        # self.dashboard.update_dashboard(self.dashboard_log)


    def testPeriodic(self):
        self.drive.tank_drive(self.button_mappings["TD Left"], self.button_mappings["TD Right"])
        
