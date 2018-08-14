from typing import Dict
from pytest import fixture
from inspect import signature
from authark.application.models.user import User
from authark.application.repositories.user_repository import UserRepository
from authark.application.repositories.user_repository import (
    MemoryUserRepository)


def test_user_repository_methods() -> None:
    methods = UserRepository.__abstractmethods__
    assert 'get' in methods
    assert 'save_' in methods
    assert 'search' in methods

    sig = signature(UserRepository.save)
    assert sig.parameters.get('user')


def test_memory_user_repository_implementation() -> None:
    assert issubclass(MemoryUserRepository, UserRepository)


@fixture
def user_dict() -> Dict[str, User]:
    user_dict = {
        "1": User('1', 'valenep', 'valenep@gmail.com', "PASS1"),
        "2": User('2', 'tebanep', 'tebanep@gmail.com', "PASS2"),
        "3": User('3', 'gabeche', 'gabeche@gmail.com', "PASS3")
    }
    return user_dict


def test_memory_user_repository_load_user(user_dict: Dict[str, User]) -> None:
    memory_user_repository = MemoryUserRepository()

    memory_user_repository.load(user_dict)

    assert memory_user_repository.user_dict == user_dict


def test_memory_user_repository_get_user(user_dict: Dict[str, User]) -> None:
    memory_user_repository = MemoryUserRepository()

    memory_user_repository.load(user_dict)
    user = memory_user_repository.get("1")

    assert user and user.username == "valenep"
    assert user and user.email == "valenep@gmail.com"


def test_memory_user_repository_save_user() -> None:
    memory_user_repository = MemoryUserRepository()

    user = User("4", "mvp", "mvp@gmail.com", "QWERTY")

    is_saved = memory_user_repository.save(user)

    assert len(memory_user_repository.user_dict) == 1
    assert is_saved
    assert "4" in memory_user_repository.user_dict.keys()
    assert user in memory_user_repository.user_dict.values()


def test_memory_user_repository_save_user_duplicate() -> None:
    memory_user_repository = MemoryUserRepository()

    user = User("4", "mvp", "mvp@gmail.com", "QWERTY")

    is_saved = memory_user_repository.save(user)
    assert is_saved
    is_saved = memory_user_repository.save(user)
    assert not is_saved
    assert len(memory_user_repository.user_dict) == 1


def test_memory_user_repository_search_all(user_dict):
    memory_user_repository = MemoryUserRepository()
    memory_user_repository.load(user_dict)

    users = memory_user_repository.search([])

    assert len(users) == 3


def test_memory_user_repository_search_limit(user_dict):
    memory_user_repository = MemoryUserRepository()
    memory_user_repository.load(user_dict)

    users = memory_user_repository.search([], limit=2)

    assert len(users) == 2


def test_memory_user_repository_search_offset(user_dict):
    memory_user_repository = MemoryUserRepository()
    memory_user_repository.load(user_dict)

    users = memory_user_repository.search([], offset=2)

    assert len(users) == 1
