'''
FRC Team 3340
Robot code for Crescendo 2024
Modular

Components folder contains modules that are imported.
'''
import wpilib
from components.drive import Drive
from components.shooter import Shooter
from components.climber import Climber
from components.dashboard import Dashboard


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.drive = Drive()
        self.shooter = Shooter()
        self.climber = Climber()
        self.dashboard = Dashboard()

        self.controller = wpilib.Joystick(0)

        dashboard_mutables = {
            "Max Drive Power": self.drive.speed
        }
    
        self.dashboard.update_dashboard(dashboard_mutables)

    def robotPeriodic(self):
        '''
        Current mappings:
        
        D-Pad UP/DOWN - Climber
        Left Stick Up/Down - Arcade Drive Forward
        Right Stick Left/Right - Arcade Drive Rotate
        L2 - Intake
        R2 - Speaker Shot
        R1 - Amp Shot (try to refrain from using)
        
        
        '''

        self.inputs = {         
            "AD Forward Axis": -self.controller.getRawAxis(1),
            "AD Rotate Axis": -self.controller.getRawAxis(2),
            "Shooter Low": self.controller.getRawButton(6),
            "Shooter High": self.controller.getRawButton(8),
            "Intake": self.controller.getRawButton(7),
            "Climber Up": self.controller.getPOV() == 0,
            "Climber Down": self.controller.getPOV() == 180,
        }

        self.stats_for_dashboard = {
            "Left Drive Power": self.drive.left_drive_train.get(),
            "Right Drive Power": self.drive.right_drive_train.get(),
            # "Climber State": self.climber.climber_state,
        }

        self.dashboard.update_dashboard(self.stats_for_dashboard)
        self.drive.speed = self.dashboard.fetch_dashboard_value("Max Drive Power", self.drive.speed, 0.5)


    def teleopPeriodic(self):
        self.drive.arcade_drive(self.inputs["AD Forward Axis"], self.inputs["AD Rotate Axis"])

        self.shooter.intake.activate_intake(self.inputs["Intake"], "collect")

        if self.inputs["Climber Up"]:
            self.climber.move_climber("UP")
        elif self.inputs["Climber Down"]:
            self.climber.move_climber("DOWN")
        else:
            self.climber.move_climber("NEUTRAL")

        if self.inputs["Shooter Low"]:
            self.shooter.shoot_note(True, self.shooter.low_power_shot)
        if self.inputs["Shooter High"]:
            self.shooter.shoot_note(True, self.shooter.high_power_shot)
        else:
            self.shooter.shoot_note(False, 0)

    def testPeriodic(self):
        pass