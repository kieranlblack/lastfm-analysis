import json
from abc import ABC, abstractmethod


class PrettyPrintable(ABC):
    @abstractmethod
    def as_dict(self):
        pass

    def _stringified_as_dict(self):
        def default_to_as_dict(o):
            try:
                return o.as_dict()
            except AttributeError:
                raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")
        return json.dumps(self.as_dict(), sort_keys=True, indent=2, ensure_ascii=False, default=default_to_as_dict)

    def __str__(self) -> str:
        return self._stringified_as_dict()

    def __repr__(self) -> str:
        return self._stringified_as_dict()
