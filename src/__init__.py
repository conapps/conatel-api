import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_oidc import OpenIDConnect


################### Logging information #######################

logger = logging.getLogger('api')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('api.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - [%(name)s/%(funcName)s] - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

##############################################################

app = Flask(__name__)

CORS(app)

app.config.from_object('config')


app.config.update({
    'SECRET_KEY': os.getenv('SECRET_KEY'),
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_USER_INFO_ENABLED': True,
    'OIDC_OPENID_REALM': 'api',
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post',
    'OIDC_VALID_ISSUERS': [os.getenv('VALID_ISSUER')]
})

oidc = OpenIDConnect(app)

app.config['SQLALCHEMY_DATABASE_URI'] =  os.getenv('SQL_URI')
# silence the deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


from src.crud.controller import ap
from src.auth.controller import auth

app.register_blueprint(ap)
app.register_blueprint(auth)

@app.errorhandler(404)
def not_found(e):
    return error("No exite la ruta para la url deseada en esta api"), 404


@app.errorhandler(405)
def doesnt_exist(e):
    return error("No exite la ruta para la url deseada en esta api"), 405


def error(message):
    return jsonify({
        'success': False,
        'message': message
    })
