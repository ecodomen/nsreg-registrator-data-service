from sqlalchemy import Column, String, VARCHAR

from source.core.models import Model


class RegistratorModel(Model):
    __tablename__ = "registrator"

    name = Column(name="name", type_=String(255), index=True, unique=True)
    nic_handle1 = Column(name="nic_handle1", type_=String(255), nullable=True)
    nic_handle2 = Column(name="nic_handle2", type_=String(255), nullable=True)
    website = Column(name="website", type_=String(255), nullable=True)
    city = Column(name="city", type_=String(255), nullable=True)
