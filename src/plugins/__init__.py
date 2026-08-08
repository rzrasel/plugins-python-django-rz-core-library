try:
    from .manager import manager
except ImportError:
    from .manager import manager

__all__ = ["manager"]