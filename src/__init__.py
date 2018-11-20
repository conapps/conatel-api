from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

app.config.from_object('config')


@app.errorhandler(404)
def not_found(error):
    return False

from src.postgres_mod.controllers import model

app.register_blueprint(model)