from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.api.v1 import content_routes, auth_routes
from app.api import health_check

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for Educated Guess Media Platform",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Event handlers
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    await connect_to_mongo()
    print(f"🚀 {settings.app_name} v{settings.app_version} started")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    await close_mongo_connection()


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "docs": "/api/docs"
    }


# Include routers
app.include_router(health_check.router, prefix="/api")
app.include_router(auth_routes.router, prefix=f"{settings.api_v1_prefix}/auth")
app.include_router(content_routes.router, prefix=settings.api_v1_prefix)
