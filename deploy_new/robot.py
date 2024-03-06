'''
FRC Team 3340
Robot code for Crescendo 2024
Modular

Components folder contains modules that are imported.
'''
import wpilib
from components.test_cim_drive import Drive
from components.shooter import Shooter
from components.climber import Climber
from components.dashboard import Dashboard


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.drive = Drive()
        # self.shooter = Shooter()
        # self.climber = Climber()
        self.dashboard = Dashboard()

        self.controller = wpilib.Joystick(0)

        dashboard_mutables = {
            "Max Drive Power": self.drive.speed
        }
    
        self.dashboard.update_dashboard(dashboard_mutables)

    def robotPeriodic(self):
        self.inputs = {
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

        self.stats_for_dashboard = {
            "Left Drive Power": self.drive.left_drive_train.get(),
            "Right Drive Power": self.drive.right_drive_train.get(),
            # "Climber State": self.climber.climber_state,
        }

        self.dashboard.update_dashboard(self.stats_for_dashboard)
        self.drive.speed = self.dashboard.fetch_dashboard_value("Max Drive Power", self.drive.speed, 0.5)


    def teleopPeriodic(self):
        self.drive.tank_drive(self.inputs["TD Left"], self.inputs["TD Right"])
        # self.drive.arcade_drive(self.inputs["AD Forward Axis"], self.inputs["AD Rotate Axis"])


    def testPeriodic(self):
        pass