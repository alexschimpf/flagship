from pydantic import BaseModel


class ErrorModel(BaseModel):
    code: str
    message: str
    field: str | None


class ErrorResponseModel(BaseModel):
    errors: list[ErrorModel]


class SuccessResponse(BaseModel):
    success: bool
