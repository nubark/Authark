from .....application.domain.common import TenantProvider, QueryParser
from .....application.domain.models import (
    Credential, Dominion, Ranking, Role, User)
from .....application.domain.repositories import (
    CredentialRepository, DominionRepository, RankingRepository,
    RoleRepository, UserRepository)
from .json_repository import JsonRepository


class JsonCredentialRepository(JsonRepository, CredentialRepository):
    """Json Credential Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection_name: str = 'credentials') -> None:
        super().__init__(data_path, parser, tenant_provider,
                         collection_name, Credential)


class JsonDominionRepository(JsonRepository, DominionRepository):
    """Json Dominion Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection_name: str = 'dominions') -> None:
        super().__init__(data_path, parser, tenant_provider,
                         collection_name, Dominion)


class JsonRankingRepository(JsonRepository, RankingRepository):
    """Json Ranking Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection_name: str = 'rankings') -> None:
        super().__init__(data_path, parser, tenant_provider,
                         collection_name, Ranking)


class JsonRoleRepository(JsonRepository, RoleRepository):
    """Json Role Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection_name: str = 'roles') -> None:
        super().__init__(data_path, parser, tenant_provider,
                         collection_name, Role)


class JsonUserRepository(JsonRepository, UserRepository):
    """Json User Repository"""

    def __init__(self, data_path: str, parser: QueryParser,
                 tenant_provider: TenantProvider,
                 collection_name: str = 'users') -> None:
        super().__init__(data_path, parser, tenant_provider,
                         collection_name, User)
