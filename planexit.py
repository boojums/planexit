import json
from datetime import timedelta, datetime

import requests


request_template = ('http://reisapi.ruter.no/Travel/GetTravels?'
                    'fromPlace={}&toPlace={}&isafter=true'
                    'maxwalkingminutes=5&'
                    'walkingfactor={}')

jernbanetorget = 3010011
jernbane_oslos = 3010013
oesthorn = 3012240
skibakken = 3012290
majorstuentbane = 3010200
havnabakken = 3012245

TRIP_PAIRS = [{'name': 'tbane', 'from': jernbanetorget, 'to': oesthorn,
               'extra_time': 10, 'walkingfactor': 100},
              {'name': '54', 'from': jernbane_oslos, 'to': skibakken,
               'extra_time': 6, 'walkingfactor': 100},
              {'name': '25major', 'from': jernbanetorget, 'to': havnabakken,
               'extra_time': 2, 'walkingfactor': 999}]

results = []
for trip in TRIP_PAIRS:
    r = requests.get(request_template.format(trip['from'], trip['to'], trip['walkingfactor']))
    content = json.loads(r.content)
    next_trip = content['TravelProposals'][0]
    start = datetime.strptime(next_trip['DepartureTime'], '%Y-%m-%dT%H:%M:%S')
    stop = datetime.strptime(next_trip['ArrivalTime'], '%Y-%m-%dT%H:%M:%S')
    real_stop = stop + timedelta(minutes=trip['extra_time'])
    result = {'name': trip['name'], 'start': start, 'stop': real_stop}
    results.append(result)

results.sort(key=lambda x: x['stop'])
for result in results:
    print '{name:>10}: {start:%H:%M} - {stop:%H:%M}'.format(**result)

