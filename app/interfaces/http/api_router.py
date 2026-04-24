from fastapi import APIRouter

from app.interfaces.http.greeting_controller import router as greeting_router
from app.interfaces.http.line_scan_controller import router as line_scan_router


api_router = APIRouter()
api_router.include_router(greeting_router)
api_router.include_router(line_scan_router)
