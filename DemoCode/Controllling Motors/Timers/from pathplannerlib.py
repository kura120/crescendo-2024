from pathplannerlib.auto import PathPlannerAuto

class RobotContainer:
    def getAutonomousCommand():
        return PathPlannerAuto('Example Auto')
    



from pathplannerlib.auto import AutoBuilder
from pathplannerlib.config import ReplanningConfig, PIDConstants

class DriveSubsystem(Subsystem):
    def __init__(self):
        # subsystem initialization here
        # ...

        # Configure the AutoBuilder last
        AutoBuilder.configureRamsete(
            self.getPose, # Robot pose supplier
            self.resetPose, # Method to reset odometry (will be called if your auto has a starting pose)
            self.getCurrentSpeeds, # Current ChassisSpeeds supplier
            self.drive, # Method that will drive the robot given ChassisSpeeds
            ReplanningConfig(), # Default path replanning config. See the API for the options here
            self.shouldFlipPath, # Supplier to control path flipping based on alliance color
            self # Reference to this subsystem to set requirements
        )

    def shouldFlipPath():
        # Boolean supplier that controls when the path will be mirrored for the red alliance
        # This will flip the path being followed to the red side of the field.
        # THE ORIGIN WILL REMAIN ON THE BLUE SIDE
        return DriverStation.getAlliance() == DriverStation.Alliance.kRed