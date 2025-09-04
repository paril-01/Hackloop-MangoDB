# models package initializer - import model modules so they register on Base.metadata
from . import user  # noqa: F401
from . import activity  # noqa: F401
from . import automation  # noqa: F401
