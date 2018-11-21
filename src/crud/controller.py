from flask import Blueprint, jsonify, request

from src.crud.model import Ap

ap = Blueprint('aps', __name__, url_prefix='/aps')

required_fields = ["ap_mac", "location_name", "has_licence"]


@ap.route('', methods=['GET'])
def get_all():
    try:
        aps = Ap.get_all_aps()
        return jsonify(aps), 200
    except Exception as e:
        return error(str(e)), 500


@ap.route('/<ap_id>', methods=['GET'])
def get(ap_id):
    try:
        return jsonify(Ap.get_ap(ap_id)), 200
    except Exception as e:
        return error('ap does not exist'), 404


@ap.route('', methods=['POST'])
def add():
    ap_json=request.get_json()
    for field in required_fields:
        if field not in ap_json:
            return error(f"Field {field} is missing!"), 400
    try:
        Ap.add_ap(ap_json["ap_mac"], ap_json["location_name"],
                  ap_json["has_licence"])
        return "", 201
    except Exception as e:
        return error(str(e)), 500


@ap.route('/<ap_id>', methods=['PUT'])
def put(ap_id):
    ap_json=request.get_json()
    try:
        Ap.update_ap(ap_id, ap_json)
        return "", 201
    except Exception as e:
        return error(str(e)), 500


@ap.route('/<ap_id>', methods=['DELETE'])
def delete(ap_id):
    try:
        Ap.delete_ap(ap_id)
        return "", 204
    except Exception as e:
        return error(str(e)), 500


def error(message):
    return jsonify({
        'success': False,
        'message': message
    })
