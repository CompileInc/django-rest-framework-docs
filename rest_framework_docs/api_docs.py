from importlib import import_module
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern
from django.utils.module_loading import import_string
from rest_framework.views import APIView
from rest_framework_docs.api_endpoint import ApiEndpoint
from rest_framework_docs.settings import DRFSettings


class ApiDocumentation(object):

    def __init__(self, urlconf):
        self.endpoints = []
        try:
            root_urlconf = import_string(urlconf)
        except ImportError:
            # Handle a case when there's no dot in ROOT_URLCONF
            root_urlconf = import_module(urlconf)
        if hasattr(root_urlconf, 'urls'):
            self.get_all_view_names(root_urlconf.urls.urlpatterns)
        else:
            self.get_all_view_names(root_urlconf.urlpatterns)

    def get_all_view_names(self, urlpatterns, parent_pattern=None):
        settings = DRFSettings().settings
        for pattern in urlpatterns:
            if isinstance(pattern, RegexURLResolver):
                parent_pattern = None if pattern._regex == "^" else pattern
                self.get_all_view_names(urlpatterns=pattern.url_patterns, parent_pattern=parent_pattern)
            elif isinstance(pattern, RegexURLPattern) and self._is_drf_view(pattern) and not self._is_format_endpoint(pattern):
                api_endpoint = ApiEndpoint(pattern, parent_pattern)
                if not self._is_api_root(pattern) or not (self._is_api_root(pattern) and settings["HIDE_APIROOT"]):
                    self.endpoints.append(api_endpoint)

    def _is_drf_view(self, pattern):
        """
        Should check whether a pattern inherits from DRF's APIView
        """
        return hasattr(pattern.callback, 'cls') and issubclass(pattern.callback.cls, APIView)

    def _is_format_endpoint(self, pattern):
        """
        Exclude endpoints with a "format" parameter
        """
        return '?P<format>' in pattern._regex

    def _is_api_root(self, pattern):
        return pattern.callback.__name__ == "APIRoot"

    def get_endpoints(self):
        return self.endpoints
