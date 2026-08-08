# Install Plugin - Rz Core Library:
Make sure Django venv has the library:

### Go to project directory
```bash
› cd C:\Rz Rasel\python-django-project\python-django-test-2
```

```bash
› activate your venv
› .\venv\Scripts\activate
› .\.venv\Scripts\activate
```

### Install your lib into Django venv:

```bash
pip install -e ..\rz-core-libarary\ --no-cache-dir
```

```bash
pip install -e ..\rz-core-libarary\ --no-cache-dir --force-reinstall
```

### Install directly from GitHub in any Django project:

```bash
pip install git+https://github.com/rzrasel/plugins-python-django-rz-core-library.git --no-cache-dir --force-reinstall
```

#### Full Path:

```bash
pip install -e "C:\Users\Rz Rasel\plugins-python-django-rz-core-library" --no-cache-dir --force-reinstall
```

### Build Plugin Rz Core Library:

```bash
python -m pip install -e. --no-cache-dir --force-reinstall
python -c "from plugins.manager import manager; print(manager.all())"
```

```bash
python -c "from rzcorelibrary import get_plugin; S=get_plugin('string_utils'); print(S.to_escape_string(\"' OR 1=1\"))"
=> Will print \' OR 1=1

python -c "import sys; sys.path.insert(0,'src'); from rzcorelibrary import get_plugin; S=get_plugin('string_utils'); print(S.to_escape_string(\"' OR 1=1\"))"
```

```bash
python -m pip install -e . --no-cache-dir --force-reinstall
python -c "from plugins.manager import manager; print(manager.all())"
```

```bash
python -m pip install -e . --no-cache-dir --force-reinstall
python -c "import rzcorelibrary.utilities; import pkgutil; print(list(pkgutil.iter_modules(rzcorelibrary.utilities.__path__)))"
python -c "from plugins.manager import manager; print(manager.all())"
```

```bash
python -m pip install -e . --no-cache-dir --force-reinstall
python -c "from plugins.manager import manager; print(manager.all())"
python -c "from rzcorelibrary import get_plugin; S=get_plugin('string_utils'); print(S.escape_string(\"'test\"))"
```


```bash
rz-core-library/
│
├── src/
│   ├── plugins/
│   │   └── base.py
│   │
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── base_exception.py
│   │
│   └── rzcorelibrary/
│       ├── __init__.py
│       │
│       ├── utilities/
│       │   ├── __init__.py
│       │   ├── string_utils.py
│       │   └── user_ip_util.py
│       │
│       └── security/
│           ├── __init__.py
│           └── ...
│
├── tests/
│   ├── utilities/
│   └── security/
│
├── examples/
│
├── .gitignore
├── LICENSE
├── README.md
└── pyproject.toml
```

```bash
rz-core-library/
├── src/
│ └── rzcorelibrary/
│ ├── __init__.py # from.utilities import get_utility
│ ├── _version.py # __version__ = "0.1.0"
│ └──── utilities/ # <-- YOUR PLUGIN LIBRARY DIRECTORY
│ ├──── __init__.py # PluginManager + get_utility()
│ ├──── base.py # BaseUtilityPlugin
│ ├──── registry.py # Storage
│ ├──── manager.py # Auto-loader for this folder
│ ├──── string_utils.py # Plugin 1
│ └──── user_ip_util.py # Plugin 2
│ ├── py.typed # PEP 561 marker
│ ├── exceptions/
│ │ └── __init__.py # PluginNotFoundError
├── tests/
├── examples/
├── pyproject.toml
├── README.md
├── LICENSE
└──.gitignore
```