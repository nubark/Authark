from injectark import FactoryBuilder
from .base_factory import BaseFactory
from .check_factory import CheckFactory
from .crypto_factory import CryptoFactory
from .json_factory import JsonFactory
from .web_factory import WebFactory


factory_builder = FactoryBuilder([
    BaseFactory, CheckFactory,
    CryptoFactory, JsonFactory, WebFactory])
