import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi


from celery.result import AsyncResult

from db_utils import models, schemas
from db_utils.database import engine

from routers import studies, admin, data

models.Base.metadata.create_all(bind=engine)  # create all tables

app = FastAPI()

# add routers
app.include_router(studies.router)
app.include_router(admin.router)
app.include_router(data.router)

# specify CORS valid origins
origins = [
# fixme: add origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# custom openapi spec text


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="RESPIRE",
        description="Lung disease data portal API specification",
        version='0.0.1',
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

@app.get('/', status_code=200)
def root():
    return {'status': 'healthy'}

# exception handling -- log 422 results to console


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    logging.error(f"{request}: {exc_str}")
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
