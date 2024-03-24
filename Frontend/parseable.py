from dataclasses import dataclass
from typing import Any

@dataclass
class Parseable:

    def parse(self, new_values: dict[str, Any]):
        for key, value in new_values.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print('missing', key)