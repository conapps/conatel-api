from flask import jsonify

def error(message):
    return jsonify({
        'success': False,
        'message': message
    })
