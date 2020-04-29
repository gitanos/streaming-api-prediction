from math import exp
from flask import jsonify, request
from flask_restful import Resource, reqparse

parser = reqparse.RequestParser()


def make_calculations(age, l_bp, rmean_rr, stdev_t):

    x_beta = -5 + 0.002 * age + 0.001 * l_bp + 0.03 * rmean_rr + 0.02 * stdev_t

    probability = exp(x_beta) / (1 + exp(x_beta))

    return probability


class Model(Resource):
    def post(self):

        parser.add_argument('age', default=0, type=int)
        parser.add_argument('last_blood_pressure', default=0.0, type=float)
        parser.add_argument('rmean_respiration_rate', default=0.0, type=float)
        parser.add_argument('standard_deviation_temperature', default=0.0, type=float)

        data = parser.parse_args()

        # TODO: adjust to parser
        data = request.get_json(force=True)

        print('DATA IN: ', data)

        prob_out = make_calculations(data['age'], \
                                     data['last_blood_pressure'], \
                                     data['rmean_respiration_rate'], \
                                     data['standard_deviation_temperature'])

        print('CALCULATED PROBABILITY value: {} FOR AGE {}'.format(prob_out, data['age']))
        return prob_out


