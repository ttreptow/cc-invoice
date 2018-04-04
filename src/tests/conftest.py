import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.local import LocalProxy

from invoice_service.models.base import BaseModel
from invoice_service.services import LINE_ITEM_SERVICE, INVOICE_SERVICE, FILTER_SERVICE
from invoice_service.services.invoice_service import InvoiceService
from invoice_service.services.item_filter_service import ItemFilterService
from invoice_service.services.line_item_service import LineItemService


@pytest.fixture
def session_maker():
    engine = create_engine("sqlite:///:memory:")
    BaseModel.metadata.create_all(engine)
    return sessionmaker(bind=engine)


@pytest.fixture
def line_item_service(service_factory):
    return service_factory.create_proxy_service(LINE_ITEM_SERVICE)


@pytest.fixture
def invoice_service(service_factory):
    return service_factory.create_proxy_service(INVOICE_SERVICE)


@pytest.fixture
def filter_service(service_factory):
    return service_factory.create_proxy_service(FILTER_SERVICE)


@pytest.fixture
def service_factory(session_maker):
    return DummyServiceFactory(session_maker)


class DummyServiceFactory:
    def __init__(self, session_maker):
        self.session_maker = session_maker
        self.services = {
            INVOICE_SERVICE: InvoiceService(self),
            LINE_ITEM_SERVICE: LineItemService(self),
            FILTER_SERVICE: ItemFilterService(self)
        }

    def create_proxy_service(self, service_name):
        return LocalProxy(lambda: self.services[service_name])
