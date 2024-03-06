# Shooter inherits intake

import wpilib
from components.test_cim_drive import CIMDrive
from components.shooter import Shooter
from components.climber import Climber
from components.dashboard import Dashboard


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.drive = CIMDrive()
        self.shooter = Shooter()
        self.climber = Climber()
        self.dashboard = Dashboard()

        self.controller = wpilib.Joystick(0)

        self.button_mappings = {
            "AD Forward Axis": self.controller.getRawAxis(0),
            "AD Rotate Axis": self.controller.getRawAxis(1),
            "TD Left": self.controller.getRawAxis(0),
            "TD Right": self.controller.getRawAxis(5),
            "Shooter Low": self.controller.getRawButton(4),
            "Shooter High": self.controller.getRawButton(5),
<<<<<<< HEAD
            "Intake": self.controller.getRawButton(6),
            "Climber Up": self.controller.getRawButton(7),
            "Climber Down": self.controller.getRawButton(8)
        }

        self.dashboard_log = {
            "Left Drive Power": self.drive.left_drive_train.get(),
            "Right Drive Power": self.drive.right_drive_train.get(),
            "Climber State": self.climber.climber_state,
=======
            "Intake": self.controller.getRawButton(6)
>>>>>>> 4e605e15bcb871dd65a1387c79fb9a582de76829
        }

    def teleopPeriodic(self):
        self.drive.arcade_drive(self.button_mappings["AD Forward Axis"], self.button_mappings["AD Rotate Axis"])
<<<<<<< HEAD
        self.dashboard.update_dashboard(self.dashboard_log)
=======
        self.shooter.intake.activate_intake(self.controller.getbu)
>>>>>>> 4e605e15bcb871dd65a1387c79fb9a582de76829


    def testPeriodic(self):
        self.drive.tank_drive(self.button_mappings["TD Left"], self.button_mappings["TD Right"])
        
