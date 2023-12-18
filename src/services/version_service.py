import solidity_parser
from github import Github, UnknownObjectException
from loguru import logger

from src.utils import hash_dict


class VersionService:
    def __init__(self, access_token: str, repositories: dict[dict]):
        self.github = Github(access_token)
        self.repositories = repositories

    def get_standards_versions(self):
        contracts_versions = {}
        for std_name, rep_data in self.repositories.items():
            versions = {}
            version_hashes = set()
            rep = self.github.get_repo(f'{rep_data["owner"]}/{rep_data["rep_name"]}')
            tags = rep.get_tags()
            for tag in tags:
                try:
                    contract = rep.get_contents(path=rep_data['contract_path'], ref=tag.name)
                except UnknownObjectException:
                    logger.info(f'ERC20.sol file not found in {tag.name}')
                    continue

                contract_str = contract.decoded_content.decode('utf-8')
                parsed_contract = solidity_parser.parse(contract_str)['children']

                contract_hash = hash_dict(parsed_contract)
                if contract_hash in version_hashes:
                    logger.info(f'Implementation version {tag.name} has already been met')
                    continue

                version_hashes.add(contract_hash)

                versions[tag.name] = parsed_contract

            contracts_versions[std_name] = versions

        return contracts_versions
