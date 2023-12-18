from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repositories import BaseRepository
from src.database.tables import ERC20ContractsTable
from src.models import ERC20Contract, ERC20ContractUpdate


class ContractsRepository(BaseRepository):
    schema_class = ERC20ContractsTable

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_unprocessed(self, unprocessed_status_id: int) -> list[ERC20Contract] | None:
        stmt = select(self.schema_class).where(self.schema_class.status_id == unprocessed_status_id)
        result = await self._session.scalars(stmt)

        return [ERC20Contract.model_validate(instance) for instance in result.all()]

    async def update_status_by_ids(self, contract_ids: Sequence[int], status_id: int) -> list[ERC20Contract]:
        stmt = (
            update(self.schema_class)
            .where(self.schema_class.id.in_(contract_ids))
            .values(status_id=status_id)
            .returning(self.schema_class)
        )
        result = await self._session.execute(stmt)
        await self._session.commit()
        await self._session.flush()
        return [ERC20Contract.model_validate(instance) for instance in result.scalars().all()]

    async def update_contract_info(self, payload: ERC20ContractUpdate) -> None:
        await self._update('id', payload.id, payload.model_dump())
        await self._session.commit()
