from flask import json

from invoice_service.exceptions import ItemNotFound, ReadOnlyItemValueError, InvalidUpdateError
from invoice_service.models.line_item import LineItem


ITEMS = [
  {
    "id": 35,
    "campaign_id": 1,
    "campaign_name": "Satterfield-Turcotte : Multi-channelled next generation analyzer - e550",
    "line_item_name": "Small Wooden Computer - 8c6d",
    "booked_amount": 875449.3657976737,
    "actual_amount": 969912.1963626008,
    "adjustments": -13423.143355653474
  },
  {
    "id": 36,
    "campaign_id": 2,
    "campaign_name": "Shanahan, Homenick and Purdy : Reactive incremental migration - 81db",
    "line_item_name": "Fantastic Granite Hat - 42cc",
    "booked_amount": 617687.6273456443,
    "actual_amount": 643308.8871557572,
    "adjustments": 35466.90013675345
  },
  {
    "id": 37,
    "campaign_id": 2,
    "campaign_name": "Shanahan, Homenick and Purdy : Reactive incremental migration - 81db",
    "line_item_name": "Incredible Plastic Hat - 7101",
    "booked_amount": 410785.6854867741,
    "actual_amount": 419937.39176046196,
    "adjustments": -14380.071956024107
  }
]


def set_data(dummy_line_item_service, data):
    dummy_line_item_service.get_line_items.return_value = data


class TestLineItemApi:
    def test_get_open_line_items(self, app_client, dummy_line_item_service):
        data = []
        set_data(dummy_line_item_service, data)

        r = app_client.get("/lineitems")

        assert r.status_code == 200
        assert json.loads(r.data) == data
        assert "Content-Type" in r.headers
        assert r.headers["Content-Type"] == "application/json"

    def test_update_line_item(self, app_client, dummy_line_item_service):
        updated_item = {"adjustments": 123.6}
        dummy_line_item_service.update_line_item.return_value = "dummy"

        r = app_client.put("/lineitems/1", data=json.dumps(updated_item))

        assert r.status_code == 200
        assert json.loads(r.data) == "dummy"
        dummy_line_item_service.update_line_item.assert_called_once_with(1, updated_item)

    def test_update_line_item_returns_404_if_id_not_an_int(self, app_client, dummy_line_item_service):
        r = app_client.put("/lineitems/bleh", data=json.dumps({}))

        assert r.status_code == 404

    def test_update_line_item_returns_404_if_id_not_found(self, app_client, dummy_line_item_service):
        dummy_line_item_service.update_line_item.side_effect = ItemNotFound

        r = app_client.put("/lineitems/1", data=json.dumps({}))

        assert r.status_code == 404

    def test_update_line_item_returns_401_if_readonly_property_set(self, app_client, dummy_line_item_service):
        dummy_line_item_service.update_line_item.side_effect = ReadOnlyItemValueError

        r = app_client.put("/lineitems/1", data=json.dumps({"something": "value"}))

        assert r.status_code == 401

    def test_update_line_item_returns_400_if_invalid_property_set(self, app_client, dummy_line_item_service):
        dummy_line_item_service.update_line_item.side_effect = InvalidUpdateError

        r = app_client.put("/lineitems/1", data=json.dumps({"something": "value"}))

        assert r.status_code == 400

    def test_serialize_object(self, app_client, dummy_line_item_service):
        data = [LineItem(**item) for item in ITEMS]
        set_data(dummy_line_item_service, data)

        r = app_client.get("/lineitems")
        expected = dict(ITEMS[0])
        expected["invoice_id"] = None

        assert 200 == r.status_code
        assert expected == json.loads(r.data)[0]
