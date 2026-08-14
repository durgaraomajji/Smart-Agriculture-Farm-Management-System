from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.database import Base, engine
from app.routes import (
    auth,
    farms,
    crops,
    irrigation,
    treatments,
    health,
    harvest,
    sales,
    dashboard
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Smart Agriculture & Farm Management System",
    description="Backend API for managing farms, fields, crops, irrigation, treatments, crop health, harvesting and sales",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(farms.router)
app.include_router(crops.router)
app.include_router(irrigation.router)
app.include_router(treatments.router)
app.include_router(health.router)
app.include_router(harvest.router)
app.include_router(sales.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {
        "message": "Smart Agriculture & Farm Management System API is running",
        "docs": "/docs"
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(
    request: Request,
    exc: IntegrityError
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Database integrity constraint violated"
        }
    )