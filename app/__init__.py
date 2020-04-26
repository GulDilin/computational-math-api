from flask import Flask
from .api import LagrangeApprox
from flask_restful import Api
from flask_cors import CORS

def create_app():
    app = Flask(__name__)


    CORS(app, resources={r"/*": {"origins": "*"}})

    api = Api(app, prefix='/api')
    api.add_resource(LagrangeApprox, '/')
    return app
