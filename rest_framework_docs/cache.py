class CacheMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def get_cache_prefix(self):
        return self.cache_prefix

    def dispatch(self, *args, **kwargs):
        timeout = self.get_cache_timeout()
        prefix = self.get_cache_prefix()
        return cache_page(timeout, key_prefix=prefix)(super(CacheMixin, self).dispatch)(*args, **kwargs)
