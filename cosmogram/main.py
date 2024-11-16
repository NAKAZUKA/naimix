# from pprint import pprint
from flask import Flask, request, jsonify
import settings as conf
import kery
from flasgger import Swagger # , SwaggerView, Schema, fields


app = Flask(__name__)
swagger = Swagger(app)

'''
{
"team":[
  {
    "FIO": "Молозаев",
    "city": "Elista",
    "day": 4,
    "hour": 12,
    "lat": 44.2558,
    "lng": 46.3078,
    "min": 30,
    "month": 1,
    "year": 2002
  },
   {
    "FIO": "Катков",
    "city": "SPb",
    "day": 23,
    "hour": 9,
    "lat": 30.3141,
    "lng": 59.9386,
    "min": 10,
    "month": 3,
    "year": 2004
  },
   {
    "FIO": "Ратушняк",
    "city": "SPb",
    "day": 21,
    "hour": 9,
    "lat": 30.3141,
    "lng": 59.9386,
    "min": 10,
    "month": 3,
    "year": 2002
  },
   {
    "FIO": "Мишин",
    "city": "Ниж. Новгород",
    "day": 23,
    "hour": 1,
    "lat": 56.3287,
    "lng": 44.002,
    "min": 00,
    "month": 4,
    "year": 2002
   }
  ]
}
'''

@app.route('/anal_human', methods=['POST'])
def anal_human():
    """Анализ человека
    SVG
    ---
    consumes: application/json
    produces: application/json
    parameters:
        - name: body
          in: "body"
          type: object
          example:
            {
            'FIO': 'Ivan Ivanov',
            'day': 1, 'month': 1, 'year': 2000,
            'hour': 12, 'min': 30,
            'lng': 2.431121, 'lat': 1.411191,
            'city': '---'
            }
    responses:
        200:
          description: "200 response"
    """

    DATA = dict()
    if request.method == 'GET':
        DATA = dict(request.args)
    if request.method == 'POST':
        DATA = dict(request.get_json())
    otv = dict()
    try:
        DATA['city']
        otv = kery.anal_human(name=DATA['FIO'], year=DATA['year'], month=DATA['month'], day=DATA['day'], hour=DATA['hour'],
                                       min=DATA['min'], lng=float(DATA['lng']), lat=float(DATA['lat']), city=DATA['city'])
    except:
        otv = kery.anal_human(name=DATA['FIO'], year=DATA['year'], month=DATA['month'], day=DATA['day'], hour=DATA['hour'],
                                       min=DATA['min'], lng=float(DATA['lng']), lat=float(DATA['lat']))
    r = kery.get_SVG_human(otv)
    print(r)
    otv = dict()
    otv['SVG'] = r
    return jsonify(otv)


@app.route('/anal_two_people', methods=['POST'])
def anal_two_people():
    """Анализ совместимости двух людей
    SVG и % совместимости
    ---
    consumes: application/json
    produces: application/json
    parameters:
        - name: body
          in: "body"
          type: object
          example:
            {
            'first': {'FIO': 'Ivan Ivanov', 'day': 1, 'month': 1, 'year': 2000, 'hour': 12, 'min': 30, 'lng': 2.431121, 'lat': 1.411191, 'city': '---'},
            'second': {'FIO': 'Alex Kot', 'day': 1, 'month': 1, 'year': 2000, 'hour': 12, 'min': 30, 'lng': 3.431451, 'lat': 1.417191, 'city': '---'}
            }
    responses:
        200:
          description: "200 response"
    """

    DATA = dict()
    if request.method == 'GET':
        DATA = dict(request.args)
    if request.method == 'POST':
        DATA = dict(request.get_json())
    otvV = DATA
    DATA = DATA['first']
    try:
        DATA['city']
        otvF = kery.anal_human(name=DATA['FIO'], year=DATA['year'], month=DATA['month'], day=DATA['day'], hour=DATA['hour'],
                                       min=DATA['min'], lng=float(DATA['lng']), lat=float(DATA['lat']), city=DATA['city'])
    except:
        otvF = kery.anal_human(name=DATA['FIO'], year=DATA['year'], month=DATA['month'], day=DATA['day'], hour=DATA['hour'],
                                       min=DATA['min'], lng=float(DATA['lng']), lat=float(DATA['lat']))
    DATA = otvV['second']
    try:
        DATA['city']
        otvS = kery.anal_human(name=DATA['FIO'], year=DATA['year'], month=DATA['month'], day=DATA['day'],
                               hour=DATA['hour'],
                               min=DATA['min'], lng=float(DATA['lng']), lat=float(DATA['lat']), city=DATA['city'])
    except:
        otvS = kery.anal_human(name=DATA['FIO'], year=DATA['year'], month=DATA['month'], day=DATA['day'],
                               hour=DATA['hour'],
                               min=DATA['min'], lng=float(DATA['lng']), lat=float(DATA['lat']))
    otv = dict()
    otv['SVG'] = kery.anal_two_people(first=otvF, second=otvS)
    return jsonify(otv)


@app.route('/anal_team_and_human', methods=['POST'])
def anal_team_and_human():
    """Анализ совместимости команды и кандидата
    SVG и % совместимости
    ---
    consumes: application/json
    produces: application/json
    parameters:
        - name: body
          in: "body"
          type: object
          example:
            {
            'team': [
            {'FIO': 'Ivan Ivanov', 'day': 1, 'month': 1, 'year': 2000, 'hour': 12, 'min': 30, 'lng': 2.431121, 'lat': 1.411191, 'city': '---'},
            {'FIO': 'Alex Kot', 'day': 1, 'month': 2, 'year': 2003, 'hour': 12, 'min': 00, 'lng': 3.431451, 'lat': 1.417191, 'city': '---'},
            {'FIO': 'Alex ROT', 'day': 3, 'month': 3, 'year': 2001, 'hour': 12, 'min': 20, 'lng': 3.431451, 'lat': 1.417191, 'city': '---'}
            ],
            'human': {'FIO': 'Parry Newer', 'day': 23, 'month': 3, 'year': 2005, 'hour': 10, 'min': 17, 'lng': 3.431451, 'lat': 1.417191, 'city': '---'}
            }
    responses:
        200:
          description: "200 response"
    """

    DATA = dict()
    if request.method == 'GET':
        DATA = dict(request.args)
    if request.method == 'POST':
        DATA = dict(request.get_json())
    TEAM = DATA['team']
    HUMAN = DATA['human']
    try:
        HUMAN['city']
        HUMAN = kery.anal_human(name=HUMAN['FIO'], year=HUMAN['year'], month=HUMAN['month'], day=HUMAN['day'],
                              hour=HUMAN['hour'], min=HUMAN['min'], lng=float(HUMAN['lng']), lat=float(HUMAN['lat']), city=HUMAN['city'])
    except:
        otv = kery.anal_human(name=HUMAN['FIO'], year=HUMAN['year'], month=HUMAN['month'], day=HUMAN['day'],
                              hour=HUMAN['hour'], min=HUMAN['min'], lng=float(HUMAN['lng']), lat=float(HUMAN['lat']))

    SR = 0.0
    KOL = 0
    MAX = 0.0
    M = []
    for DATA in TEAM:
        KOL += 1
        try:
            DATA['city']
            otv = kery.anal_human(name=DATA['FIO'], year=DATA['year'], month=DATA['month'], day=DATA['day'], hour=DATA['hour'],
                                           min=DATA['min'], lng=float(DATA['lng']), lat=float(DATA['lat']), city=DATA['city'])
        except:
            otv = kery.anal_human(name=DATA['FIO'], year=DATA['year'], month=DATA['month'], day=DATA['day'], hour=DATA['hour'],
                                           min=DATA['min'], lng=float(DATA['lng']), lat=float(DATA['lat']))
        ert = kery.anal_two_people(otv, HUMAN)
        if ert["dif"] >= MAX:
            MAX = ert["dif"]
            M = ert["svg"]
        SR += ert["dif"]

    SR /= float(KOL)
    otv = dict()
    otv['dif'] = SR
    otv['svg'] = M
    return jsonify(otv)


@app.route('/anal_team', methods=['POST'])
def anal_team():
    """Анализ совместимости команды
    SVG и % совместимости
    ---
    consumes: application/json
    produces: application/json
    parameters:
        - name: body
          in: "body"
          type: object
          example:
            {
            'team': [
            {'FIO': 'Ivan Ivanov', 'day': 1, 'month': 1, 'year': 2000, 'hour': 12, 'min': 30, 'lng': 2.431121, 'lat': 1.411191, 'city': '---'},
            {'FIO': 'Alex Kot', 'day': 1, 'month': 2, 'year': 2003, 'hour': 12, 'min': 00, 'lng': 3.431451, 'lat': 1.417191, 'city': '---'},
            {'FIO': 'Alex ROT', 'day': 3, 'month': 3, 'year': 2001, 'hour': 12, 'min': 20, 'lng': 3.431451, 'lat': 1.417191, 'city': '---'},
            {'FIO': 'Parry Newer', 'day': 23, 'month': 3, 'year': 2005, 'hour': 10, 'min': 17, 'lng': 3.431451, 'lat': 1.417191, 'city': '---'}
            ]
            }
    responses:
        200:
          description: "200 response"
    """

    DATA = dict()
    if request.method == 'GET':
        DATA = dict(request.args)
    if request.method == 'POST':
        DATA = dict(request.get_json())
    TEAM = DATA['team'][1:]
    HUMAN = DATA['team'][0]
    try:
        HUMAN['city']
        HUMAN = kery.anal_human(name=HUMAN['FIO'], year=HUMAN['year'], month=HUMAN['month'], day=HUMAN['day'],
                              hour=HUMAN['hour'], min=HUMAN['min'], lng=float(HUMAN['lng']), lat=float(HUMAN['lat']), city=HUMAN['city'])
    except:
        otv = kery.anal_human(name=HUMAN['FIO'], year=HUMAN['year'], month=HUMAN['month'], day=HUMAN['day'],
                              hour=HUMAN['hour'], min=HUMAN['min'], lng=float(HUMAN['lng']), lat=float(HUMAN['lat']))

    SR = 0.0
    KOL = 0
    MAX = 0.0
    M = []
    for DATA in TEAM:
        KOL += 1
        try:
            DATA['city']
            otv = kery.anal_human(name=DATA['FIO'], year=DATA['year'], month=DATA['month'], day=DATA['day'], hour=DATA['hour'],
                                           min=DATA['min'], lng=float(DATA['lng']), lat=float(DATA['lat']), city=DATA['city'])
        except:
            otv = kery.anal_human(name=DATA['FIO'], year=DATA['year'], month=DATA['month'], day=DATA['day'], hour=DATA['hour'],
                                           min=DATA['min'], lng=float(DATA['lng']), lat=float(DATA['lat']))
        ert = kery.anal_two_people(otv, HUMAN)
        if ert["dif"] >= MAX:
            MAX = ert["dif"]
            M = ert["svg"]
        SR += ert["dif"]

    SR /= float(KOL)
    otv = dict()
    otv['dif'] = SR
    otv['svg'] = M
    return jsonify(otv)


if __name__ == '__main__':
    app.run(debug=True, host=conf.GET("host"), port=conf.GET("port"))
