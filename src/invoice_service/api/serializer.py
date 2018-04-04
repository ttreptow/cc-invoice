from flask import current_app, json

from invoice_service.models.base import BaseModel


def serialize(data):
    return current_app.response_class(
        (dumps(data), '\n'),
        mimetype=current_app.config['JSONIFY_MIMETYPE']
    )


def dumps(data):
    return json.dumps(data, default=dump_model)


def dump_model(obj):
    if isinstance(obj, BaseModel):
        return {col.name: getattr(obj, col.name) for col in obj.__table__.c}
    raise TypeError()
