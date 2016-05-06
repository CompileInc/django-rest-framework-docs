import json
import inspect
from django.contrib.admindocs.views import simplify_regex
from django.core.validators import EMPTY_VALUES
from django.utils.encoding import force_str
from rest_framework_docs.settings import DRFSettings


class ApiEndpoint(object):

    def __init__(self, pattern, parent_pattern=None):
        self.pattern = pattern
        self.callback = pattern.callback
        # self.name = pattern.name
        self.docstring = self.__get_docstring__()
        self.name_parent = simplify_regex(parent_pattern.regex.pattern).strip('/') if parent_pattern else None
        self.path = self.__get_path__(parent_pattern)
        self.allowed_methods = self.__get_allowed_methods__()
        # self.view_name = pattern.callback.__name__
        self.errors = None
        self.fields = self.__get_serializer_fields__()
        self.fields_json = self.__get_serializer_fields_json__()
        self.filters = self.__get_filter_fields__()
        self.permissions = self.__get_permissions_class__()

    def __get_path__(self, parent_pattern):
        if parent_pattern:
            return "/{0}{1}".format(self.name_parent, simplify_regex(self.pattern.regex.pattern))
        return simplify_regex(self.pattern.regex.pattern)

    def __get_allowed_methods__(self):
        return [force_str(m).upper() for m in self.callback.cls.http_method_names if hasattr(self.callback.cls, m)]

    def __get_docstring__(self):
        return inspect.getdoc(self.callback)

    def __get_permissions_class__(self):
        for perm_class in self.pattern.callback.cls.permission_classes:
            return perm_class.__name__

    def _is_hidden_field(self, field):
        return "Hidden" in field.__class__.__name__

    def __get_serializer_fields__(self):
        fields = []
        settings = DRFSettings().settings

        if hasattr(self.callback.cls, 'serializer_class') and hasattr(self.callback.cls.serializer_class, 'get_fields'):
            serializer = self.callback.cls.serializer_class
            if hasattr(serializer, 'get_fields'):
                try:
                    fields = [{
                        "name": key,
                        "type": str(field.__class__.__name__),
                        "required": field.required
                    } for key, field in serializer().get_fields().items() \
                              if (settings['HIDE_HIDDEN_FIELDS'] and not self._is_hidden_field(field)) or\
                                 (not settings['HIDE_HIDDEN_FIELDS'])]
                except KeyError as e:
                    self.errors = e
                    fields = []

                # FIXME:
                # Show more attibutes of `field`?

        return fields

    def __get_filters__(self, filter_backend):
        filter_data =  {'backend_name': filter_backend.__name__,
                        'filter_fields': [],
                        'search_param': None,
                        'ordering': {}
                        }

        filter_class = None
        get_filter_class = getattr(filter_backend, "get_filter_class", None)
        if callable(get_filter_class):
            try:
                try:
                    qs = self.callback.cls().get_queryset()
                except:
                    qs = self.callback.cls().model.objects.all()
                filter_class = filter_backend().get_filter_class(view=self.callback.cls,
                                                                 queryset=qs)
            except:
                pass

            # FIXME:
            # Have a better mechanism to extract fields

        if filter_class:
            filter_data['filter_fields'] = filter_class.__dict__['base_filters'].items()

        if hasattr(filter_backend, 'search_param'):
            filter_data['search_param'] = filter_backend.search_param

        # Checks if ordering_fields are set in the view before setting them
        if hasattr(filter_backend, 'ordering_fields') and hasattr(self.callback.cls, 'ordering_fields')\
           and self.callback.cls.ordering_fields:
            filter_data['ordering'] = {'ordering_fields': self.callback.cls.ordering_fields,
                                       'ordering_param': filter_backend.ordering_param}

        return filter_data

    def __get_filter_fields__(self):
        _filters = {
                    'filter_fields':{},
                    'search_param': None,
                    'ordering': {},
                    }

        filters = []
        if hasattr(self.callback.cls, 'filter_backends'):
            filters = [self.__get_filters__(backend) for backend in self.callback.cls.filter_backends]

        # Squash across filters
        for f in filters:
            for field in f['filter_fields']:
                _filters['filter_fields'][field[0]] = field[1]

            if f['search_param'] not in EMPTY_VALUES:
                _filters['search_param'] = f['search_param']

            if f['ordering'] not in EMPTY_VALUES:
                _filters['ordering'] = f['ordering']

        return _filters

    def __get_serializer_fields_json__(self):
        # FIXME:
        # Return JSON or not?
        return json.dumps(self.fields)
