
import wpilib, phoenix5

from components.intake import Intake

''' Shooter Code '''

class Shooter:
    def __init__(self):
        self.intake = Intake()

        idle_mode = phoenix5.NeutralMode.Coast
    
        self.low_power_shot = 0.1
        self.high_power_shot = 0.2

        self.delay = wpilib.Timer()
        self.delay_duration = 3.0

        left_motor = phoenix5.WPI_TalonSRX(9)
        right_motor = phoenix5.WPI_TalonSRX(10)

        left_motor.setNeutralMode(idle_mode)
        right_motor.setNeutralMode(idle_mode)

        self.outtake_motors = wpilib.MotorControllerGroup(left_motor, right_motor)

        self.outtake_motors.setInverted(True)

    def shoot_note(self, activate, motor_speed):
        if activate:
            self.outtake_motors.set(motor_speed)
            self.intake.shooting_speed.set(motor_speed)
            
            if self.delay.get() == 0:
                self.delay.start()
            elif self.delay.get() >= self.delay_duration:
                self.delay.stop()
                self.intake.activate_intake(True, "eject")
        
        else:
            self.delay.stop()
            self.delay.reset()
            self.intake.activate_intake(False, "eject")



        