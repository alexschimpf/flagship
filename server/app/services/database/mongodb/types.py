from typing import TypedDict, Any, NotRequired
from enum import IntEnum
from datetime import datetime
from bson import ObjectId


class Operator(IntEnum):
    EQUALS = 1
    NOT_EQUALS = 2
    LESS_THAN = 3
    LESS_THAN_OR_EQUAL_TO = 4
    GREATER_THAN = 5
    GREATER_THAN_OR_EQUAL_TO = 6
    MATCHES_REGEX = 7
    IN_LIST = 8
    NOT_IN_LIST = 9
    INTERSECTS = 10
    NOT_INTERSECTS = 11
    CONTAINS = 12
    NOT_CONTAINS = 13


class ContextField(TypedDict):
    _id: NotRequired[ObjectId]
    name: str
    key: str
    value_type: str
    description: str
    created_date: datetime
    updated_date: datetime


class FeatureFlagConditions(TypedDict):
    context_key: str
    operator: Operator
    value: Any


class FeatureFlag(TypedDict):
    _id: NotRequired[ObjectId]
    name: str
    description: str
    created_date: datetime
    updated_date: datetime
    conditions: list[FeatureFlagConditions]
    enabled: bool


class Project(TypedDict):
    _id: NotRequired[ObjectId]
    name: str
    context_fields: list[ContextField]
    feature_flags: list[FeatureFlag]
    created_date: datetime
    updated_date: datetime
