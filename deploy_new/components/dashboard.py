import wpilib

class Dashboard:

    def update_dashboard(self, items: dict):
        for key in items.keys():
            item = items[key]
            if type(item) is str:
                wpilib.SmartDashboard.putString(key, item)
            elif type(item) is float or type(item) is int:
                wpilib.SmartDashboard.putNumber(key, item) 
            elif type(item) is bool:
                wpilib.SmartDashboard.putBoolean(key, item) 

    def fetch_dashboard_value(self, key, value, default):
        if type(value) is str:
            return wpilib.SmartDashboard.getString(key, default)
        elif type(value) is float or type(value) is int:
            return wpilib.SmartDashboard.getNumber(key, default)
        elif type(value) is bool:
            return wpilib.SmartDashboard.getBoolean(key, default)
        

    