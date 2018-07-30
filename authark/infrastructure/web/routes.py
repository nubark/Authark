from flask import Flask
from flask_restful import Api
from authark.application.coordinators.auth_coordinator import AuthCoordinator
from authark.application.repositories.user_repository import (
    MemoryUserRepository)
from authark.infrastructure.web.resources.auth_resource import AuthResource
from authark.infrastructure.web.resources.register_resource import (
    RegisterResource)
from authark.infrastructure.crypto.pyjwt_token_service import PyJWTTokenService
from authark.infrastructure.config.registry import Registry


def set_routes(app: Flask, registry: Registry) -> None:

    @app.route('/')
    def index() -> str:
        return "Welcome to Authark!"

    # Restful API
    api = Api(app)

    # Services
    auth_coordinator = registry['auth_coordinator']

    # Auth resource
    api.add_resource(
        AuthResource,
        '/auth', '/login', '/token',
        resource_class_kwargs={
            'auth_coordinator': auth_coordinator
        })

    # Register resource
    api.add_resource(
        RegisterResource,
        '/register', '/signup',
        resource_class_kwargs={
            'auth_coordinator': auth_coordinator
        })