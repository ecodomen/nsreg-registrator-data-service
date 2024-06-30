from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from source.app.registrator.schemas import (
    RegistratorId,
    RegistratorPage,
    RegistratorPagination,
    RegistratorRequest,
    RegistratorResponse,
    RegistratorUpdateRequest,
)
from source.app.registrator.services import (
    create_registrator,
    delete_registrator,
    get_registrator,
    get_db_registrator,
    list_registrator,
    update_registrator,
)
from source.core.database import get_db
from source.core.schemas import ExceptionSchema

registrator_router = APIRouter(prefix="/registrator")


@registrator_router.post(
    "/",
    response_model=RegistratorResponse,
    responses={
        status.HTTP_409_CONFLICT: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_201_CREATED,
    tags=["registrator"],
)
async def registrator_create(
    registrator: RegistratorRequest, db: AsyncSession = Depends(get_db)
) -> RegistratorResponse:
    if created_registrator := await create_registrator(registrator=registrator, db=db):
        return created_registrator
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Регистратор '{registrator.name}' уже существует",
    )


@registrator_router.get(
    "/",
    response_model=RegistratorPage,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema}},
    tags=["registrator"],
)
async def registrator_list(
    pagination: RegistratorPagination = Depends(),
    db: AsyncSession = Depends(get_db),
) -> RegistratorPage:
    return await list_registrator(
        page=pagination.page,
        size=pagination.size,
        sort=pagination.sort,
        order=pagination.order,
        db=db,
    )


@registrator_router.get(
    "/{registrator_id}",
    response_model=RegistratorResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
    },
    tags=["registrator"],
)
async def registrator_get(
    request: RegistratorId = Depends(),
    db: AsyncSession = Depends(get_db),
) -> RegistratorResponse:
    if registrator := await get_registrator(
        registrator_id=request.registrator_id, db=db
    ):
        return registrator
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Регистратор '{request.registrator_id}' не найден",
    )


@registrator_router.patch(
    "/{registrator_id}",
    response_model=RegistratorResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_409_CONFLICT: {"model": ExceptionSchema},
    },
    tags=["registrator"],
)
async def registrator_update(
    payload: RegistratorUpdateRequest,
    request: RegistratorId = Depends(),
    db: AsyncSession = Depends(get_db),
) -> RegistratorResponse:
    if registrator := await get_db_registrator(
        registrator_id=request.registrator_id, db=db
    ):
        if updated_registrator := await update_registrator(
            registrator=registrator, registrator_update=payload, db=db
        ):
            return updated_registrator
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Регистратор '{payload.name}' уже существует",
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Регистратор '{request.registrator_id}' не найден",
    )


@registrator_router.delete(
    "/{registrator_id}",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["registrator"],
)
async def registrator_delete(
    request: RegistratorId = Depends(),
    db: AsyncSession = Depends(get_db),
) -> None:
    if not await delete_registrator(registrator_id=request.registrator_id, db=db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Регистратор '{request.registrator_id}' не найден",
        )
