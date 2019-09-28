from flask import Flask, request, render_template, send_from_directory
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
from sqlalchemy import create_engine
from json import dumps
import time
import math
import requests
import json

e = create_engine('sqlite:///db/tnc.db')

city_api = "https://geocode-maps.yandex.ru/1.x/"

stations_api = "https://api.rasp.yandex.net/v3.0/nearest_stations/"

app = Flask(__name__)
api = Api(app)
CORS(app)

parser = reqparse.RequestParser()
parser.add_argument('latitude', type=float, required=True, location='args')
parser.add_argument('longtitude', type=float,  required=True, location='args')
parser.add_argument('level', type=int, required=True, location='args')
parser.add_argument('checksum', type=int, required=True, location='args')
parser.add_argument('operator', type=str, required = True, location='args')
parser.add_argument('type', type=str, location='args')

stat_parser = reqparse.RequestParser()
stat_parser.add_argument('city', type=str, location='args')

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

# def get_coordinate(data):
#     pass
    
def form_query(data):
    pass
    
def get_center(points):
    up = points['upperCorner'].split(' ')
    low = points['lowerCorner'].split(' ')
    return (float(up[0]) + float(low[0])) / 2, (float(up[1]) + float(low[1])) / 2

def get_city_points(d):
    try:
        points = d['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['boundedBy']['Envelope']
    except:
        points = d['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope']
    return points
    
def get_json_response(api, payload):
    r = requests.get(api, params=payload).text
    d = json.loads(r)
    return d

def form_stations(d):
    a = d['stations']
    stations = dict()
    titles = []
    codes = []
    for i in a:
        stations[i['title']] = i['code']
    #     titles.append(i['title'])
    #     codes.append(i['code'])
    # stations.append(titles)
    # stations.append(codes)
    return stations

class Signals(Resource):
    def get(self):
        conn = e.connect()
        query = conn.execute("select * from signals")

        return {'signals': [i for i in query.cursor.fetchall()]}

    def post(self):
        args = parser.parse_args()
        conn = e.connect()
        # print(response.text)
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

    def put(self):
        pass

class Stations(Resource):
    def get(self):
        args = stat_parser.parse_args()
        stations = []
        city_load = {'apikey': '9491694e-e68b-4127-b2ce-272871fde6a2', 'geocode': args['city'].replace("\"",''), 'format':'json'}
        # print(city_load)
        d = get_json_response(city_api, city_load)
        # print(d)
        points = get_city_points(d)
        lon, lat = get_center(points)
        # print(lon, lat)
        stations_load = {'apikey': 'f88c2a51-4a12-4072-bf65-4da9626ea175', 'format':'json', 'lng': str(lon), 'lat': str(lat), 'distance': '30', 'limit':'50','transport_types':'train' }
        d = get_json_response(stations_api, stations_load)
        return form_stations(d)


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
  return send_from_directory('./map/', path)

@app.route('/')
def root():
  return send_from_directory('./map/', 'index.html')

@app.route('/home')
def index():
    return render_template('index.html')

api.add_resource(Signals, '/signals')

api.add_resource(Stations, '/stations')



# @app.route('/<path:path>', methods=['GET'])
# def static_proxy(path):
#   return send_from_directory('map/', path)

if __name__ == '__main__':
     app.run(host='localhost', port=555, debug=True)

@app.errorhandler(500)
def server_error(e):
  return 'An internal error occurred [main.py] %s' % e, 500