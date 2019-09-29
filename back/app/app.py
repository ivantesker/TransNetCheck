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
route_parser.add_argument('tele2', type=bool,  location='form')
route_parser.add_argument('mts_rus', type=bool,  location='form')
route_parser.add_argument('beeline', type=bool,  location='form')
route_parser.add_argument('megafon', type=bool,  location='form')
route_parser.add_argument('operator', type=bool,  location='form')




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
        stations_load = {'apikey': 'bd0e99aa-4519-482d-8f80-c9f07c53a090', 'format':'json', 'lng': str(lon), 'lat': str(lat), 'distance': '30', 'limit':'50','transport_types':'train' }
        d = get_json_response(stations_api, stations_load)
        return form_stations(d)

class Routes(Resource):
    def post(self):
        args = route_parser.parse_args()
        route_load = {'apikey': 'bd0e99aa-4519-482d-8f80-c9f07c53a090', 'format':'json', 'from': args['start_point'], 'to': args['end_point'], 'transport_types':'train'}
        # print(get_json_response(route_api, route_load))
        d = get_json_response(route_api, route_load)['segments']

        uids = []
        for i in d:
            ro = str(i['thread']['number']) + " " + str(i['thread']['title'])
            if ro not in uids:
                uids.append(ro)
        return uids
    
    def put(self):
        oper_args = json.loads(request.data.decode('UTF-8').replace("'", '"'))
        
        args = route_parser.parse_args()
        route_load = {'apikey': 'bd0e99aa-4519-482d-8f80-c9f07c53a090', 'format':'json', 'from': args['start_point'], 'to': args['end_point'], 'transport_types':'train'}
        
        d = get_json_response(route_api, route_load)['segments']
        # print(d)
        threads = []

        operator_colors = {'beeline': "#fdca00",
                            'tele2': "#4b4b4b",
                            'mts_rus': "#e30612",
                            'megafon': "#741982"}

        # connection_level = {'4G': 0.6,
        #                     '3G': 0.4,
        #                     '2G': 0.4,
        #                     'E': 0.3,
        #                     'unknown':0.1}

        for i in d:
            if i['thread']['number'] != args['number']:
                continue
            route_stations_load= {'apikey': 'bd0e99aa-4519-482d-8f80-c9f07c53a090', 'format':'json', 'uid': i['thread']['uid']}
            f = get_json_response(route_stations_api, route_stations_load)
            threads = []
            for j in f['stops']:
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
            data = {"type": "FeatureCollection",
                    "features": []}
            ind = 1
            thread_count = 0
            print(threads)
            frag = {"type": "Feature",
                    "id": ind,
                    "options": {"strokeWidth": 3},
                    "properties": {"balloonContent": "Содержимое балуна", "hintContent": "Текст подсказки"},
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                        ]
                    }        
            }
            for k in threads:
                frag['geometry']['coordinates'].append([k[1],k[0]])
            data["features"].append(frag)
            for j in threads:

                if thread_count == 0:
                    first_thread = j
                    thread_count += 1
                    continue
                connection = "select latitude, longtitude, operator, ntype, level from signals where longtitude between {flo} and {slo} and latitude between {fla} and {sla} and operator in ('beeline', 'mts_rus', 'tele2', 'megafon') and ntype in ('E','2G','3G','4G')"\
                .format(flo=0, slo=10000, fla=0, sla=10000)
                # .format(flo=first_thread[0], slo=j[0], fla=first_thread[1], sla=j[1])
                print(connection)
                conn = e.connect()
                query = conn.execute(connection)
                first_thread = j
                for i in query.cursor.fetchall():
                    
                    ind += 1

                    if not oper_args['tele2'] and i[2] == 'tele2':
                        continue
                    if not oper_args['mts_rus'] and i[2] == 'mts_rus':
                        continue
                    if not oper_args['beeline'] and i[2] == 'beeline':
                        continue
                    if not oper_args['megafon'] and i[2] == 'megafon':
                        continue
                    
                    connection_level = 0
                    if int(i[4]) == 99:
                        connection_level = 0
                    elif int(i[4]) > -49:
                        connection_level = 0.35
                    elif int(i[4]) > -80:
                        connection_level = 0.2
                    else:
                        connection_level = 0.05

                    
                    frag = {"type": "Feature",
                    "id": ind,
                    "options": {"fillColor": operator_colors[i[2]], "strokeColor": operator_colors[i[2]], "opacity": connection_level},
                    "properties": { "hintContent": i[2] + ' ' +  i[3] },
                    "geometry": {
                        "type": "Circle",
                        "coordinates": [
                            i[0],
                            i[1]
                        ],
                        "radius": 7000
                    }
                    }
                    data["features"].append(frag)
                
        return data

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
  return send_from_directory('./map/', path)

@app.route('/map')
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