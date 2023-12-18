debug:
	uvicorn src.main:app --reload
make-migrations:
	alembic revision --autogenerate
migrate:
	alembic upgrade head
downgrade:
	alembic downgrade -1