

def test_session_manager_creation(session_manager):
    assert hasattr(session_manager, 'set_tenant')


def test_session_manager_set_tenant(session_manager):
    tenant = {'name': 'Amazon'}
    session_manager.set_tenant(tenant)
    tenant = session_manager.tenant_provider.tenant
    assert tenant.slug == 'amazon'


def test_session_manager_get_tenant(session_manager):
    tenant = {'name': 'Amazon'}
    session_manager.set_tenant(tenant)
    tenant = session_manager.get_tenant()
    assert tenant['slug'] == 'amazon'


def test_session_manager_set_user(session_manager):
    user = {'name': 'jdacevedo'}
    session_manager.set_user(user)
    assert session_manager.auth_provider.user.name == 'jdacevedo'
