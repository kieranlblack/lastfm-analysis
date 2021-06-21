from abc import ABC, abstractmethod
import json


class PrettyPrintable(ABC):
    @property
    @abstractmethod
    def dict_representation(self):
        pass

    @property
    def stringified_dict_representation(self):
        return json.dumps(self.dict_representation, sort_keys=True, indent=2, ensure_ascii=False)

    def __str__(self) -> str:
        return self.stringified_dict_representation

    def __repr__(self) -> str:
        return self.stringified_dict_representation
