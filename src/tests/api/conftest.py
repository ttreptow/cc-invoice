from unittest.mock import Mock

import pytest

from invoice_service.app_factory import create_app
from invoice_service.services import LINE_ITEM_SERVICE, INVOICE_SERVICE
from invoice_service.services.invoice_service import InvoiceService
from invoice_service.services.line_item_service import LineItemService
from invoice_service.services.service_factory import ServiceFactory


@pytest.fixture
def dummy_line_item_service():
    return Mock(LineItemService)


@pytest.fixture
def dummy_invoice_service():
    return Mock(InvoiceService)


@pytest.fixture
def mock_service_factory_builder(dummy_line_item_service, dummy_invoice_service):
    def build(app):
        serv_fact = ServiceFactory(app)
        serv_fact.register_service(LINE_ITEM_SERVICE, lambda sf: dummy_line_item_service)
        serv_fact.register_service(INVOICE_SERVICE, lambda sf: dummy_invoice_service)
        return serv_fact
    return build


@pytest.fixture(autouse=True)
def dummy_invoice_app(mock_service_factory_builder):
    config = {'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:"}
    app = create_app(config=config, service_factory_builder=mock_service_factory_builder)
    app.testing = True
    with app.test_request_context():
        yield app


@pytest.fixture
def app_client(dummy_invoice_app):
    return dummy_invoice_app.test_client()
