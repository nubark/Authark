from pytest import fixture
from authark.application.domain.models import (
    User, Credential, Dominion, Role, Ranking,
    Restriction, Policy)
from authark.application.domain.common import (
    QueryParser, Tenant, StandardTenantProvider)
from authark.application.domain.repositories import (
    UserRepository, MemoryUserRepository,
    CredentialRepository, MemoryCredentialRepository,
    DominionRepository, MemoryDominionRepository,
    RoleRepository, MemoryRoleRepository,
    RankingRepository, MemoryRankingRepository,
    RestrictionRepository, MemoryRestrictionRepository,
    PolicyRepository, MemoryPolicyRepository)
from authark.application.informers import (
    AutharkInformer, StandardAutharkInformer,
    ComposingInformer, StandardComposingInformer)


@fixture
def parser():
    return QueryParser()


@fixture
def tenant_provider():
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(name="Default"))
    return tenant_provider


@fixture
def user_repository(tenant_provider, parser) -> UserRepository:
    user_repository = MemoryUserRepository(parser, tenant_provider)
    user_repository.load({
        "default": {
            "valenep": User(id='1', username='valenep',
                            email='valenep@gmail.com'),
            "tebanep": User(id='2', username='tebanep',
                            email='tebanep@gmail.com'),
            "gabeche": User(id='3', username='gabeche',
                            email='gabeche@gmail.com')
        }
    })
    return user_repository


@fixture
def credential_repository(tenant_provider, parser) -> CredentialRepository:
    credential_repository = MemoryCredentialRepository(parser, tenant_provider)
    credential_repository.load({
        "default": {
            "1": Credential(id='1', user_id='1', value="PASS1"),
            "2": Credential(id='2', user_id='2', value="PASS2"),
            "3": Credential(id='3', user_id='3', value="PASS3"),
        }
    })
    return credential_repository


@fixture
def dominion_repository(tenant_provider, parser) -> DominionRepository:
    dominion_repository = MemoryDominionRepository(parser, tenant_provider)
    dominion_repository.load({
        "default": {
            "1": Dominion(id='1', name='Data Server')
        }
    })
    return dominion_repository


@fixture
def role_repository(tenant_provider, parser) -> RoleRepository:
    role_repository = MemoryRoleRepository(parser, tenant_provider)
    role_repository.load({
        "default": {
            "1": Role(id='1', name='admin', dominion_id='1',
                      description="Service's Administrator")
        }
    })
    return role_repository


@fixture
def restriction_repository(tenant_provider, parser) -> RestrictionRepository:
    restriction_repository = MemoryRestrictionRepository(
        parser, tenant_provider)
    restriction_repository.load({
        "default": {
            "1": Restriction(id='1', group='group name', name='group name',
                             sequence="1", target='target name',
                             domain="domain name")
        }
    })
    return restriction_repository


@fixture
def policy_repository(tenant_provider, parser) -> PolicyRepository:
    policy_repository = MemoryPolicyRepository(parser, tenant_provider)
    policy_repository.load({
        "default": {
            "1": Policy(id='1', resource='resource name',
                        privilege='privilege name',
                        role="role name", restriction='restriction name')
        }
    })
    return policy_repository


@fixture
def ranking_repository(tenant_provider, parser) -> RankingRepository:
    ranking_repository = MemoryRankingRepository(parser, tenant_provider)
    ranking_repository.load({
        "default": {
            "1": Ranking(id='1', user_id='1', role_id='1',
                         description="Service's Administrator")
        }
    })
    return ranking_repository


@fixture
def authark_informer(user_repository: UserRepository,
                     credential_repository: CredentialRepository,
                     dominion_repository: DominionRepository,
                     role_repository: RoleRepository,
                     restriction_repository: RestrictionRepository,
                     policy_repository: PolicyRepository,
                     ranking_repository: RankingRepository

                     ) -> AutharkInformer:
    return StandardAutharkInformer(
        user_repository,
        credential_repository,
        dominion_repository,
        role_repository,
        restriction_repository,
        policy_repository,
        ranking_repository)


@fixture
def composing_informer(dominion_repository: DominionRepository,
                       role_repository: RoleRepository,
                       ranking_repository: RankingRepository
                       ) -> ComposingInformer:
    return StandardComposingInformer(
        dominion_repository,
        role_repository,
        ranking_repository)
