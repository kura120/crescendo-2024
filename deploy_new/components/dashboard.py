import wpilib

class Dashboard:
    def __init__(self):
        pass

    def update_dashboard(self, items: dict):
        for key in items.keys():
            item = items[key]
            
            if type(item) is str:
                wpilib.SmartDashboard.putString(key, item)
            elif type(item) is float:
                wpilib.SmartDashboard.putNumber(key, item) 
            elif type(item) is bool:
                wpilib.SmartDashboard.putBoolean(key, item) 

            # match type(item):
            #     case <float>:
            #     case type(float):