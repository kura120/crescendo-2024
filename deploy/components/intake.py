'''
Intake Code
FRC 3340 Coding Team

What it's supposed to do:
When driver holds the intake button down on their controller, the intake motors should spin.
Upon releasing the button, the intake motors do a partial rotation to keep the note in the shooter.

Code before 2/27 WORKS
Changes untested
'''


import wpilib, rev

class Intake:
    def __init__(self):

        # Change THESE
        self.default_speed = 0.5    
        self.default_reverse_speed = 0.1

        # NOT these
        self.speed = 0.3
        self.back_speed = 0.1          
        self.shooting_speed = 0        # Changed by shooter.py

        motor_type = rev.CANSparkMax.MotorType.kBrushless
        idle_mode = rev.CANSparkMax.IdleMode.kCoast

        self.intake_motor = rev.CANSparkMax(8, motor_type)
        self.intake_motor.setIdleMode(idle_mode)
        self.intake_motor.setInverted(True)

        self.reverse_intake_timer = wpilib.Timer()
        self.reverse_intake_duration = 0.2

        # Intake-specific:
        self.using_intake = False            


    def activate_intake(self, enabled, mode: str):
        match mode:
            case "eject":
                if enabled:
                    self.intake_motor.set(self.shooting_speed)
                else:
                    self.intake_motor.set(0)
            
            case "collect":
                if enabled:
                    if not(self.using_intake):
                        self.reverse_intake_timer.reset()
                        self.reverse_intake_timer.stop()
                        self.using_intake = True

                    self.intake_motor.set(self.speed)

                else:
                    
                    if self.using_intake:
                        self.using_intake = False
                        self.reverse_intake_timer.start()
                        self.intake_motor.set(-self.back_speed)
                    
                    if self.reverse_intake_timer.get() >= self.reverse_intake_duration:
                        self.intake_motor.set(0)
                        self.reverse_intake_timer.stop()
