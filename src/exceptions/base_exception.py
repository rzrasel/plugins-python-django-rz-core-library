class PluginError(Exception): pass
class PluginNotFoundError(PluginError):
    def __init__(self, name):
        super().__init__(f"Plugin '{name}' not found")