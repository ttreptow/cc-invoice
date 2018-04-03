from collections import defaultdict

from sqlalchemy.orm.exc import NoResultFound

from invoice_service.exceptions import ItemNotFound, ReadOnlyItemValueError, InvalidUpdateError
from invoice_service.models.line_item import LineItem


def add_filters(base_query, filters):
    if len(filters) == 0:
        filters = [LineItem.invoice_id.is_(None)]
    for f in filters:
        base_query = base_query.filter(f)
    return base_query


class LineItemService:
    def __init__(self, service_factory):
        self.session_maker = service_factory.session_maker
        self.editable_props = {"adjustments"}

    def get_line_items(self, *filters):
        session = self.session_maker()
        return add_filters(session.query(LineItem), filters).all()

    def get_grouped_items(self, group_by, *filters):
        session = self.session_maker()
        group_col = getattr(LineItem, group_by)
        items = add_filters(session.query(group_col, LineItem), filters)
        grouped = defaultdict(list)
        for val, item in items:
            grouped[val].append(item)
        return grouped

    def get_line_item(self, item_id):
        session = self.session_maker()
        items = session.query(LineItem).filter(LineItem.id == item_id)
        try:
            return items.one()
        except NoResultFound:
            raise ItemNotFound(item_id)

    def add_item(self, item):
        self.add_items([item])

    def add_items(self, items):
        session = self.session_maker()
        for item in items:
            session.add(item)
        session.commit()

    def update_line_item(self, item_id, attributes):
        if not isinstance(attributes, dict):
            raise InvalidUpdateError()
        line_item_cols = {col.name for col in LineItem.__table__.c}
        if attributes.keys() - line_item_cols:
            raise InvalidUpdateError()
        if attributes.keys() - self.editable_props:
            raise ReadOnlyItemValueError()
        session = self.session_maker()
        session.query(LineItem).filter(LineItem.id == item_id).update(attributes, synchronize_session=False)
        session.commit()

    def set_invoice(self, invoice_id):
        session = self.session_maker()
        session.query(LineItem).filter(LineItem.invoice_id.is_(None)).update({"invoice_id": invoice_id},
                                                                             synchronize_session=False)
        session.commit()
