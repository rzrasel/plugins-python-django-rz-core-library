import pkgutil
import importlib
import importlib.metadata

try:
    from .registry import Registry
except ImportError:
    from .registry import Registry

PLUGIN_DIRS = [
    "rzcorelibrary.generator",
    "rzcorelibrary.generator.database",
    "rzcorelibrary.generator.general",
    "rzcorelibrary.http.header",
    "rzcorelibrary.http.response",
    "rzcorelibrary.language",
    "rzcorelibrary.language.mapping",
    "rzcorelibrary.language.transliterate",
    "rzcorelibrary.log",
    "rzcorelibrary.security",
    "rzcorelibrary.utilities",
    "rzcorelibrary.utilities.http",
    "rzcorelibrary.utilities.string",
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