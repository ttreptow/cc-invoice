from flask import json

from invoice_service.service import ItemNotFound, ReadOnlyItemValueError, InvalidUpdateError


def set_data(dummy_service, data):
    dummy_service.get_line_items.return_value = data


class TestInvoiceApi:
    def test_get_open_line_items(self, invoice_app, dummy_service):
        data = []
        set_data(dummy_service, data)

        r = invoice_app.get("/lineitems")

        assert r.status_code == 200
        assert json.loads(r.data) == data
        assert "Content-Type" in r.headers
        assert r.headers["Content-Type"] == "application/json"

    def test_update_line_item(self, invoice_app, dummy_service):
        updated_item = {"adjustments": 123.6}
        dummy_service.update_line_item.return_value = "dummy"

        r = invoice_app.put("/lineitems/1", data=json.dumps(updated_item))

        assert r.status_code == 200
        assert json.loads(r.data) == "dummy"
        dummy_service.update_line_item.assert_called_once_with(1, updated_item)

    def test_update_line_item_returns_404_if_id_not_an_int(self, invoice_app, dummy_service):
        r = invoice_app.put("/lineitems/bleh", data=json.dumps({}))

        assert r.status_code == 404

    def test_update_line_item_returns_404_if_id_not_found(self, invoice_app, dummy_service):
        dummy_service.update_line_item.side_effect = ItemNotFound

        r = invoice_app.put("/lineitems/1", data=json.dumps({}))

        assert r.status_code == 404

    def test_update_line_item_returns_401_if_readonly_property_set(self, invoice_app, dummy_service):
        dummy_service.update_line_item.side_effect = ReadOnlyItemValueError

        r = invoice_app.put("/lineitems/1", data=json.dumps({"something": "value"}))

        assert r.status_code == 401

    def test_update_line_item_returns_400_if_invalid_property_set(self, invoice_app, dummy_service):
        dummy_service.update_line_item.side_effect = InvalidUpdateError

        r = invoice_app.put("/lineitems/1", data=json.dumps({"something": "value"}))

        assert r.status_code == 400
