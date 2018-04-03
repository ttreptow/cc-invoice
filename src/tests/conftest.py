from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from invoice_service.app_factory import create_app
from invoice_service.models.base import BaseModel
from invoice_service.services.line_item_service import InvoiceService
from invoice_service.services.service_factory import set_service


@pytest.fixture
def dummy_service():
    return Mock(InvoiceService)


@pytest.fixture(autouse=True)
def invoice_app(dummy_service):
    app = create_app()
    app.testing = True
    with app.test_request_context():
        set_service(dummy_service)
        yield app.test_client()


@pytest.fixture
def session_maker():
    engine = create_engine("sqlite:///:memory:")
    BaseModel.metadata.create_all(engine)
    return sessionmaker(bind=engine)


@pytest.fixture
def invoice_service(session_maker):
    return InvoiceService(session_maker)


