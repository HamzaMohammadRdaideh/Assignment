import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.api.v1.routers import api_router
from fastapi.openapi.utils import get_openapi

from core.database.connection import close_mongo_connection, connect_to_mongo
from core.middlewares.catch_exceptions import ExceptionMiddleWare

app = FastAPI(title="Assignment", docs_url="/assignment/docs",
              openapi_url="/users/openapi.json")

app.include_router(api_router)
app.add_middleware(ExceptionMiddleWare)


@app.on_event("startup")
def startup_event():
    connect_to_mongo()


@app.on_event("shutdown")
def shutdown_event():
    close_mongo_connection()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Assignment",
        version="1.0.0",
        description="The documentation for Assignment service",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(app)
