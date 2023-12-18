from typing import Annotated, TypeVar

from sqlalchemy import ForeignKey, MetaData, String, Boolean
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped, relationship

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

int_pk = Annotated[int, mapped_column(primary_key=True)]


class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata


ConcreteTable = TypeVar("ConcreteTable", bound=Base)


class StatusesTable(Base):
    __tablename__ = 'statuses'

    id: Mapped[int_pk]

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(255), nullable=False)

    erc20_contracts: Mapped[list['ERC20ContractsTable']] = relationship(back_populates='status')


class ERC20ContractsTable(Base):
    __tablename__ = 'erc20_contracts'

    id: Mapped[int_pk]

    contract_address: Mapped[str] = mapped_column(String(42), nullable=False)
    source_code: Mapped[str] = mapped_column(String, nullable=False)

    is_erc20: Mapped[bool] = mapped_column(Boolean, nullable=True)
    erc20_version: Mapped[str] = mapped_column(String(255), nullable=True)

    status_id: Mapped[int] = mapped_column(ForeignKey('statuses.id'))
    status: Mapped['StatusesTable'] = relationship(back_populates='erc20_contracts')
