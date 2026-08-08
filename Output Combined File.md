/ File: C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary\src\exceptions\__init__.py **/

from .base_exception import PluginError, PluginNotFoundError

__all__ = ["PluginError", "PluginNotFoundError"]

/ File: C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary\src\exceptions\base_exception.py **/

class PluginError(Exception): pass
class PluginNotFoundError(PluginError):
    def __init__(self, name):
        super().__init__(f"Plugin '{name}' not found")

/ File: C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary\src\plugins\__init__.py **/

try:
    from .manager import manager
except ImportError:
    from .manager import manager

__all__ = ["manager"]

/ File: C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary\src\plugins\base.py **/

from abc import ABC, abstractmethod
from typing import Any

class BasePlugin(ABC):
    """
    Base class for all rz-core-library plugins
    Every plugin in src/rzcorelibrary/utilities/ and security/ must inherit this
    """
    name: str = ""
    version: str = "1.0.0"
    description: str = ""

    @abstractmethod
    def get_util(self) -> Any:
        """
        Return the utility class
        Example: return StringUtils
        """
        pass

    def get_info(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description
        }

/ File: C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary\src\plugins\manager.py **/

import pkgutil
import importlib
import importlib.metadata

try:
    from .registry import Registry
except ImportError:
    from .registry import Registry

PLUGIN_DIRS = [
    "rzcorelibrary.utilities",
    "rzcorelibrary.security"
]

class PluginManager(Registry):
    def load_all(self):
        for package_name in PLUGIN_DIRS:
            try:
                package = importlib.import_module(package_name)
            except ModuleNotFoundError:
                continue

            if not hasattr(package, "__path__"):
                continue

            for _, mod_name, _ in pkgutil.iter_modules(package.__path__):
                try:
                    module = importlib.import_module(f"{package_name}.{mod_name}")
                    if hasattr(module, "Plugin"):
                        p = module.Plugin()
                        self.register(p.name, p.get_util())
                except Exception as e:
                    import traceback
                    print(f"[rz-core-library] Failed to load {package_name}.{mod_name}:")
                    traceback.print_exc()

        # external plugins
        try:
            for ep in importlib.metadata.entry_points(group="rzcorelibrary.plugins"):
                p = ep.load()()
                self.register(p.name, p.get_util())
        except Exception:
            pass

manager = PluginManager()
manager.load_all()

/ File: C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary\src\plugins\registry.py **/

class Registry:
    def __init__(self):
        self._store = {}

    def register(self, name: str, obj):
        self._store[name] = obj

    def get(self, name: str):
        return self._store.get(name)

    def all(self):
        return self._store

/ File: C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary\src\rzcorelibrary\utilities\__init__.py **/



/ File: C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary\src\rzcorelibrary\utilities\string_utils.py **/

# File Name: string_utils.py
try:
    from plugins.base import BasePlugin
except ImportError:
    from ...plugins.base import BasePlugin

class StringUtils:

    @staticmethod
    def escape_string(value: str | bytes | None) -> str | bytes | None:
        if value is None:
            return None

        # MySQL escaping: \ first, then others
        if isinstance(value, bytes):
            return (
                value.replace(b"\\", b"\\\\")
                .replace(b"\0", b"\\0")
                .replace(b"\n", b"\\n")
                .replace(b"\r", b"\\r")
                .replace(b"\x1a", b"\\Z")
                .replace(b"'", b"\\'")
                .replace(b'"', b'\\"')
            )

        return (
            value.replace("\\", "\\\\")
            .replace("\0", "\\0")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\x1a", "\\Z")
            .replace("'", "\\'")
            .replace('"', '\\"')
        )

/ File: C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary\src\rzcorelibrary\__init__.py **/

from plugins.manager import manager
from exceptions.base_exception import PluginNotFoundError
from rzcorelibrary.version import __version__, __version_info__

def get_plugin(name: str):
    util = manager.get(name)
    if not util:
        raise PluginNotFoundError(name)
    return util

__all__ = ["get_plugin", "manager", "__version__", "PluginNotFoundError"]

/ File: C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary\src\rzcorelibrary\version.py **/

__version__ = "0.1.0"
__version_info__ = (0, 1, 0)

/ File: C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary\pyproject.toml **/

[project]
name = "rz-core-library"
dynamic = ["version"]
description = "RZ Core Library with utilities and security plugins"
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}

authors = [
    { name = "Rz Rasel" }
]

dependencies = []

[project.entry-points."rzcorelibrary.plugins"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.version]
path = "src/rzcorelibrary/version.py"

[tool.hatch.build.targets.wheel]
packages = ["src/rzcorelibrary"]

[tool.hatch.build.targets.wheel.force-include]
"src/plugins" = "plugins"
"src/exceptions" = "exceptions"




C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary>
C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary>python -m pip install -e . --no-cache-dir --force-reinstall
Obtaining file:///C:/Users/OMEN/Desktop/2026-01-05/Rz%20Rasel%20Tutorial/python-django-project/python-django-test-2/rz-core-libarary
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Installing backend dependencies ... done
  Preparing editable metadata (pyproject.toml) ... done
Building wheels for collected packages: rz-core-library
  Building editable for rz-core-library (pyproject.toml) ... done
  Created wheel for rz-core-library: filename=rz_core_library-0.1.0-py3-none-any.whl size=3827 sha256=cb580ca6e158c306c73b798d503c7baeccdb02e8772691ce3b0f9cc1e8a74275
  Stored in directory: C:\Users\OMEN\AppData\Local\Temp\pip-ephem-wheel-cache-n6nulcrv\wheels\f2\a7\02\ccb138584385cd1b5efc6418ba3d533c62c0a6ee549bfb3981
Successfully built rz-core-library
Installing collected packages: rz-core-library
  Attempting uninstall: rz-core-library
    Found existing installation: rz-core-library 0.1.0
    Uninstalling rz-core-library-0.1.0:
      Successfully uninstalled rz-core-library-0.1.0
Successfully installed rz-core-library-0.1.0

C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary>python -c "from plugins.manager import manager; print(manager.all())"
{}

C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary>python -c "from rzcorelibrary import get_plugin; S=get_plugin('string_utils'); print(S.escape_string(\"'test\"))"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from rzcorelibrary import get_plugin; S=get_plugin('string_utils'); print(S.escape_string("'test"))
                                            ~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary\src\rzcorelibrary\__init__.py", line 8, in get_plugin
    raise PluginNotFoundError(name)
exceptions.base_exception.PluginNotFoundError: Plugin 'string_utils' not found

C:\Users\OMEN\Desktop\2026-01-05\Rz Rasel Tutorial\python-django-project\python-django-test-2\rz-core-libarary>