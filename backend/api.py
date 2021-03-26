from flask import Flask, make_response, request
from flask_restful import reqparse, Api, Resource
from flask_cors import CORS
import json
import pandas as pd
from backend.db import db_connection, search_streets, get_days, streets_paged
from datetime import date, datetime

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('term')

HEADERS = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*'}

conn = db_connection()


class SearchStreets(Resource):
    def get(self):
        search_term = request.args.get('q')
        streets = search_streets(conn, str(search_term))
        return output_json(streets, 200)


class Street(Resource):
    def get(self, city, street):
        bindays = get_days(conn, city, street)
        return output_json(bindays, 200)


class StreetsPaged(Resource):
    def get(self, city, page):
        bindays = streets_paged(conn, city, int(page))
        code = 200
        return output_json(bindays, code)


def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    if isinstance(data, pd.DataFrame):
        jsondata = data.to_json(index=False, orient='table')
    else:
        jsondata = json.dumps(data, default=json_serial)
    resp = make_response(jsondata, code)
    resp.headers.extend(headers or {})
    return resp


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


##
## Actually setup the Api resource routing here
##
api.add_resource(SearchStreets, '/streets')
api.add_resource(Street, '/street/<city>/<street>')
api.add_resource(StreetsPaged, '/streetspaged/<city>/<page>')

if __name__ == '__main__':
    app.run(debug=False, host='192.168.1.28')
