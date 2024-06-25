from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from backend.core.middleware import AuthMiddleware
from backend.endpoints.routers import calories_router, user_router, stats_router
from backend.metrics import prometheus_metrics, metrics


def setup_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.add_middleware(AuthMiddleware)
    app.middleware('http')(prometheus_metrics)


def setup_routers(app: FastAPI) -> None:
    app.include_router(calories_router)
    app.include_router(stats_router)
    app.include_router(user_router)
    app.add_route('/metrics', metrics)


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger')
    setup_routers(app)

    setup_middleware(app)

    return app


if __name__ == '__main__':
    uvicorn.run('main:create_app', host='0.0.0.0', port=8000, factory=True, reload=True)
