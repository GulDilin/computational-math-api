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
                if points_count > 100:
                    return {'error': 'Too many dots for interpolation'}
            except Exception as ex:
                return {'error': 'left and right need to be decimal'}, 400

            left_error = False
            right_error = False
            try:
                x = left
                eval(data['function'])
            except (NameError, SyntaxError):
                return {'error': 'function cannot be recognized'}, 400
            except Exception:
                left_error = True


            try:
                x = right
                eval(data['function'])
            except Exception as ex:
                right_error = True

            if left_error and right_error:
                return {'error': 'function cannot be counted in that limits'}, 400
            elif left_error:
                return {'error': 'function cannot be counted in left limit'}, 400
            elif right_error:
                return {'error': 'function cannot be counted in right limit'}, 400

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
            if 'correct_x' in data:
                for el in data['correct_x']:
                    if float(el['x']) in base_x:
                        return {'error': 'corrected X already in use'}, 400
                    base_x[el['index']] = float(el['x'])

            left, right = min(base_x), max(base_x)

            print(f'base x = {base_x}')
            print(f'func = {[funct.func(el) for el in base_x]}')
            try:
                f = [funct.func(el) for el in base_x]
            except Exception:
                return {'error': 'function cannot be counted in some dot'}, 400

            if 'correct_y' in data:
                for el in data['correct_y']:
                    f[el['index']] = float(el['y'])
            print(f'approx = {[lagrang.approx(f, base_x, el) for el in base_x]}')

            if new_x is not None:
                if new_x > right:
                    right = new_x
                elif new_x < left:
                    left = new_x
                new_y =lagrang.approx(f, base_x, new_x)

            x = [left + (right - left) / 500 * i for i in range(500 + 1)]
            print(f'x {x[0]} {x[-1]}')

            res = [{
                        'name': 'Original',
                        'type': 'line',
                        'data': [{
                            'x': el,
                            'y': funct.func(el)
                        } for el in x]
                    }, {
                        'name': 'Dots',
                        'type': 'scatter',
                        'data': [{
                            'x': base_x[i],
                            'y': f[i]
                        } for i in range(len(base_x))]
                    }]

            if is_approx:
                res.append({
                        'name': 'Interpolate',
                        'type': 'line',
                        'data': [{
                            'x': el,
                            'y': lagrang.approx(f, base_x, el)
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
