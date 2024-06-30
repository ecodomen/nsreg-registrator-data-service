from fastapi import APIRouter, Depends

from source.app.registrator.views import registrator_router
from source.core.auth import api_key_auth

api_router = APIRouter()

api_router.include_router(registrator_router, dependencies=[Depends(api_key_auth)])
