from math import ceil

from sqlalchemy import asc, desc, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from source.app.registrator.enums import Order, Sort
from source.app.registrator.models import RegistratorModel
from source.app.registrator.schemas import (
    RegistratorCreate,
    RegistratorPage,
    RegistratorRequest,
    RegistratorResponse,
    RegistratorUpdate,
    RegistratorUpdateRequest,
)


async def get_registrator(
    registrator_id: int, db: AsyncSession
) -> RegistratorResponse | None:
    if registrator := await db.get(RegistratorModel, registrator_id):
        return RegistratorResponse.model_validate(registrator)
    return None


async def list_registrator(
    page: int, size: int, sort: Sort, order: Order, db: AsyncSession
) -> RegistratorPage:
    order = asc(sort) if order == Order.ASC.value else desc(sort)
    registrators = await db.scalars(
        select(RegistratorModel).order_by(order).offset((page - 1) * size).limit(size)
    )
    total = await db.scalar(select(func.count(RegistratorModel.id)))

    registrator_list = [
        RegistratorResponse.model_validate(registrator)
        for registrator in registrators.all()
    ]
    return RegistratorPage(
        registrator=registrator_list,
        page=page,
        size=size,
        total=total,
        pages=(ceil(total / size) if size else 1),
    )


async def create_registrator(
    registrator: RegistratorRequest, db: AsyncSession
) -> RegistratorResponse | None:
    try:
        registrator = RegistratorModel(
            **RegistratorCreate(**registrator.model_dump()).model_dump()
        )
        db.add(registrator)
        await db.commit()
        await db.refresh(registrator)
        return RegistratorResponse.model_validate(registrator)
    except IntegrityError:
        return None


async def update_registrator(
    registrator: RegistratorModel,
    registrator_update: RegistratorUpdateRequest,
    db: AsyncSession,
) -> RegistratorResponse | None:
    try:
        fields_to_update = (
            RegistratorUpdate(**registrator_update.model_dump()).model_dump().items()
        )
        for key, value in fields_to_update:
            if value is not None:
                setattr(registrator, key, value)
        await db.commit()
        await db.refresh(registrator)
        return RegistratorResponse.model_validate(registrator)
    except IntegrityError:
        return None


async def delete_registrator(registrator_id: int, db: AsyncSession) -> bool:
    if registrator := await db.get(RegistratorModel, registrator_id):
        await db.delete(registrator)
        await db.commit()
        return True
    return False


async def get_db_registrator(
    registrator_id: int, db: AsyncSession
) -> RegistratorModel | None:
    return await db.get(RegistratorModel, registrator_id)
