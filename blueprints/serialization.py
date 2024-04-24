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
                data[str(field)] = \
                    value if isinstance(value, bool) else \
                    value.name if isinstance(value, Enum) else \
                    self.default(value)
            return data

        if hasattr(o, 'to_json'):
            return o.to_json()

        return json.JSONEncoder.default(self, o)

def to_json(obj: Any):
    """ Serializes `obj` to JSON """
    return json.dumps(obj, cls=ExtendedJSONEncoder)
