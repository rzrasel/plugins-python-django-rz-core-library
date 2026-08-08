from plugins.manager import manager
from exceptions.base_exception import PluginNotFoundError
from rzcorelibrary.version import __version__, __version_info__

def get_plugin(name: str):
    util = manager.get(name)
    if not util:
        raise PluginNotFoundError(name)
    return util

__all__ = ["get_plugin", "manager", "__version__", "PluginNotFoundError"]

'''try:
    from plugins.manager import manager
    from exceptions.base_exception import PluginNotFoundError
    from rzcorelibrary.version import __version__
except ImportError:
    from.version import __version__
    from..plugins.manager import manager
    from..exceptions.base_exception import PluginNotFoundError

def get_plugin(name: str):
    util = manager.get(name)
    if not util:
        raise PluginNotFoundError(name)
    return util'''