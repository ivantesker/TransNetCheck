from flask import Flask, request, render_template, send_from_directory
from flask_restful import Resource, Api, reqparse, abort
from sqlalchemy import create_engine
from json import dumps
import time
import math

e = create_engine('sqlite:///db/tnc.db')

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('latitude', type=float, required=True, location='form')
parser.add_argument('longtitude', type=float,  required=True, location='form')
parser.add_argument('level', type=int, required=True, location='form')
parser.add_argument('checksum', type=int, required=True, location='form')
parser.add_argument('operator', type=str, required = True, location='form')
parser.add_argument('type', type=str, location='form')


def check_request(data):
    # print(data['latitude'])
    # print(data['longtitude'])
    # print(data['level'])
    # print(data['checksum'])

    # if int(data['latitude'] ** 2 + math.sqrt(data['longtitude']) + math.log10(data['level'])) % 1000 == data['checksum']:
    #     return True
    # else:
    #     return False
    return True

class Signals(Resource):
    def get(self):
        conn = e.connect()
        query = conn.execute("select * from signals")

        return {'signals': [i for i in query.cursor.fetchall()]}

    def put(self):
        args = parser.parse_args()
        conn = e.connect()
        if args['type']:
            command = "INSERT INTO signals(latitude, longtitude, level, date, operator, ntype) VALUES({latitude}, {longtitude}, {level}, {date}, {operator}, {ntype})"\
                .format(latitude=args['latitude'], longtitude=args['longtitude'], level=args['level'], date=int(time.time()), operator=args['operator'].lower(), ntype=args['type'])
        else:
            command = "INSERT INTO signals(latitude, longtitude, level, date, operator) VALUES({latitude}, {longtitude}, {level}, {date}, {operator})"\
                .format(latitude=args['latitude'], longtitude=args['longtitude'], level=args['level'], date=int(time.time()), operator=args['operator'].lower())
        if check_request(args):
            query = conn.execute(command)
            return 'Success'
        else:
            return 'Checksum error'

    def delete(self):
        pass

    def post(self):
        pass
 

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
  return send_from_directory('./map/', path)

@app.route('/map')
def root():
  return send_from_directory('./map/', 'index.html')

@app.route('/')
def index():
    return render_template('index.html')

api.add_resource(Signals, '/signals')


# @app.route('/<path:path>', methods=['GET'])
# def static_proxy(path):
#   return send_from_directory('map/', path)

if __name__ == '__main__':
  # This is used when running locally only. When deploying use a webserver process 
  # such as Gunicorn to serve the app.
  app.run(host='127.0.0.1', port=6060, debug=True)


@app.errorhandler(500)
def server_error(e):
  return 'An internal error occurred [main.py] %s' % e, 500