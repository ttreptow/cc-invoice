import os

import pytest
from flask import json

from invoice_service.app_factory import create_app
from invoice_service.models.line_item import LineItem
from invoice_service.services import LINE_ITEM_SERVICE
from invoice_service.services.service_factory import ServiceFactory


@pytest.fixture
def invoice_app(placement_test_data):
    config = {'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:",
              'SQLALCHEMY_ECHO': True}
    app = create_app(config=config)
    app.testing = True
    with app.test_request_context():
        line_item_service = ServiceFactory.create_proxy_service(LINE_ITEM_SERVICE)
        line_item_service.add_items(placement_test_data)
        return app.test_client()


@pytest.fixture
def placement_test_data():
    path = os.path.join(os.path.dirname(__file__), "data", "placements_teaser_data.json")
    with open(path, "rt") as f:
        data = json.load(f)
    return [LineItem(**item) for item in data]


class TestFullStack:
    def test_get_line_items(self, invoice_app):
        r = invoice_app.get("/lineitems")

        assert r.status_code == 200
        data = json.loads(r.data)
        assert 10000 == len(data)

    def test_get_total(self, invoice_app):
        r = invoice_app.get("/invoices/current/total")

        assert r.status_code == 200
        total = json.loads(r.data)
        assert 4811950011.273662 == total

    def test_get_subtotals(self, invoice_app):
        r = invoice_app.get("/invoices/current/subtotals")

        assert r.status_code == 200
        subtotals = json.loads(r.data)
        assert 419 == len(subtotals)
        for subtot in subtotals.values():
            assert subtot > 0

    def test_adjust_item(self, invoice_app):
        putresp = invoice_app.put("/lineitems/36", data=json.dumps({"adjustments": 0}))
        totalresp = invoice_app.get("/invoices/current/total")

        total = json.loads(totalresp.data)
        assert putresp.status_code == 200
        assert totalresp.status_code == 200
        assert 4811950011.273662 - 35466.90013675345 == total

    def test_set_filter(self, invoice_app):
        initial_total_resp = invoice_app.get("/invoices/current/total")
        filter_data = {"field_name": "campaign_id", "operation": "in", "values": [5, 6, 22]}
        invoice_app.put("/lineitems/filters", data=json.dumps(filter_data))
        getitems_resp = invoice_app.get("/lineitems")
        filtered_total_resp = invoice_app.get("/invoices/current/total")

        initial_total = json.loads(initial_total_resp.data)
        filtered_items = json.loads(getitems_resp.data)
        filtered_total = json.loads(filtered_total_resp.data)

        assert filtered_total < initial_total
        assert len(filtered_items) < 10000  # original data has 10000 items
