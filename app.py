from flask import Flask, jsonify, request, Response
import json

from settings import *


def validBookObject(book):
    if 'KeyName' in dictionaryObject:
        return True
    return False


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if (request_data['isbn'] == False):
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = '/books'

    else:
        response = Response(json.dumps(invalidErrorMsg), status=400,
                            mimetype='application/json')
    return response


@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request = request.get_json()
    if True:
        response = Response("", 204)
    else:
        response = Response(json.dumps(invalidErrorMsg), status=400,
                            mimetype='application/json')
    return response


@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    if True:
        response = Response("", status=204)
    else:
        response = Response("", status=404, mimetype='application/json')
    return response


invalidErrorMsg = {
    'error': 'an Error'
    'message': 'a Message'
}

app.run(port=5000)
