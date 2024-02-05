from typing import TypedDict
from pydantic import BaseModel


class FeatureFlags(BaseModel):
    items: list[str]
