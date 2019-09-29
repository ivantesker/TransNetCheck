import json
import random
from flask import Flask, request, render_template, send_from_directory
from flask_restful import Resource, Api, reqparse, abort
from flask_cors import CORS
from sqlalchemy import create_engine
from json import dumps
import time
import math
import requests

e = create_engine('sqlite:///db/tnc.db')
conn = e.connect()
for x in range(10000):
    
    command = "INSERT INTO signals(latitude, longtitude, level, date, operator, ntype) VALUES({latitude}, {longtitude}, {level}, {date}, '{operator}', '{ntype}')"\
                .format(latitude=(random.random() * 180 - 90),longtitude=str(random.random() * 360 - 180), date=int(time.time()),level='100', operator='beeline', ntype='3G')
    query = conn.execute(command)


