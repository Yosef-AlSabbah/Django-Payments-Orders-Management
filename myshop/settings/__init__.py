from decouple import config

if config('PIPELINE') == 'production':
    from .production import *
else:
    from .local import *