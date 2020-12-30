from .base import *

if DEBUG == True:
    from .local import *  # default for development only
else:
    from .production import *  # default for production only
