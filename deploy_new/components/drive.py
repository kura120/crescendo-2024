'''
Chassis drive module
Made for NEO
'''

import wpilib, wpilib.drive, rev

class Drive:
    def __init__(self):
        ''' Creating the drive train '''
        # Parameters:
        self.speed = 0.75

        # Defining motor type
        motor_type = rev.CANSparkMax.MotorType.kBrushless
        idle_mode = rev.CANSparkMax.IdleMode.kCoast

        # Creating motor objects
        self.left_motor_a = rev.CANSparkMax(1, motor_type)
        self.right_motor_a = rev.CANSparkMax(2, motor_type)
        self.left_motor_b = rev.CANSparkMax(3, motor_type)
        self.right_motor_b = rev.CANSparkMax(4, motor_type)

        motors = [self.left_motor_a, self.right_motor_a, self.left_motor_b, self.right_motor_b]
        self.encoders = []
        
        # Setting motor idle mode and creating encoder instances
        for motor in motors:
            motor.setIdleMode(idle_mode)
            self.encoders.append(motor.getEncoder())

        # Create drive trains
        self.left_drive_train = wpilib.MotorControllerGroup(self.left_motor_a, self.left_motor_b)
        self.right_drive_train = wpilib.MotorControllerGroup(self.right_motor_a, self.right_motor_b)

        self.mean_encoder_position: list[float] = []

        self.robot_drive = wpilib.drive.DifferentialDrive(leftMotor=self.left_drive_train, rightMotor=self.right_drive_train)

    def update_encoder_position(self):
        self.mean_encoder_position = [(self.encoders[0].getPosition() + self.encoders[2].getPosition()) / 2,
                                       (self.encoders[1].getPosition() + self.encoders[2].getPosition()) / 2]

    def calibrate_encoders(self):
        for encoder in self.encoders:
            encoder.setPosition(0)

    def move_robot(self, forward, rotate):
        self.robot_drive.arcadeDrive(xSpeed=forward * self.speed, zRotation=rotate * self.speed)
    
        