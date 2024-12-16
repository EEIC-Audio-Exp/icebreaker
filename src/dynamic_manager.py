class DynamicValueManager:
    def __init__(self):
        self.dynamic_value = "Let's start icebreak!"
    
    def set_value(self, value):
        self.dynamic_value = value
    
    def get_value(self):
        return self.dynamic_value

dynamic_value_manager = DynamicValueManager()
