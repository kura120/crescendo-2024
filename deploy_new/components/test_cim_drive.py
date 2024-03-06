'''
Chassis drive module
Made for CIMs
'''

import wpilib, wpilib.drive, phoenix5


class Drive:
    def __init__(self):
        ''' Creating the drive train '''
        # Parameters:
        self.speed = 0.5

        # Defining motor type
        idle_mode = phoenix5.NeutralMode.Coast

        # Creating motor objects
        self.left_motor_a = phoenix5.WPI_TalonSRX(1)
        self.right_motor_a = phoenix5.WPI_TalonSRX(2)
        self.left_motor_b = phoenix5.WPI_TalonSRX(3)
        self.right_motor_b = phoenix5.WPI_TalonSRX(4)

        motors = [self.left_motor_a, self.right_motor_a, self.left_motor_b, self.right_motor_b]  
        # Setting motor idle mode and creating encoder instances
        for motor in motors:
            motor.setNeutralMode(idle_mode)

        # Create drive trains
        self.left_drive_train = wpilib.MotorControllerGroup(self.left_motor_a, self.left_motor_b)
        self.right_drive_train = wpilib.MotorControllerGroup(self.right_motor_a, self.right_motor_b)

        self.right_drive_train.setInverted(True)

        self.mean_encoder_position: list[float] = []

        self.robot_drive = wpilib.drive.DifferentialDrive(leftMotor=self.left_drive_train, rightMotor=self.right_drive_train)


    def arcade_drive(self, forward, rotate):
        self.robot_drive.setMaxOutput(self.speed)
        self.robot_drive.arcadeDrive(xSpeed=(forward), zRotation=(rotate))

    def tank_drive(self, left, right):
        self.robot_drive.setMaxOutput(self.speed)
        self.robot_drive.tankDrive(leftSpeed=left * self.speed, rightSpeed=right*self.speed)
        