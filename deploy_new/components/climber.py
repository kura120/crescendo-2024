import wpilib, rev

class Climber:
    def __init__(self):
        idle_mode = rev.CANSparkMax.IdleMode.kBrake
        self.speed = 0.4
        self.climber_states = ["UP", "NEUTRAL", "DOWN"]
        self.climber_state = self.climber_states[0]
    
        self.climber_motor = rev.CANSparkMax(7, rev.CANSparkLowLevel.MotorType.kBrushless)   
        self.climber_motor.setIdleMode(idle_mode)

    def move_climber(self, direction):
        match direction:
            case "UP":
                self.climber_motor.set(self.speed)
                self.climber_state = self.climber_states[0]
            
            case "DOWN":
                self.climber_motor.set(-self.speed)
                self.climber_state = self.climber_states[2]
            
            case "NEUTRAL":
                self.climber_motor.set(0)
                self.climber_state = self.climber_states[1]
            