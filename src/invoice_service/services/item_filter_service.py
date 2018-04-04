import json

from sqlalchemy.orm import make_transient

from invoice_service.models.active_item_filter import ActiveItemFilter


class ItemFilterService:
    def __init__(self, service_factory):
        self.session_maker = service_factory.session_maker

    def get_active_filters(self):
        session = self.session_maker()
        filters = []
        for f in session.query(ActiveItemFilter):
            make_transient(f)
            f.values = json.loads(f.values)
            filters.append(f)
        return filters

    def add_filter(self, field_name, operation, values):
        session = self.session_maker()
        session.add(ActiveItemFilter(field_name=field_name, operation=operation, values=json.dumps(values)))
        session.commit()

    def clear_active_filters(self):
        session = self.session_maker()
        session.query(ActiveItemFilter).delete(synchronize_session=False)
        session.commit()
