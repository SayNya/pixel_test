import asyncio

from src.core import settings
from src.services import VersionService
from src.celery_impl import create_celery

TASKS = ('src.celery_impl.contracts',)

vs = VersionService(settings.github_access_token, settings.repositories)
versions = vs.get_standards_versions()

loop = asyncio.get_event_loop()
app = create_celery(tasks=TASKS)
