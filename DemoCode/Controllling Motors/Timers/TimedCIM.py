import robotpy, wpilib, phoenix5   

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.motor_timer = wpilib.Timer()
        self.CIML = phoenix5.TalonSRX(1)  
        self.CIMR = phoenix5.TalonSRX(2)         # Replace ID with another number if 1 does not work.
        self.controller = wpilib.PS4Controller(0) # Replace IDcontroller with proper button.
        self.speed = 0.5

    def testInit(self):
        self.motor_timer.start()

    def testPeriodic(self):
        if self.motor_timer.get() > 0.5: #seconds
            self.CIM.set(phoenix5.ControlMode.PercentOutput, 0)
            
        else:
            self.CIM.set(phoenix5.ControlMode.PercentOutput, 0.05) #can change output here
        
    def testExit(self):
        self.motor_timer.stop()
        self.motor_timer.reset()