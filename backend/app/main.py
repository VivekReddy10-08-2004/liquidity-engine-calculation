"""Application entry point; domain endpoints will be added during MVP development."""

from fastapi import FastAPI

from backend.app.api.errors import install_validation_error_handler
from backend.app.config import Settings

settings = Settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
install_validation_error_handler(app)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Backend is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
