from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core import settings

engine = create_async_engine(
    settings.db_url,
    echo=True,
)

async_session = async_sessionmaker(engine, expire_on_commit=False)
