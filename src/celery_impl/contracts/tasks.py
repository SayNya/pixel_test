from src.database import async_session
from src.database.repositories import ContractsRepository, StatusRepository
from src.main import app, loop, versions
from src.services import ContractsService


async def start(versions):
    async with async_session() as session:
        contracts_repository = ContractsRepository(session)
        status_repository = StatusRepository(session)
        contracts_service = ContractsService(versions['ERC20'], contracts_repository, status_repository)
        await contracts_service.handle()


@app.task()
def process_contracts():
    loop.run_until_complete(start(versions))


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        30,
        process_contracts.s(),
    )
