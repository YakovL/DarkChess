"""
Extended serialization supporting `to_json()` method and
serializing simple dataclasses
"""
import json
from dataclasses import is_dataclass
from enum import Enum
from typing import Any, Dict

# is it needed in later Python versions?
class ExtendedJSONEncoder(json.JSONEncoder):
    """ Extends JSONEncoder with support of custom `to_json()` method
    and serializing simple dataclasses """
    def default(self, o: Any):

        if is_dataclass(o):
            data: Dict[str, Any] = {}
            for field in o.__dataclass_fields__.keys():
                value = getattr(o, field)
                data[str(field)] = self.serialize_unless_primitive(value)
            return data

        if hasattr(o, 'to_json'):
            return o.to_json()

        if hasattr(o, 'to_dict'):
            as_dict = o.to_dict()
            return self.serialize_unless_primitive(as_dict)

        if isinstance(o, dict):
            data: Dict[str, Any] = {}
            for key, value in o.items():
                data[key] = self.serialize_unless_primitive(value)
            return data

        if isinstance(o, list):
            return [self.serialize_unless_primitive(x) for x in o]

        return json.JSONEncoder.default(self, o)

    def serialize_unless_primitive(self, o: Any) -> Any:
        """ Only continues the transformation for non-primitives """
        if isinstance(o, (bool, str)) or \
           o is None:
            return o

        if isinstance(o, Enum):
            return o.name

        return self.default(o)

def to_json(obj: Any):
    """ Serializes `obj` to JSON """
    return json.dumps(obj, cls=ExtendedJSONEncoder)
