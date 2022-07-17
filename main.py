import requests
import json
import yaml
from datetime import datetime
import pytz

# this is an inelegant solution and assumes that every item is
# already in chicago time.
def myConvertTime(z):
    # convert from chicago to PDTs
    date_string = z['date'] + ' ' + z['time']
    dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    tz = pytz.timezone(z['tz'])
    dt2 = tz.localize(dt)
    dt3 = dt2.astimezone(pytz.timezone('America/Los_Angeles'))

    res = datetime.strftime(dt3, "%H:%M:%S%p")
    #print(res)
    return res




r = requests.get('https://indico.fnal.gov/export/timetable/22303.json')
data = json.loads(r.text)

data = data['results']['22303']

#Navigate the layers of the nested dicts in order to reach the session IDs
setOfIds = set()
for day in data:
    for sN in data[day]:
        setOfIds.add(data[day][sN]['sessionId'])

#trim the nulls
#print(setOfIds)
setOfIds.remove(None)
len(setOfIds)

emptyIDs = 0
output = []
for id in setOfIds:
    url = 'https://indico.fnal.gov/export/event/22303/session/' + str(id) + '.json'
    r2 = requests.get(url)
    data2 = json.loads(r2.text)
    for x in data2['results']:

        #complain if the address is an empty string
        #if x['address'] == '':
            #print("Error. The address value for search " + str(id) + " is an empty string!")
            #emptyIDs += 1

        
        #print(x['startDate'])
        output.append({
            "id": x['address'],
            "day": x['startDate']['date'].replace('2022-0', ''),
            "title": x['title'],
            "location": x['location'] + ' ' + x['room'],
            "time": myConvertTime(x['startDate']) + '-' + myConvertTime(x['endDate'])
        })

#print(str(emptyIDs), 'empty IDs')
result = open("output.yaml", "w")
result.write(yaml.dump(output))
result.close()