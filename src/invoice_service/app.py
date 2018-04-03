from flask import request, jsonify, json, abort

from invoice_service.app_factory import create_app, get_service
from invoice_service.service import ItemNotFound, ReadOnlyItemValueError, InvalidUpdateError

app = create_app()


@app.route("/lineitems")
def get_line_items():
    return jsonify(get_service().get_line_items())


@app.route("/lineitems/<item_id>", methods=['PUT'])
def update_line_item(item_id):
    try:
        item_id = int(item_id)
    except ValueError:
        abort(404)
    try:
        return jsonify(get_service().update_line_item(item_id, json.loads(request.data)))
    except ItemNotFound:
        abort(404)
    except ReadOnlyItemValueError:
        abort(401)
    except InvalidUpdateError:
        abort(400)

