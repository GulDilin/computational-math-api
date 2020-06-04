from flask import Flask
from .api import LagrangeApprox
from .api import DifferentialEquations
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)


CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app, prefix='/api')
api.add_resource(LagrangeApprox, '/')
api.add_resource(DifferentialEquations, '/diff_eq')

