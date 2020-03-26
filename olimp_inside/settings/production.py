from .base import *

DEBUG = True
STATIC_ROOT = "/srv/olimp-inside/public/static/"
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
        os.path.join(BASE_DIR, "../ui/public/")
]
ALLOWED_HOSTS = ["olimp2018.enhancelab.ru", "192.168.10.4", "inside.olimp-union.com"]
MEDIA_ROOT = "/srv/olimp-inside/public/media/"
