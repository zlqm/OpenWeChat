###################################
# Schema
###################################
class Missing:
    pass


_missing = Missing()


class Field:
    def __init__(self, *, default=_missing):
        self.default = default

    def serialize(self, value):
        return self.cast_func(value)

    def deserialize(self, value):
        return self.cast_func(value)

    def cast_func(self, value):
        return value


class Int(Field):
    cast_func = int


class Str(Field):
    cast_func = str


class Json(Field):
    pass


class SchemaMetaClass(type):
    def __new__(cls, cls_name, bases, cls_dict):
        _data_fields = {}
        for base in bases:
            _data_fields.update(getattr(base, '_data_fields', {}))
        for key, value in cls_dict.items():
            if isinstance(value, Field):
                _data_fields[key] = value
        for key in _data_fields:
            if key in cls_dict:
                cls_dict.pop(key)
        cls_dict.update(_data_fields=_data_fields)
        return super().__new__(cls, cls_name, bases, cls_dict)


class Schema(dict, metaclass=SchemaMetaClass):
    def __init__(self, **kwargs):
        origin_kwargs, kwargs = kwargs, {}
        for key, field in self._data_fields.items():
            if key in origin_kwargs:
                kwargs[key] = field.deserialize(origin_kwargs[key])
            else:
                if field.default is not _missing:
                    kwargs[key] = field.default
                else:
                    msg = 'field {} does not has a default value'.format(key)
                    raise ValueError(msg)
        super().__init__(**kwargs)

    def __getattr__(self, key):
        return self[key]


##############################
# MISC
##############################
def walk_subclass(cls):
    for subclass in cls.__subclasses__():
        yield subclass
        for sub_subclass in walk_subclass(subclass):
            yield sub_subclass



#############
# xml
#############
def get_xml_node_value(xml_data, key):
    value = xml_data.find(key)
    if value is None:
        raise KeyError('cannot find node: {}'.format(key))
    return value.text

# TODO: use lxml to improve performance
