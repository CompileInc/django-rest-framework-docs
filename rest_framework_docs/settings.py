from django.conf import settings

class DRFSettings(object):

    def __init__(self):
        self.drf_settings = {
            "HIDE_DOCS": self.get_setting("HIDE_DOCS") or False,
            "HIDE_LIVE_ENDPOINTS": self.get_setting("HIDE_LIVE_ENDPOINTS") or False,
            "HIDE_HIDDEN_FIELDS": self.get_setting("HIDE_HIDDEN_FIELDS") or False,
            "HIDE_APIROOT": self.get_setting("HIDE_APIROOT") or False,
            "DEFAULT_URLCONF": settings.ROOT_URLCONF,
            "CACHE_PREFIX": "DRFDOCS",
            "CACHE_TIMEOUT": self.get_setting("CACHE_TIMEOUT") or 0,
        }
        self.drf_settings["URLCONF"] = self.get_setting("URLCONF") or self.drf_settings["DEFAULT_URLCONF"]

    def get_setting(self, name):
        try:
            return settings.REST_FRAMEWORK_DOCS[name]
        except:
            return None

    @property
    def settings(self):
        return self.drf_settings
