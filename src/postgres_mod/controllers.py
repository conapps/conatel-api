from flask import Blueprint

postgres_sql = Blueprint('model', __name__, url_prefix='/model')

required_fields = ["ap_id", 'ap_mac',"location_name", "has_licence"]

@model.route('/aps', methods=['GET'])
def get_all():
    try:
        aps = get_all_aps()
        return jsonify(aps)
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@model.route('/aps/<ap_id>', methods=['GET'])
def get(ap_id):
    try:
        return jsonify(get_ap(ap_id))
    except Exception as e:
        return jsonify({
            'success': False,
            'message': "ap does not exist."
        }), 404


@model.route('/aps', methods=['POST'])
def add():
    ap_json = request.get_json()
    for field in required_fields:
        if field not in ap_json:
            return jsonify({
                'success': False,
                'message': f"Field {field} is missing!"
            }), 400
    try:
        add_ap(ap_json)
        return jsonify({
            'success': True,
            'message': "ap created succesfully!"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@model.route('/aps/<ap_id>', methods=['PUT'])
def put(ap_id):
    ap_json = request.get_json()
    for field in required_fields:
        if field not in ap_json:
            return jsonify({
                'success': False,
                'message': f"Field {field} is missing!"
            }), 400
    try:
        edit_ap(ap_id, ap_json)
        return jsonify({
            'success': True,
            'message': "ap edited succesfully!"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@model.route('/aps/<ap_id>', methods=['DELETE'])
def delete(ap_id):
    try:
        delete_ap(ap_id)
        return jsonify({
            'success': True,
            'message': "ap deleted succesfully!"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500