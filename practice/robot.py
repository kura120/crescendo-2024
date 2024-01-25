import robotpy, wpilib, wpilib.drive, rev, math

class MyRobot(wpilib.TimedRobot):
    cim_motor = wpilib.CANStatus()
    print(cim_motor)

if __name__ == "__main__":
    wpilib.run(MyRobot)