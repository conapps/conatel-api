import os
import requests
import jwt
from flask import Blueprint, redirect, request, jsonify
from oauth2client.client import OAuth2Credentials
from src import oidc
from src.utils import error
from config import APP_DIR

auth = Blueprint('auth', __name__, url_prefix='/auth')


pem_path = os.path.join(APP_DIR, 'key.pem')


@auth.route('/login')
def login():
    return oidc.redirect_to_auth_server(None, request.values)


@auth.route('/callback')
@oidc.custom_callback
def callback(data):
    info = oidc.user_getinfo(['sub'])
    user_id = info.get('sub')
    if user_id in oidc.credentials_store:
        try:
            access_token = OAuth2Credentials.from_json(
                oidc.credentials_store[user_id]).access_token
            print ('access_token=<%s>' % access_token)
            headers = {'Authorization': 'Bearer %s' % (access_token)}
        except:
            a = 2
    return redirect('http://google.com', code=302)


@auth.route('/token_login', methods=['POST'])
def get_token():
    body = request.get_json()
    for field in ['username', 'password']:
        if field not in body:
            return error(f"Field {field} is missing!"), 400
    data = {
        'grant_type': 'password',
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'username': body['username'],
        'password': body['password']
    }
    response = requests.post(os.getenv('OPENID_URL') + '/token', data=data)
    if response.status_code != requests.codes.ok:
        return error("Error en username/password"), 400
    data = response.json()
    ret = {
        "access_token": data['access_token'],
        "refresh_token": data['refresh_token']
    }
    return jsonify(ret), 200


@auth.route('/token_refresh', methods=['POST'])
def refresh_token():
    body = request.get_json()
    for field in ['refresh_token']:
        if field not in body:
            return error(f"Field {field} is missing!"), 400
    data = {
        'grant_type': 'refresh_token',
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'refresh_token': body['refresh_token'],
    }
    response = requests.post(os.getenv('OPENID_URL') + '/token', data=data)
    if response.status_code != requests.codes.ok:
        return error("Error en refresh token"), 400
    data = response.json()
    ret = {
        "access_token": data['access_token'],
        "refresh_token": data['refresh_token']
    }
    return jsonify(ret), 200


@auth.route('/token_verify')
def verify():
    if 'token' not in request.headers:
        return error("Token is missing!"), 400
    with open(APP_DIR + "/key.pem", "rb") as f:
        public_key = f.read().decode('ascii')
    access_token = request.headers['token']
    try:
        access_token_json = jwt.decode(
            access_token, public_key, algorithms=['RS256'], audience=os.getenv('AUDIENCE'))
        return "", 204
    except Exception as e:
        return error("Error with deserialaizing the token"), 500


@auth.route('/token_logout', methods=['POST'])
def logout():
    body = request.get_json()
    for field in ['username', 'refresh_token']:
        if field not in body:
            return error(f"Field {field} is missing!"), 400
    data = {
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET'),
        'username': body['username'],
        'refresh_token': body['refresh_token']
    }
    response = requests.post(os.getenv('OPENID_URL') + '/logout', data=data)
    if response.status_code != 204:
        return error("Error en logging out"), 500
    return "", 204
