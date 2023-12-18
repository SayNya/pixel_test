from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    db_name: str
    db_username: str
    db_password: str
    db_host: str

    @property
    def db_url(self) -> str:
        return f'postgresql+asyncpg://{self.db_username}:{self.db_password}@{self.db_host}:5432/{self.db_name}'

    celery_broker_url: str

    github_access_token: str
    repositories: dict = {
        'ERC20': {
            'owner': 'OpenZeppelin',
            'rep_name': 'openzeppelin-contracts',
            'contract_path': r'contracts/token/ERC20/ERC20.sol'
        },
    }


settings = Settings()
