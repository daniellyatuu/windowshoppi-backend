from .base import *

# local.py and production.py all inherit from base.py

from .production import *  # default for production only
try:
    from .local import *  # default for development only
except:
    pass
