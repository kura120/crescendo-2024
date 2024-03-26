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
from math import pi


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.drive = Drive()
        self.shooter = Shooter()
        self.climber = Climber()
        self.dashboard = Dashboard()
        self.controller = wpilib.Joystick(0)

        dashboard_mutables = {
            "Max Drive Power": self.drive.default_speed,
            "Intake Power": self.shooter.intake.default_speed,
            "Intake Back Power": self.shooter.intake.default_reverse_speed,
            "Climber Power": self.climber.default_speed,
            "Drive Style": self.drive.drive_style 
        }
    
        self.dashboard.update_dashboard(dashboard_mutables)

    def autonomousInit(self):
        self.encoder_wheel_distance = (42 * 14) / (6 * pi)
        self.auto_mode = "simple move"
        self.time = wpilib.Timer()
        self.time.start()

    def autonomousPeriodic(self):
        match self.auto_mode:
            case "simple move":
                if self.time.get() < 3:
                    self.drive.tank_drive(0.5, 0.5, False)
                else:
                    self.time.stop()
                    self.drive.tank_drive(0,0, False)
            case "shoot":
                self.shooter.delay_duration = 3
                self.shooter.shoot_note(True, [1, 1])
                if self.time.get() > 5: 
                    # self.shooter.delay_duration = 2
                    self.shooter.shoot_note(False, [0, 0])


    def robotPeriodic(self):
        self.alliance = wpilib.DriverStation.getAlliance()

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
            "Reverse Intake from Shooter": self.controller.getRawButton(5),
            "Drive Brake": self.controller.getRawButton(2),
            "High Shot": self.controller.getRawButton(6), 
            "Low Shot": self.controller.getRawButton(8),
            "Intake": self.controller.getRawButton(7),
            "Climber Up": self.controller.getPOV() == 0,
            "Climber Down": self.controller.getPOV() == 180,
        }

        self.stats_for_dashboard = {
            "Left Drive Power": self.drive.left_drive_train.get() * 100,
            "Right Drive Power": self.drive.right_drive_train.get() * 100,
            "Climber State": self.climber.climber_state,
            "Shot Timer": self.shooter.delay_duration - self.shooter.delay.get(),
            "Shooter Power A": self.shooter.motor_A.get(),
            "Shooter Power B": self.shooter.motor_B.get(),
        
        }
        self.dashboard.update_dashboard(self.stats_for_dashboard)

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
        

        if self.inputs["Reverse Intake from Shooter"]:
            self.shooter.reverse_intake_from_shooter()
        elif self.inputs["High Shot"]:
            self.shooter.shoot_note(True, self.shooter.high_power_shot)
        elif self.inputs["Low Shot"]:
            self.shooter.shoot_note(True, self.shooter.low_power_shot)
        elif not(self.shooter.shooter_active):
            self.shooter.intake.activate_intake(self.inputs["Intake"], "collect")
        else:
            self.shooter.shoot_note(False, 0)

