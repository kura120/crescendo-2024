
import wpilib, phoenix5
from components.intake import Intake

''' Shooter Code '''

class Shooter:
    def __init__(self):
        # CHANGE THESE for SPEED ([0] - A [1] - B)
        self.default_amp = [0.45, 0.4]
        self.default_speaker = [0.9, 0.4]


        self.shooter_active = False
        self.intake = Intake()

        idle_mode = phoenix5.NeutralMode.Coast
        
        # DO NOT CHANGE THESE!
        self.low_power_shot = self.default_amp
        self.high_power_shot = self.default_speaker

        self.delay = wpilib.Timer()
        self.delay_duration = 2
        
        self.wind_back_time = wpilib.Timer()
        self.wind_back_delay = 0.25

        self.motor_A = phoenix5.WPI_TalonSRX(9)
        self.motor_B = phoenix5.WPI_TalonSRX(10)

        self.motor_A.setNeutralMode(idle_mode)
        self.motor_B.setNeutralMode(idle_mode)

        self.motor_A.setInverted(True)
        self.motor_B.setInverted(True)

        # self.outtake_motors = wpilib.MotorControllerGroup(motor_A, motor_B)


    def shoot_note(self, activate, motor_speeds):
        if activate:
            # if not(self.shooter_active) and self.wind_back_time.get() < self.wind_back_delay:
            #     if self.wind_back_time == 0:
            #         self.wind_back_time.start()
            #         self.outtake_motors.set(-0.25)
            # else:
            # self.outtake_motors.set(0)
            # self.wind_back_time.stop()

            self.shooter_active = True
            self.wind_back_time.reset()
            self.motor_A.set(motor_speeds[0])
            self.motor_B.set(motor_speeds[1])
            self.intake.shooting_speed = (motor_speeds[0])
       
            if self.delay.get() == 0:
                self.delay.start()

            if self.delay.get() >= self.delay_duration:
                self.delay.stop()
                self.intake.activate_intake(True, "eject")
        
        else:
            if self.shooter_active:
                self.intake.activate_intake(False, "eject")
            self.shooter_active = False
            self.stop_shooter_motors()
            self.delay.stop()
            self.delay.reset()

    
    def reverse_intake_from_shooter(self):
        self.shooter_active = True
        self.motor_A.set(-.15)
        self.motor_B.set(-.15)

    def stop_shooter_motors(self):
        self.motor_A.set(0)
        self.motor_B.set(0)