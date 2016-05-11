from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework_docs.settings import DRFSettings


class CacheMixin(object):
    def get_cache_prefix(self):
        settings = DRFSettings().settings
        return u"%s_%s_" % (settings['CACHE_PREFIX'], self._get_url_conf())

    def get_cache_timeout(self):
        settings = DRFSettings().settings
        return settings['CACHE_TIMEOUT']

    def dispatch(self, *args, **kwargs):
        timeout = self.get_cache_timeout()
        prefix = self.get_cache_prefix()
        return cache_page(timeout, key_prefix=prefix)(super(CacheMixin, self).dispatch)(*args, **kwargs)
