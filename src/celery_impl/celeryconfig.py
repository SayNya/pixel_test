from src.core import settings

broker_url = settings.celery_broker_url

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Minsk'
enable_utc = True
