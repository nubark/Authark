from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from authark.application.utilities.type_definitions import QueryDomain
from authark.application.models.user import User
from authark.application.repositories.expression_parser import ExpressionParser


class UserRepository(ABC):
    @abstractmethod
    def get(self, id: str) -> User:
        "Get method to be implemented."

    def save(self, user: User) -> bool:
        existing_user = self.get(user.id)
        if existing_user and existing_user.id:
            return False

        return self.save_(user)

    @abstractmethod
    def save_(self, user: User) -> bool:
        "Internal save method to be implemented."

    @abstractmethod
    def search(self, domain: QueryDomain,
               limit: int, offset: int) -> List[User]:
        "Search users matching a query domain"

    @abstractmethod
    def delete(self, user: User) -> bool:
        "Delete method to be implemented."


class MemoryUserRepository(UserRepository):
    def __init__(self, parser: ExpressionParser) -> None:
        self.user_dict = {}  # type: Dict[str, User]
        self.parser = parser

    def get(self, id: str) -> Optional[User]:
        user = self.user_dict.get(id)
        return user

    def save_(self, user: User) -> bool:
        id = user.id
        self.user_dict[id] = user
        return True

    def search(self, domain: QueryDomain, limit=100, offset=0) -> List[User]:
        users = []
        filter_function = self.parser.parse(domain)
        for user in list(self.user_dict.values()):
            if filter_function(user):
                users.append(user)

        if limit:
            users = users[:limit]
        if offset:
            users = users[offset:]
        return users

    def delete(self, user: User) -> bool:
        if user.id not in self.user_dict:
            return False
        del self.user_dict[user.id]
        return True

    def load(self, user_dict: Dict[str, User]) -> None:
        self.user_dict = user_dict
