from src.models import InternalModel


class ERC20Contract(InternalModel):
    id: int
    contract_address: str
    source_code: str

    status_id: int


class ERC20ContractUpdate(InternalModel):
    id: int
    is_erc20: bool = False
    erc20_version: str = ''

    status_id: int = 2
