from asyncio import sleep
from pytest import fixture, raises
from authark.application.domain.common import (
    QueryParser, StandardTenantProvider, Tenant)
from authark.application.domain.models import Entity
from authark.application.domain.repositories import (
    Repository, MemoryRepository)


class Alpha(Entity):
    def __init__(self, **attributes) -> None:
        super().__init__(**attributes)
        self.field_1 = attributes.get('field_1', "")


class Beta(Entity):
    def __init__(self, **attributes) -> None:
        super().__init__(**attributes)
        self.alpha_id = attributes.get('alpha_id', "")


def test_memory_repository_implementation() -> None:
    assert issubclass(MemoryRepository, Repository)


@fixture
def memory_repository() -> MemoryRepository[Alpha]:
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(id='001', name="Default"))
    parser = QueryParser()

    class AlphaMemoryRepository(MemoryRepository[Alpha]):
        model = Alpha

    repository = AlphaMemoryRepository(parser, tenant_provider)

    repository.load({"default": {}})
    return repository


@fixture
def alpha_memory_repository() -> MemoryRepository[Alpha]:
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(id='001', name="Default"))
    parser = QueryParser()

    class AlphaMemoryRepository(MemoryRepository[Alpha]):
        model = Alpha

    repository = AlphaMemoryRepository(parser, tenant_provider)
    repository.load({
        "default": {
            "1": Alpha(id='1', field_1='value_1'),
            "2": Alpha(id='2', field_1='value_2'),
            "3": Alpha(id='3', field_1='value_3')
        }
    })
    return repository


@fixture
def beta_memory_repository() -> MemoryRepository[Beta]:
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(id='001', name="Default"))
    parser = QueryParser()

    class BetaMemoryRepository(MemoryRepository[Beta]):
        model = Beta

    repository = BetaMemoryRepository(parser, tenant_provider)
    repository.load({
        "default": {
            "1": Beta(id='1', alpha_id='1'),
            "2": Beta(id='2', alpha_id='1'),
            "3": Beta(id='3', alpha_id='2')
        }
    })
    return repository


def test_memory_repository_model(memory_repository) -> None:
    assert memory_repository.model is Alpha


def test_memory_repository_not_implemented_model(memory_repository) -> None:
    tenant_provider = StandardTenantProvider()
    tenant_provider.setup(Tenant(id='001', name="Default"))
    parser = QueryParser()
    repository = MemoryRepository(parser, tenant_provider)
    with raises(NotImplementedError):
        repository.model


def test_memory_repository_tenant_provider(alpha_memory_repository) -> None:
    assert alpha_memory_repository.tenant_provider is not None


async def test_memory_repository_search_limit(alpha_memory_repository):
    items = await alpha_memory_repository.search([], limit=2)

    assert len(items) == 2


async def test_memory_repository_search_limit_none(alpha_memory_repository):
    items = await alpha_memory_repository.search([], limit=None, offset=None)

    assert len(items) == 3


async def test_memory_repository_search_offset(alpha_memory_repository):
    items = await alpha_memory_repository.search([], offset=2)

    assert len(items) == 1


async def test_memory_repository_add(memory_repository) -> None:
    item = Alpha(id="1", field_1="value_1")

    is_saved = await memory_repository.add(item)

    assert len(memory_repository.data['default']) == 1
    assert is_saved
    assert "1" in memory_repository.data['default'].keys()
    assert item in memory_repository.data['default'].values()


async def test_memory_repository_add_update(memory_repository) -> None:
    created_entity = Alpha(id="1", field_1="value_1")
    created_entity, *_ = await memory_repository.add(created_entity)

    await sleep(1)

    updated_entity = Alpha(id="1", field_1="New Value")
    updated_entity, *_ = await memory_repository.add(updated_entity)

    assert created_entity.created_at == updated_entity.created_at

    items = memory_repository.data['default']
    assert len(items) == 1
    assert "1" in items.keys()
    assert updated_entity in items.values()
    assert "New Value" in items['1'].field_1


async def test_memory_repository_add_no_id(memory_repository) -> None:
    item = Alpha(field_1="value_1")

    is_saved = await memory_repository.add(item)

    items = memory_repository.data['default']
    assert len(items) == 1
    assert is_saved
    assert len(list(items.keys())[0]) > 0
    assert item in items.values()


async def test_memory_repository_add_multiple(memory_repository):
    items = [
        Alpha(field_1="value_1"),
        Alpha(field_1="value_2")
    ]

    returned_items = await memory_repository.add(items)

    items = memory_repository.data['default']
    assert len(returned_items) == 2
    assert returned_items[0].field_1 == 'value_1'
    assert returned_items[1].field_1 == 'value_2'


async def test_memory_repository_search(alpha_memory_repository):
    domain = [('field_1', '=', "value_3")]

    items = await alpha_memory_repository.search(domain)

    assert len(items) == 1
    for item in items:
        assert item.id == '3'
        assert item.field_1 == "value_3"


async def test_memory_repository_search_all(alpha_memory_repository):
    items = await alpha_memory_repository.search([])

    assert len(items) == 3


async def test_memory_repository_search_limit(alpha_memory_repository):
    items = await alpha_memory_repository.search([], limit=2)

    assert len(items) == 2


async def test_memory_repository_search_limit_zero(alpha_memory_repository):
    items = await alpha_memory_repository.search([], limit=0)

    assert len(items) == 0


async def test_memory_repository_search_offset(alpha_memory_repository):
    items = await alpha_memory_repository.search([], offset=2)

    assert len(items) == 1


async def test_memory_repository_search_join_one_to_many(
        alpha_memory_repository, beta_memory_repository):

    for parent, betaren in await alpha_memory_repository.search(
            [('id', '=', '1')], join=beta_memory_repository):

        assert isinstance(parent, Alpha)
        assert all(isinstance(beta, Beta) for beta in betaren)
        assert len(betaren) == 2


async def test_memory_repository_search_join_many_to_one(
        alpha_memory_repository, beta_memory_repository):

    for element, siblings in await beta_memory_repository.search(
            [('id', '=', '1')], join=alpha_memory_repository,
            link=alpha_memory_repository):

        assert isinstance(element, Beta)
        assert len(siblings) == 1
        assert isinstance(next(iter(siblings)), Alpha)


async def test_memory_repository_remove_true(alpha_memory_repository):
    item = alpha_memory_repository.data['default']["2"]
    deleted = await alpha_memory_repository.remove(item)

    items = alpha_memory_repository.data['default']
    assert deleted is True
    assert len(items) == 2
    assert "2" not in items


async def test_memory_repository_remove_false(alpha_memory_repository):
    item = Alpha(**{'id': '6', 'field_1': 'MISSING'})
    deleted = await alpha_memory_repository.remove(item)

    items = alpha_memory_repository.data['default']
    assert deleted is False
    assert len(items) == 3


async def test_memory_repository_remove_idempotent(alpha_memory_repository):
    existing_item = item = alpha_memory_repository.data['default']["2"]
    missing_item = Alpha(**{'id': '6', 'field_1': 'MISSING'})

    items = alpha_memory_repository.data['default']

    deleted = await alpha_memory_repository.remove(
        [existing_item, missing_item])

    assert deleted is True
    assert len(items) == 2

    deleted = await alpha_memory_repository.remove(
        [existing_item, missing_item])

    assert deleted is False
    assert len(items) == 2


async def test_memory_repository_count(alpha_memory_repository):
    count = await alpha_memory_repository.count()

    assert count == 3


async def test_memory_repository_count_domain(alpha_memory_repository):
    domain = [('field_1', '=', "value_3")]
    count = await alpha_memory_repository.count(domain)

    assert count == 1
