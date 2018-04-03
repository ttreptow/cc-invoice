from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from invoice_service.app_factory import create_app
from invoice_service.models.base import BaseModel
from invoice_service.services import LINE_ITEM_SERVICE
from invoice_service.services.line_item_service import LineItemService
from invoice_service.services.service_factory import ServiceFactory


@pytest.fixture
def dummy_line_item_service():
    return Mock(LineItemService)





@pytest.fixture
def mock_service_factory_builder(dummy_line_item_service):
    def build(app):
        serv_fact = ServiceFactory(app)
        serv_fact.register_service(LINE_ITEM_SERVICE, lambda sf: dummy_line_item_service)
        return serv_fact
    return build


@pytest.fixture(autouse=True)
def invoice_app(mock_service_factory_builder):
    config = {'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:"}
    app = create_app(config=config, service_factory_builder=mock_service_factory_builder)
    app.testing = True
    with app.test_request_context():
        yield app


@pytest.fixture
def app_client(invoice_app):
    return invoice_app.test_client()


@pytest.fixture
def session_maker():
    engine = create_engine("sqlite:///:memory:")
    BaseModel.metadata.create_all(engine)
    return sessionmaker(bind=engine)


@pytest.fixture
def line_item_service(session_maker):
    return LineItemService(DummyServiceFactory(session_maker))


class DummyServiceFactory:
    def __init__(self, session_maker):
        self.session_maker = session_maker
