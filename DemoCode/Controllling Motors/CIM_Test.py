import wpilib, phoenix5   

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

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.CIM = phoenix5.TalonSRX(1)         # Replace ID with another number if 1 does not work.
        self.joystick = wpilib.Joystick(1)

    def testPeriodic(self):
        self.CIM.set(phoenix5.ControlMode.PercentOutput, 0.1)