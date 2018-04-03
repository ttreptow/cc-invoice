from collections import defaultdict

from sqlalchemy.orm.exc import NoResultFound

from invoice_service.db_utils import scoped_session
from invoice_service.models.line_item import LineItem


class ItemNotFound(Exception):
    pass


class ReadOnlyItemValueError(Exception):
    pass


class InvalidUpdateError(Exception):
    pass


class LineItemService:
    def __init__(self, service_factory):
        self.session_maker = service_factory.session_maker
        self.editable_props = {"adjustments"}

    def get_line_items(self):
        with scoped_session(self.session_maker) as session:
            return session.query(LineItem).all()

    def get_grouped_items(self, group_by, values=None):
        with scoped_session(self.session_maker) as session:
            group_col = getattr(LineItem, group_by)
            items = session.query(group_col, LineItem)
            if values:
                items = items.filter(group_col.in_(values))
            grouped = defaultdict(list)
            for val, item in items:
                grouped[val].append(item)
            return grouped

    def get_line_item(self, item_id):
        with scoped_session(self.session_maker) as session:
            items = session.query(LineItem).filter(LineItem.id == item_id)
            try:
                return items.one()
            except NoResultFound:
                raise ItemNotFound(item_id)

    def add_item(self, item):
        self.add_items([item])

    def add_items(self, items):
        with scoped_session(self.session_maker) as session:
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
        with scoped_session(self.session_maker) as session:
            session.query(LineItem).filter(LineItem.id == item_id).update(attributes, synchronize_session=False)
            session.commit()
