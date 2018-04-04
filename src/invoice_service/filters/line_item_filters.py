from invoice_service.models.line_item import LineItem


class InvalidFilterField(Exception):
    pass


class InvalidFilterOperation(Exception):
    pass


def eq_operation(field_name, values):
    return getattr(LineItem, field_name).__eq__(values)


def in_operation(field_name, values):
    return getattr(LineItem, field_name).in_(values)


LINE_ITEM_OPS = {
    "eq": eq_operation,
    "in": in_operation
}


def build_line_item_filter(field_name, operation, values):
    if field_name not in {col.name for col in LineItem.__table__.c}:
        raise InvalidFilterField(field_name)
    if operation not in LINE_ITEM_OPS:
        raise InvalidFilterOperation(operation)
    return LINE_ITEM_OPS[operation](field_name, values)


def build_filter_from_model(filter_model):
    return build_line_item_filter(filter_model.field_name, filter_model.operation, filter_model.values)
