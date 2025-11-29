from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "educated-guess-api"
    }


@router.get("/readiness", tags=["Health"])
async def readiness_check():
    """Readiness probe for Kubernetes"""
    # Add database connectivity check here if needed
    return {
        "status": "ready"
    }


@router.get("/liveness", tags=["Health"])
async def liveness_check():
    """Liveness probe for Kubernetes"""
    return {
        "status": "alive"
    }
