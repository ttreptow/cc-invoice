import pytest
from sqlalchemy.sql.elements import BinaryExpression

from invoice_service.filters.line_item_filters import InvalidFilterField, InvalidFilterOperation, build_line_item_filter


class TestFilterBuilder:
    def test_invalid_field_name_raises_error(self):
        with pytest.raises(InvalidFilterField):
            build_line_item_filter("blah", "eq", 1)

    def test_invalid_operation_raises_error(self):
        with pytest.raises(InvalidFilterOperation):
            build_line_item_filter("campaign_id", "foo", 1)

    def test_filter_eq(self):
        f = build_line_item_filter("campaign_id", "eq", 1)

        assert isinstance(f, BinaryExpression)
        assert f.right.value == 1
        assert f.left.key == "campaign_id"

