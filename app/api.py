from flask import Flask
from flask_restful import Resource
from flask_restful import reqparse
from flask import current_app as app
from math import sin, cos, tan, sqrt
from flask import request
from counter import lagrang
import json

app = Flask(__name__)


class Function:
    def __init__(self, func_str):
        self.func_str = func_str

    def func(self, x):
        return eval(self.func_str)


class LagrangeApprox(Resource):
    def post(self):
        try:
            data = json.loads(request.data)
            print(request.data)
            if 'function' not in data or 'left' not in data or 'right' not in data or 'points_count' not in data:
                return {'error': 'function, left, right and points_count are required params'}, 400
            try:
                left = float(data['left'])
                right = float(data['right'])
                points_count = float(data['points_count'])
            except Exception as ex:
                return {'error': 'left and right need to be decimal'}, 400

            try:
                x = 0
                eval(data['function'])
            except Exception as ex:
                return {'error': 'function cannot be recognized'}, 400

            is_approx = False
            if 'approximate' in data:
                try:
                    is_approx = bool(data['approximate'])
                except Exception:
                    return {'error': 'approximate is optional bool parameter'}

            new_x = None
            new_y = None
            if 'new_x' in data:
                if not is_approx:
                    return {'error': 'new_x can be used only with approx'}
                try:
                    new_x = float(data['new_x'])
                except Exception:
                    return {'error': 'new_x is optional float parameter'}

            if left > right:
                left, right = right, left

            func_str = data['function']
            funct = Function(func_str)
            d = abs(right - left) / (points_count - 1)
            print(f'd = {d}')
            base_x = [left + d * i for i in range(int(points_count))]
            print(f'base x = {base_x}')
            print(f'approx = {[funct.func(el) for el in base_x]}')
            print(f'approx = {[lagrang.approx(funct.func, base_x, el) for el in base_x]}')

            if new_x is not None:
                if new_x > right:
                    right = new_x
                elif new_x < left:
                    left = new_x
                new_y =lagrang.approx(funct.func, base_x, new_x)

            x = [left + (right - left) / 500 * i for i in range(500 + 1)]
            print(f'x {x[0]} {x[-1]}')

            res = [{
                        'name': 'Original',
                        'type': 'line',
                        'data': [{
                            'x': round(el * 1000) / 1000,
                            'y': round(funct.func(el) * 1000) / 1000
                        } for el in x]
                    }, {
                        'name': 'Dots',
                        'type': 'scatter',
                        'data': [{
                            'x': round(el * 1000) / 1000,
                            'y': round(funct.func(el) * 1000) / 1000
                        } for el in base_x]
                    }]

            if is_approx:
                res.append({
                        'name': 'Approximate',
                        'type': 'line',
                        'data': [{
                            'x': round(el * 1000) / 1000,
                            'y': round(lagrang.approx(funct.func, base_x, el)* 1000) / 1000
                        } for el in x]
                    })
            if new_x is not None:
                res.append({
                    'name': 'New dot',
                    'type': 'scatter',
                    'data': [{
                        'x': new_x,
                        'y': new_y
                    }]
                })
                return {'series': res, "new_y": new_y}

            return {'series': res}
        except Exception as e:
            return {'error': str(e)}, 400
