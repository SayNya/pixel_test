import solidity_parser
from loguru import logger

from src.database.repositories import ContractsRepository, StatusRepository
from src.models import ERC20ContractUpdate


class ContractsService:
    ERC20_FUNCTIONS = ('totalSupply', 'balanceOf', 'transfer', 'allowance', 'approve', 'transferFrom')
    ERC20_EVENTS = ('Transfer', 'Approval')

    def __init__(self, versions: dict, contracts_repository: ContractsRepository, status_repository: StatusRepository):
        self.versions = versions

        self.contracts_repository = contracts_repository
        self.status_repository = status_repository

    async def handle(self) -> None:
        unprocessed_status = await self.status_repository.get_by_code('waits_processing')
        processing_status = await self.status_repository.get_by_code('processing')
        processed_status = await self.status_repository.get_by_code('processed')
        failed_status = await self.status_repository.get_by_code('failed')

        unprocessed_contracts = await self.contracts_repository.get_unprocessed(unprocessed_status.id)
        unprocessed_contracts = await self.contracts_repository.update_status_by_ids(
            [contract.id for contract in unprocessed_contracts],
            processing_status.id
        )

        for contract in unprocessed_contracts:
            logger.info(f'Processing {contract.contract_address}')
            contract_model = ERC20ContractUpdate(id=contract.id, status_id=processed_status.id)
            try:
                parsed_contract = solidity_parser.parse(contract.source_code)
            except Exception as e:
                logger.error(f'Error {e} when parsing contract {contract.contract_address}')
                contract_model.status_id = failed_status.id
            else:
                contract_obj = solidity_parser.objectify(parsed_contract).contracts
                if self.is_erc20_contract(contract_obj):
                    contract_model.is_erc20 = True
                    if version := self.check_contract_version(parsed_contract):
                        contract_model.erc20_version = version

            await self.contracts_repository.update_contract_info(contract_model)

    def is_erc20_contract(self, contract: dict) -> bool:
        for ctr in contract.values():
            if self.analyze_contract(ctr):
                return True

        return False

    def analyze_contract(self, contract) -> bool:
        for func_name in self.ERC20_FUNCTIONS:
            if func_name not in contract.functions.keys():
                return False

        # for event_name in self.ERC20_EVENTS:
        #     if event_name not in contract.events.keys():
        #         return False

        return True

    def check_contract_version(self, contract) -> str | None:
        for version, code in self.versions.items():
            if contract['children'] == code:
                return version
