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


class ContextValueType(IntEnum):
    STRING = 1
    NUMBER = 2
    INTEGER = 3
    BOOLEAN = 4
    ENUM = 5
    VERSION = 6
    STRING_LIST = 7
    INTEGER_LIST = 8
    ENUM_LIST = 9


class ContextField(TypedDict):
    _id: NotRequired[ObjectId]
    name: str
    key: str
    value_type: ContextValueType
    description: str
    enum_def: str | None
    created_date: datetime
    updated_date: datetime


class FeatureFlagCondition(TypedDict):
    context_key: str
    operator: Operator
    value: Any


class FeatureFlag(TypedDict):
    _id: NotRequired[ObjectId]
    name: str
    description: str
    enabled: bool
    conditions: list[list[FeatureFlagCondition]]
    created_date: datetime
    updated_date: datetime


class Project(TypedDict):
    _id: NotRequired[ObjectId]
    name: str
    private_key: str
    context_fields: list[ContextField]
    feature_flags: list[FeatureFlag]
    created_date: datetime
    updated_date: datetime


class UserRole(IntEnum):
    READ_ONLY = 1
    STANDARD = 2
    ADMIN = 3


class UserStatus(IntEnum):
    INVITED = 1
    ACTIVATED = 2


class User(TypedDict):
    _id: NotRequired[ObjectId]
    email: str
    name: str
    role: UserRole
    projects: list[ObjectId]
    password: str | None
    password_token: str | None
    status: UserStatus
    created_date: datetime
    updated_date: datetime
