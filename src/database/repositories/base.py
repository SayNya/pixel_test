from typing import Any, AsyncGenerator, Generic, Type

from sqlalchemy import Result, asc, delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.tables import ConcreteTable
from src.errors import (
    DatabaseError,
    NotFoundError,
    UnprocessableError,
)

__all__ = ("BaseRepository",)


class BaseRepository(Generic[ConcreteTable]):
    schema_class: Type[ConcreteTable]

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()

        self._session = session
        if not self.schema_class:
            raise UnprocessableError(
                message=(
                    "Can not initiate the class without schema_class attribute"
                )
            )

    async def _update(
            self, key: str, value: Any, payload: dict[str, Any]
    ) -> ConcreteTable:

        query = (
            update(self.schema_class)
            .where(getattr(self.schema_class, key) == value)
            .values(payload)
            .returning(self.schema_class)
        )
        result: Result = await self._session.execute(query)
        await self._session.flush()

        if not (schema := result.scalar_one_or_none()):
            raise DatabaseError

        return schema

    async def _get(self, key: str, value: Any) -> ConcreteTable:

        query = select(self.schema_class).where(
            getattr(self.schema_class, key) == value
        )
        result: Result = await self._session.execute(query)

        if not (_result := result.scalars().one_or_none()):
            raise NotFoundError

        return _result

    async def count(self) -> int:
        result: Result = await self._session.execute(func.count(self.schema_class.id))
        value = result.scalar()

        if not isinstance(value, int):
            raise UnprocessableError(
                message=(
                    "For some reason count function returned not an integer."
                    f"Value: {value}"
                ),
            )

        return value

    async def _first(self, by: str = "id") -> ConcreteTable:
        result: Result = await self._session.execute(
            select(self.schema_class).order_by(asc(by)).limit(1)
        )

        if not (_result := result.scalar_one_or_none()):
            raise NotFoundError

        return _result

    async def _last(self, by: str = "id") -> ConcreteTable:
        result: Result = await self._session.execute(
            select(self.schema_class).order_by(desc(by)).limit(1)
        )

        if not (_result := result.scalar_one_or_none()):
            raise NotFoundError

        return _result

    async def _save(self, payload: dict[str, Any]) -> ConcreteTable:
        try:
            schema = self.schema_class(**payload)
            self._session.add(schema)
            await self._session.flush()
            await self._session.refresh(schema)
            return schema
        except Exception:
            raise DatabaseError

    async def _all(self) -> AsyncGenerator[ConcreteTable, None]:
        result: Result = await self._session.execute(select(self.schema_class))
        schemas = result.scalars().all()

        for schema in schemas:
            yield schema

    async def delete(self, id_: int) -> None:
        await self._session.execute(
            delete(self.schema_class).where(self.schema_class.id == id_)
        )
        await self._session.flush()
