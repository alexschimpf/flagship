from pydantic import BaseModel


class FeatureFlags(BaseModel):
    items: list[str]
