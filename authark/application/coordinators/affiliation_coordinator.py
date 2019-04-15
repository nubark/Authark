from typing import Dict, Any
from ..services import TenantService, CatalogService, Tenant
from .types import DominionDict, RoleDict


class AffiliationCoordinator:

    def __init__(self, catalog_service: CatalogService,
                 tenant_service: TenantService) -> None:
        self.catalog_service = catalog_service
        self.tenant_service = tenant_service

    def establish_tenant(self, tenant_id: str) -> None:
        tenant = self.catalog_service.get_tenant(tenant_id)
        self.tenant_service.setup(tenant)

    def get_current_tenant(self) -> Dict[str, Any]:
        current = self.tenant_service.get_tenant()
        return vars(current)
