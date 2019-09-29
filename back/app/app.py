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

route_api = "https://api.rasp.yandex.net/v3.0/search/"

route_stations_api = "https://api.rasp.yandex.net/v3.0/thread/"

app = Flask(__name__)
api = Api(app)
CORS(app)

parser = reqparse.RequestParser()
parser.add_argument('latitude', type=float, required=True, location='form')
parser.add_argument('longtitude', type=float,  required=True, location='form')
parser.add_argument('level', type=int, required=True, location='form')
parser.add_argument('checksum', type=int, required=True, location='form')
parser.add_argument('operator', type=str, required = True, location='form')
parser.add_argument('type', type=str, location='form')

stat_parser = reqparse.RequestParser()
stat_parser.add_argument('city', type=str, required = True, location='args')

route_parser = reqparse.RequestParser()
route_parser.add_argument('start_point', type=str, required = True, location='args')
route_parser.add_argument('end_point', type=str, required = True, location='args')
route_parser.add_argument('number', type=str,  location='args')
route_parser.add_argument('title', type=str,  location='args')


# test
coordinates = dict()

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
    return stations

class Signals(Resource):
    def get(self):
        conn = e.connect()
        query = conn.execute("select * from signals")

        return {'signals': [i for i in query.cursor.fetchall()]}

    def put(self):
        args = parser.parse_args()
        conn = e.connect()
        print(request.data)
        if args['type']:
            command = "INSERT INTO signals(latitude, longtitude, level, date, operator, ntype) VALUES({latitude}, {longtitude}, {level}, {date}, {operator}, {ntype})"\
                .format(latitude=args['latitude'], longtitude=args['longtitude'], level=args['level'], date=int(time.time()), operator=args['operator'].lower(), ntype=args['type'])
        else:
            command = "INSERT INTO signals(latitude, longtitude, level, date, operator) VALUES({latitude}, {longtitude}, {level}, {date}, {operator})"\
                .format(latitude=args['latitude'], longtitude=args['longtitude'], level=args['level'], date=int(time.time()), operator=args['operator'].lower())
        if check_request(args):
            query = conn.execute(command)
            return {'Response':'Success'}
        else:
            return {'Response':'Checksum error'}

    def delete(self):
        pass

    def post(self):
        # print(json.loads(request.data))
        
        args = json.loads(request.data.decode('UTF-8').replace("'", '"'))
        # parser.parse_args()
        conn = e.connect()
        print('OK')
        print(request)
        if args['type']:
            command = "INSERT INTO signals(latitude, longtitude, level, date, operator, ntype) VALUES({latitude}, {longtitude}, {level}, {date}, '{operator}', '{ntype}')"\
                .format(latitude=args['latitude'], longtitude=args['longtitude'], level=args['level'], date=int(time.time()), operator=args['operator'].lower(), ntype=str(args['type']))
            print(command)
        else:
            command = "INSERT INTO signals(latitude, longtitude, level, date, operator) VALUES({latitude}, {longtitude}, {level}, {date}, '{operator}')"\
                .format(latitude=args['latitude'], longtitude=args['longtitude'], level=args['level'], date=int(time.time()), operator=args['operator'].lower())
        if check_request(args):
            query = conn.execute(command)
            return {'Response':'Success'}
        else:
            return {'Response':'Checksum error'}

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

class Routes(Resource):
    def post(self):
        args = route_parser.parse_args()
        route_load = {'apikey': 'f88c2a51-4a12-4072-bf65-4da9626ea175', 'format':'json', 'from': args['start_point'], 'to': args['end_point'], 'transport_types':'train'}
        d = get_json_response(route_api, route_load)['segments']

        uids = []
        for i in d:
            ro = str(i['thread']['number']) + " " + str(i['thread']['title'])
            if ro not in uids:
                uids.append(ro)
        return uids
    
    def put(self):
        args = route_parser.parse_args()
        route_load = {'apikey': 'f88c2a51-4a12-4072-bf65-4da9626ea175', 'format':'json', 'from': args['start_point'], 'to': args['end_point'], 'transport_types':'train'}
        d = get_json_response(route_api, route_load)['segments']
        
        threads = []

        for i in d:
            if i['thread']['number'] != args['number']:
                continue
            route_stations_load= {'apikey': 'f88c2a51-4a12-4072-bf65-4da9626ea175', 'format':'json', 'uid': i['thread']['uid']}
            e = get_json_response(route_stations_api, route_stations_load)
            threads = []
            for j in e['stops']:
                if j['station']['title'] in coordinates:
                    [lon, lat] = coordinates[j['station']['title']]
                else:
                    city_load = {'apikey': '9491694e-e68b-4127-b2ce-272871fde6a2', 'geocode': j['station']['title'], 'format':'json', 'results':'1'}
                    d = get_json_response(city_api, city_load)
                    points = get_city_points(d)
                    lon, lat = get_center(points)
                    coordinates[j['station']['title']] = [lon, lat]
                station_meta = []
                station_meta.append(lon)
                station_meta.append(lat)
                threads.append(station_meta)
        if threads:
            return threads
        else:
            return {'message': 'Error'}

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

api.add_resource(Routes, '/routes')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=999 , debug=True)

@app.errorhandler(500)
def server_error(e):
  return 'An internal error occurred [main.py] %s' % e, 500