import pytest

from invoice_service.db_utils import scoped_session
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


def add_item(session_maker, item_dict):
    item = LineItem(**item_dict)
    with scoped_session(session_maker) as sess:
        sess.add(item)
        sess.commit()


def assert_item_equal(item, expected_item_dict):
    for col in LineItem.__table__.c:
        assert expected_item_dict[col.name] == getattr(item, col.name)


class TestInvoiceService:
    def test_get_line_items_empty(self, invoice_service):
        items = invoice_service.get_line_items()

        assert items == []

    def test_get_line_items(self, invoice_service, session_maker):
        add_item(session_maker, DUMMY_ITEM)

        items = list(invoice_service.get_line_items())

        assert len(items) == 1
        assert_item_equal(items[0], DUMMY_ITEM)

    def test_get_line_item(self, invoice_service, session_maker):
        add_item(session_maker, DUMMY_ITEM)

        item = invoice_service.get_line_item(1)

        assert_item_equal(item, DUMMY_ITEM)

    def test_update_line_item(self, invoice_service, session_maker):
        add_item(session_maker, DUMMY_ITEM)

        invoice_service.update_line_item(1, {"adjustments": 123.1})

        updated_item = invoice_service.get_line_item(1)

        expected = DUMMY_ITEM.copy()
        expected["adjustments"] = 123.1

        assert_item_equal(updated_item, expected)

    def test_raise_error_when_updating_readonly(self, invoice_service, session_maker):
        add_item(session_maker, DUMMY_ITEM)

        with pytest.raises(ReadOnlyItemValueError):
            invoice_service.update_line_item(1, {"adjustments": 123.1, "booked_amount": 555.13})

        updated_item = invoice_service.get_line_item(1)
        assert_item_equal(updated_item, DUMMY_ITEM)

    def test_raise_error_when_updaing_invalid_props(self, invoice_service, session_maker):
        add_item(session_maker, DUMMY_ITEM)

        with pytest.raises(InvalidUpdateError):
            invoice_service.update_line_item(1, {"adjustments": 123.1, "booked_amount": 555.13, "something": 333.2})

        updated_item = invoice_service.get_line_item(1)

        assert_item_equal(updated_item, DUMMY_ITEM)
