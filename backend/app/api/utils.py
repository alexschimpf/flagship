from enum import Enum
from typing import Type


def get_enum_description(enum: Type[Enum]) -> str:
    name_to_val = {
        name: val.value
        for name, val in enum.__members__.items()
    }
    description = []
    for name, val in name_to_val.items():
        clean_name = name.lower().replace('_', ' ')
        description.append(f'{clean_name}: {val}')
    return '</br>'.join(description)
