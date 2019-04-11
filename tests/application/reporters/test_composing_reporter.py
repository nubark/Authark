from pytest import fixture, raises
from authark.application.models.user import User
from authark.application.models.credential import Credential
from authark.application.repositories.user_repository import (
    UserRepository, MemoryUserRepository)
from authark.application.repositories.credential_repository import (
    CredentialRepository, MemoryCredentialRepository)
from authark.application.repositories.expression_parser import ExpressionParser
from authark.application.reporters import ComposingReporter


def test_composing_reporter_methods():
    methods = ComposingReporter.__abstractmethods__
    assert 'list_user_roles' in methods


def test_composing_reporter_list_user_roles(composing_reporter):
    user_id = '1'
    result = composing_reporter.list_user_roles(user_id)
    assert isinstance(result, list)
    assert result[0] == {'ranking_id': '1', 'role': 'admin',
                         'dominion': 'Data Server'}


def test_composing_reporter_list_user_roles_(composing_reporter):
    user_id = '1'
    result = composing_reporter.list_user_roles(user_id)
    assert isinstance(result, list)
    assert result[0] == {'ranking_id': '1', 'role': 'admin',
                         'dominion': 'Data Server'}


def test_composing_reporter_list_resource_policies(composing_reporter):
    resource_id = '1'
    result = composing_reporter.list_resource_policies(resource_id)
    assert isinstance(result, list)
    assert result[0] == {'permission_id': '1',
                         'policy': 'Administrators Only',
                         'type': 'role',
                         'value': 'admin'}


def test_composing_reporter_list_role_permissions(composing_reporter):
    role_id = '1'
    result = composing_reporter.list_role_permissions(role_id)
    assert isinstance(result, list)
    assert result[0] == {
        'grant_id': '1', 'permission_id': '1', 'resource': 'products',
        'policy': 'Administrators Only', 'type': 'role', 'value': 'admin'}
