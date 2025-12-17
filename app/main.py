import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.shared.exceptions import AppException
from app.core.error_handler import app_exception_handler

from app.modules.auth.router import router as auth_router
from app.modules.events.router import router as events_router
from app.modules.mail.router import router as mail_router

def create_app() -> FastAPI:
    app = FastAPI(title="Media6 API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(AppException, app_exception_handler)

    app.include_router(auth_router)
    app.include_router(events_router)
    app.include_router(mail_router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=not settings.is_prod,
    )
