from pathlib import Path
from .development_config import DevelopmentConfig


class ProductionConfig(DevelopmentConfig):
    def __init__(self):
        super().__init__()
        self['mode'] = 'PROD'
        self['gunicorn'].update({
            'debug': True,
            'accesslog': '-',
            'loglevel': 'debug'
        })
        self['tenancy'] = {
            'type': 'json',
            'url': Path.home() / 'tenants_catalog.json'
        }
        self['data'] = {
            'type': 'json',
            'dir': Path.home() / 'data'
        }
        self['database'] = {
            'type': 'json',
            'url': './authark_data.json'
        }
        self['factory'] = 'JsonFactory'
        self['strategy'].update({
            "UserRepository": {
                "method": "json_user_repository"
            },
            "CredentialRepository": {
                "method": "json_credential_repository"
            },
            "DominionRepository": {
                "method": "json_dominion_repository"
            },
            "RoleRepository": {
                "method": "json_role_repository"
            },
            "RankingRepository": {
                "method": "json_ranking_repository"
            },
            "PolicyRepository": {
                "method": "json_policy_repository"
            },
            "ResourceRepository": {
                "method": "json_resource_repository"
            },
            "GrantRepository": {
                "method": "json_grant_repository"
            },
            "PermissionRepository": {
                "method": "json_permission_repository"
            },
            "HashService": {
                "method": "passlib_hash_service"
            },
            "AccessTokenService": {
                "method": "pyjwt_access_token_service"
            },
            "RefreshTokenService": {
                "method": "pyjwt_refresh_token_service"
            },
            "ImportService": {
                "method": "json_import_service"
            },
            "CatalogService": {
                "method": "json_catalog_service"
            },
        })
