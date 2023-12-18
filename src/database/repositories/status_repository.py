from sqlalchemy.ext.asyncio import AsyncSession

from src.database.repositories import BaseRepository
from src.database.tables import StatusesTable
from src.models import Status


class StatusRepository(BaseRepository):
    schema_class = StatusesTable

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_code(self, code: str) -> Status:
        instance = await self._get(key='code', value=code)
        return Status.model_validate(instance)
