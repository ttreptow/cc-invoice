from flask import Blueprint, jsonify, abort, json, request

from invoice_service.services import LINE_ITEM_SERVICE
from invoice_service.services.line_item_service import ItemNotFound, ReadOnlyItemValueError, InvalidUpdateError
from invoice_service.services.service_factory import ServiceFactory

line_items = Blueprint('line_items', __name__, url_prefix="/lineitems")


line_item_service = ServiceFactory.create_proxy_service(LINE_ITEM_SERVICE)


@line_items.route("")
def get_line_items():
    return jsonify(line_item_service.get_line_items())


@line_items.route("/<item_id>", methods=['PUT'])
def update_line_item(item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        abort(404)
    try:
        return jsonify(line_item_service.update_line_item(item_id, json.loads(request.data)))
    except ItemNotFound:
        abort(404)
    except ReadOnlyItemValueError:
        abort(401)
    except InvalidUpdateError:
        abort(400)
