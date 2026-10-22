"""Stable, user-readable validation error responses."""

from collections.abc import Mapping, Sequence
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ValidationIssue(BaseModel):
    code: str
    field: str
    message: str
    context: dict[str, Any] | None = None


class ValidationErrorResponse(BaseModel):
    error: str = "validation_failed"
    message: str = "The request contains invalid data."
    issues: list[ValidationIssue]


def validation_issues(errors: Sequence[Mapping[str, Any]]) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for error in errors:
        location = [str(part) for part in error.get("loc", ()) if part not in {"body", "query"}]
        context = error.get("ctx")
        if context:
            context = {
                key: value for key, value in context.items() if not isinstance(value, Exception)
            }
        issues.append(
            ValidationIssue(
                code=str(error.get("type", "invalid_value")),
                field=".".join(location) or "request",
                message=str(error.get("msg", "Invalid value")),
                context=context or None,
            )
        )
    return issues


def install_validation_error_handler(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def request_validation_error_handler(
        _request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        response = ValidationErrorResponse(issues=validation_issues(exc.errors()))
        return JSONResponse(status_code=422, content=response.model_dump(mode="json"))
