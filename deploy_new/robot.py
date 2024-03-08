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
            "Max Drive Power": self.drive.default_speed,
            "Speaker Shot Power": self.shooter.high_power_shot,
            "Amp Shot Power": self.shooter.high_power_shot,
            "Intake Power": self.shooter.intake.default_speed,
            "Intake Back Power": self.shooter.intake.default_reverse_speed,
            "Climber Power": self.climber.default_speed,
            "Drive Style": self.drive.drive_style 
        }
    
        self.dashboard.update_dashboard(dashboard_mutables)

    def robotPeriodic(self):
        '''
        Current input map:
        D-Pad UP/DOWN - Climber
        Left Stick Up/Down - Arcade Drive Forward / Tank Drive Left
        Right Stick Up/Down - Tank Drive Right
        Right Stick Left/Right - Arcade Drive Rotate
        L2 - Intake
        R2 - Speaker Shot
        L1 - Brake (slows down your drive speed by half, use for more precise control)
        R1 - Amp Shot (try to refrain from using)
        '''

        self.inputs = {         
            "AD Forward Axis": -self.controller.getRawAxis(1),
            "Tank Left Axis": -self.controller.getRawAxis(1),
            "AD Rotate Axis": self.controller.getZ(),
            "Tank Right Axis": -self.controller.getRawAxis(5),
            "Drive Brake": self.controller.getRawButton(5),
            "Shooter Low": self.controller.getRawButton(6),
            "Shooter High": self.controller.getRawButton(8),
            "Intake": self.controller.getRawButton(7),
            "Climber Up": self.controller.getPOV() == 0,
            "Climber Down": self.controller.getPOV() == 180,
        }

        self.stats_for_dashboard = {
            "Left Drive Power": self.drive.left_drive_train.get(),
            "Right Drive Power": self.drive.right_drive_train.get(),
            "Climber State": self.climber.climber_state,
        }

        self.dashboard.update_dashboard(self.stats_for_dashboard)
        self.drive.speed = self.dashboard.fetch_dashboard_value("Max Drive Power", self.drive.speed, self.drive.default_speed)
        self.shooter.high_power_shot = self.dashboard.fetch_dashboard_value("Speaker Shot Power", self.shooter.high_power_shot, self.shooter.default_speaker)
        self.shooter.low_power_shot = self.dashboard.fetch_dashboard_value("Amp Shot Power", self.shooter.low_power_shot, self.shooter.default_amp)
        self.shooter.intake.speed = self.dashboard.fetch_dashboard_value("Intake Power", self.shooter.intake.speed, self.shooter.intake.default_speed)
        self.shooter.intake.back_speed = self.dashboard.fetch_dashboard_value("Intake Back Power", self.shooter.intake.back_speed, self.shooter.intake.default_reverse_speed)    

    def teleopPeriodic(self):
        match self.drive.drive_style:
            case "arcade":
                self.drive.arcade_drive(self.inputs["AD Forward Axis"], self.inputs["AD Rotate Axis"], self.inputs['Drive Brake'])
            case "tank":
                self.drive.tank_drive(self.inputs["Tank Left Axis"], self.inputs["Tank Right Axis"], self.inputs['Drive Brake'])

        if self.inputs["Climber Up"]:
            self.climber.move_climber("UP")
        elif self.inputs["Climber Down"]:
            self.climber.move_climber("DOWN")
        else:
            self.climber.move_climber("NEUTRAL")
        
        if not(self.shooter.shooter_active):
            self.shooter.intake.activate_intake(self.inputs["Intake"], "collect")

        if self.inputs["Shooter Low"]:
            self.shooter.shoot_note(True, self.shooter.low_power_shot)
        elif self.inputs["Shooter High"]:
            self.shooter.shoot_note(True, self.shooter.high_power_shot)
        else:
            self.shooter.shoot_note(False, 0)

