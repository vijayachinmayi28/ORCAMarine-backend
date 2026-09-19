from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="ORCAMarine - AI Marine Safety Assistant backend",
)

origins = settings.allowed_origins_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["system"])
async def root():
    return {
        "project": settings.app_name,
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }
