import requests
import json
import yaml

def myConvertTime(x):
    y = x
    if (int(y[:2]) - 2) > 12:
        y = str(int(y[:2]) - 14) + y[2:]
        y = y + 'pm'
    elif (int(y[:2]) - 2) == 12:
        y = str(int(y[:2]) - 2) + y[2:]
        y = y + 'pm'
    else:
        y = str(int(y[:2]) - 2) + y[2:]
        y = y + 'am'

    return y

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
    data2 = data2['results'][0]

    #complain if the address is an empty string
    if data2['address'] == '':
        print("Error. The address value for search " + str(id) + " is an empty string!")
        emptyIDs += 1
    
    output.append({
        "id": data2['address'],
        "day": data2['startDate']['date'].replace('2022-0', ''),
        "title": data2['title'],
        "location": data2['location'] + ' ' + data2['room'],
        "time": myConvertTime(data2['startDate']['time']) + '-' + myConvertTime(data2['endDate']['time'])
    })

print(str(emptyIDs), 'empty IDs')
result = open("output.yaml", "w")
result.write(yaml.dump(output))
result.close()

