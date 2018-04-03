from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from invoice_service.app import app
from invoice_service.app_factory import set_service
from invoice_service.models.base import BaseModel
from invoice_service.service import InvoiceService


@pytest.fixture
def dummy_service():
    return Mock(InvoiceService)


@pytest.fixture(autouse=True)
def invoice_app(dummy_service):
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


