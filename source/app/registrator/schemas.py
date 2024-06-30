from datetime import datetime

from pydantic import BaseModel, Field

from source.app.registrator.enums import Order, Sort
from source.core.schemas import PageSchema, ResponseSchema


class RegistratorRequest(BaseModel):
    name: str
    nic_handle1: str | None = None
    nic_handle2: str | None = None
    website: str | None = None
    city: str | None = None


class RegistratorCreate(RegistratorRequest):
    pass


class RegistratorResponse(ResponseSchema):
    name: str
    nic_handle1: str | None = None
    nic_handle2: str | None = None
    website: str | None = None
    city: str | None = None
    create_date: datetime
    update_date: datetime


class RegistratorUpdateRequest(BaseModel):
    name: str
    nic_handle1: str | None = None
    nic_handle2: str | None = None
    website: str | None = None
    city: str | None = None


class RegistratorUpdate(RegistratorUpdateRequest):
    pass


class RegistratorPage(PageSchema):
    registrator: list[RegistratorResponse]


class RegistratorPagination(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=50, ge=0)
    sort: Sort = Sort.ID
    order: Order = Order.ASC


class RegistratorId(BaseModel):
    registrator_id: int
