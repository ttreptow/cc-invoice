import pytest

from invoice_service.models.line_item import LineItem
from invoice_service.services.line_item_service import ReadOnlyItemValueError, InvalidUpdateError

DUMMY_ITEM = {
        "id": 1,
        "campaign_id": 1,
        "campaign_name": "Satterfield-Turcotte : Multi-channelled next generation analyzer - e550",
        "line_item_name": "Awesome Plastic Car - 6475",
        "booked_amount": 430706.6871532752,
        "actual_amount": 401966.50504006835,
        "adjustments": 1311.0731142230268
    }


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


def assert_item_equal(item, expected_item_dict):
    for col in LineItem.__table__.c:
        assert expected_item_dict[col.name] == getattr(item, col.name)


class TestInvoiceService:
    def test_get_line_items_empty(self, line_item_service):
        items = line_item_service.get_line_items()

        assert items == []

    def test_get_line_items(self, line_item_service):
        line_item_service.add_item(LineItem(**DUMMY_ITEM))

        items = list(line_item_service.get_line_items())

        assert len(items) == 1
        assert_item_equal(items[0], DUMMY_ITEM)

    def test_get_line_item(self, line_item_service):
        line_item_service.add_item(LineItem(**DUMMY_ITEM))

        item = line_item_service.get_line_item(1)

        assert_item_equal(item, DUMMY_ITEM)

    def test_update_line_item(self, line_item_service):
        line_item_service.add_item(LineItem(**DUMMY_ITEM))

        line_item_service.update_line_item(1, {"adjustments": 123.1})

        updated_item = line_item_service.get_line_item(1)

        expected = DUMMY_ITEM.copy()
        expected["adjustments"] = 123.1

        assert_item_equal(updated_item, expected)

    def test_raise_error_when_updating_readonly(self, line_item_service):
        line_item_service.add_item(LineItem(**DUMMY_ITEM))

        with pytest.raises(ReadOnlyItemValueError):
            line_item_service.update_line_item(1, {"adjustments": 123.1, "booked_amount": 555.13})

        updated_item = line_item_service.get_line_item(1)
        assert_item_equal(updated_item, DUMMY_ITEM)

    def test_raise_error_when_updaing_invalid_props(self, line_item_service):
        line_item_service.add_item(LineItem(**DUMMY_ITEM))

        with pytest.raises(InvalidUpdateError):
            line_item_service.update_line_item(1, {"adjustments": 123.1, "booked_amount": 555.13, "something": 333.2})

        updated_item = line_item_service.get_line_item(1)

        assert_item_equal(updated_item, DUMMY_ITEM)

    def test_get_grouped_items(self, line_item_service):
        line_item_service.add_items(LineItem(**item) for item in ITEMS)

        items = line_item_service.get_grouped_items(group_by="campaign_id")

        assert isinstance(items, dict)
        assert len(items[1]) == 1
        assert len(items[2]) == 2

    def test_get_grouped_items_with_filter(self, line_item_service):
        line_item_service.add_items(LineItem(**item) for item in ITEMS)

        items = line_item_service.get_grouped_items(group_by="campaign_id", values=[2])

        assert isinstance(items, dict)
        assert 1 not in items
        assert 2 == len(items[2])
