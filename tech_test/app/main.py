from fastapi import FastAPI

from .routes import api_router


def app_factory() -> FastAPI:
    app = FastAPI(title="app")
    app.include_router(api_router)
    return app


app = app_factory()
