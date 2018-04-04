import json

from invoice_service.api.serializer import dumps
from invoice_service.models.line_item import LineItem

ITEM_DATA = {
    "id": 36,
    "campaign_id": 2,
    "campaign_name": "Shanahan, Homenick and Purdy : Reactive incremental migration - 81db",
    "line_item_name": "Fantastic Granite Hat - 42cc",
    "booked_amount": 617687.6273456443,
    "actual_amount": 643308.8871557572,
    "adjustments": 35466.90013675345,
    "invoice_id": None
  }


def test_serialize_item():
    item = LineItem(**ITEM_DATA)

    result = json.loads(dumps(item))

    assert result == ITEM_DATA
