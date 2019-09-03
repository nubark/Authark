import contextlib
from pytest import raises
from unittest.mock import Mock, call
from authark.infrastructure.cli import cli as cli_module
from authark.infrastructure.cli import Cli
from io import StringIO


def test_cli_instantiation(cli):
    assert cli is not None


def test_cli_run(cli):
    mock_parse = Mock()
    cli.parse = mock_parse
    argv = []
    cli.run(argv)

    assert mock_parse.call_count == 1


def test_cli_parse(cli):
    called = False
    argv = ['serve']
    result = cli.parse(argv)

    assert result is not None


def test_cli_parse_empty_argv(cli):
    with raises(SystemExit) as e:
        result = cli.parse([])


def test_cli_setup(cli, namespace):
    cli.setup(namespace)


def test_cli_provision(cli, monkeypatch, namespace):
    namespace.name = "custom"
    cli.provision(namespace)
    tenants = cli.resolver["TenantSupplier"].search_tenants("")

    assert len(tenants) == 1
    assert tenants[0]["name"] == "custom"

    print("TENANTS::::", tenants)


def test_cli_serve(cli, monkeypatch, namespace):
    called = False

    class MockServerApplication:
        def __init__(self, app, options):
            pass

        def run(self):
            nonlocal called
            called = True

    create_app_called = False

    def mock_create_app_function(config, resolver):
        nonlocal create_app_called
        create_app_called = True

    monkeypatch.setattr(
        cli_module, 'ServerApplication', MockServerApplication)
    monkeypatch.setattr(
        cli_module, 'create_app', mock_create_app_function)

    cli.serve(namespace)

    assert called and create_app_called


def test_cli_terminal(cli, monkeypatch, namespace):
    called = False

    class MockTerminalMain:
        def __init__(self, context):
            pass

        def run(self):
            nonlocal called
            called = True

    monkeypatch.setattr(cli_module, 'Main', MockTerminalMain)

    cli.terminal(namespace)

    assert called


def test_cli_load(cli, monkeypatch, namespace):
    namespace.input_file = ""
    namespace.source = ""
    namespace.password_field = ""
    namespace.tenant = "servagro"
    namespace.name = "servagro"

    cli.provision(namespace)

    temp_stdout = StringIO()
    with contextlib.redirect_stdout(temp_stdout):
        cli.load(namespace)

    output = temp_stdout.getvalue().strip()
    assert output == '::::::LOAD:::::'

    # With source and password
    namespace.source = "source"
    namespace.password_field = "my_password"
    temp_stdout = StringIO()
    with contextlib.redirect_stdout(temp_stdout):
        cli.load(namespace)

    output = temp_stdout.getvalue().strip()
    assert output == '::::::LOAD:::::'


def test_cli_load_no_tentant_setted(cli, monkeypatch, namespace):
    namespace.input_file = ""
    namespace.source = ""
    namespace.password_field = ""
    namespace.tenant = ""

    temp_stdout = StringIO()
    with contextlib.redirect_stdout(temp_stdout):
        cli.load(namespace)

    output = temp_stdout.getvalue().strip()
    assert output == '::::::LOAD::::: \nA tenant is required.'