from django.conf import settings


class DRFSettings(object):

    def __init__(self):
        self.drf_settings = {
            "HIDE_DOCS": self.get_setting("HIDE_DOCS") or False,
            "HIDE_LIVE_ENDPOINT": self.get_setting("HIDE_LIVE_ENDPOINT") or False,
            "HIDE_HIDDEN_FIELDS": self.get_setting("HIDE_HIDDEN_FIELDS") or False,
        }

    def get_setting(self, name):
        try:
            return settings.REST_FRAMEWORK_DOCS[name]
        except:
            return None

    @property
    def settings(self):
        return self.drf_settings
