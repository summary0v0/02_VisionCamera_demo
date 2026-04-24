from fastapi import FastAPI

from app.interfaces.http.api_router import api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI DDD Demo",
        description="A minimal FastAPI project with a DDD-style structure.",
        version="0.1.0",
    )
    app.include_router(api_router)
    return app
