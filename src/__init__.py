import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

CORS(app)


app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] =  os.getenv('SQL_URI')
# silence the deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


from src.crud.controller import ap

app.register_blueprint(ap)


@app.errorhandler(404)
def not_found(e):
    return error("No exite la ruta para la url deseada en esta api"), 404


@app.errorhandler(405)
def not_found(e):
    return error("No exite la ruta para la url deseada en esta api"), 405


def error(message):
    return jsonify({
        'success': False,
        'message': message
    })
