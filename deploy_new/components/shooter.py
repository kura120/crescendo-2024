
import wpilib, phoenix5

from components.intake import Intake

''' Shooter Code '''

class Shooter:
    def __init__(self):
        # CHANGE THESE for SPEED
        self.default_amp = 0.4
        self.default_speaker = 0.7

        self.shooter_active = False
        self.intake = Intake()

        idle_mode = phoenix5.NeutralMode.Coast
        
        # DO NOT CHANGE THESE!
        self.low_power_shot = 0.4
        self.high_power_shot = 0.7

        self.delay = wpilib.Timer()
        self.delay_duration = 1.0

        left_motor = phoenix5.WPI_TalonSRX(9)
        right_motor = phoenix5.WPI_TalonSRX(10)

        left_motor.setNeutralMode(idle_mode)
        right_motor.setNeutralMode(idle_mode)

        left_motor.setInverted(True)
        right_motor.setInverted(True)

        self.outtake_motors = wpilib.MotorControllerGroup(left_motor, right_motor)


    def shoot_note(self, activate, motor_speed):
        if activate:
            self.shooter_active = True
            self.outtake_motors.set(motor_speed)
            self.intake.shooting_speed = motor_speed
            
            if self.delay.get() == 0:
                self.delay.start()

            if self.delay.get() >= self.delay_duration:
                self.delay.stop()
                print("GO.")
                self.intake.activate_intake(True, "eject")
        
        else:
            if self.shooter_active:
                self.intake.activate_intake(False, "eject")

            self.shooter_active = False
            self.outtake_motors.set(0)
            self.delay.stop()
            self.delay.reset()

        



        