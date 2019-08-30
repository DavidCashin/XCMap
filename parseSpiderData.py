import json
import pprint
import time
import dateparser
from datetime import datetime, date, timedelta
import requests

with open('data.txt', 'r') as file:
    key = file.read().replace('\n', '').replace('\r', '')

year = 2019

with open('sidearm/sidearm_common.json') as f:
    races_json = json.load(f)
with open('sidearm/dalhousie_stfx.json') as f:
    races_json.extend(json.load(f))
with open('sidearm/geegees.json') as f:
    races_json.extend(json.load(f))
with open('sidearm/guelph.json') as f:
    races_json.extend(json.load(f))

# we'll bin each race into a 'weekend of the month'. assumptions are the year and that all races occur around a weekend
# we need to figure out date ranges where if a date is in that range, it belongs to a certain weekend
# example: sept 21 is the race. thats a saturday. Any date between monday (the 16th) and Sunday (22nd) should get pinned to that weekend

# we can find each weekend of the year by finding the first weekend of the year and adding 7 days each time
# TODO: this could be genericized for any given date range, instead of jan 1, YEAR to dec 31, YEAR
weekends = {}
# January 1st of the given year
dt = date(year, 1, 1)
# First Sunday of the given year       
dt += timedelta(days = 6 - dt.weekday())  
weekend_index = 0
while dt.year == year:
    # the timedelta objects being stored here can be compared against other td objects to find deltas
    weekends[weekend_index] = {"sunday": dt.strftime("%Y-%m-%d"), "race": []} # initialize empty race array for later
    dt += timedelta(days = 7)
    weekend_index += 1

# this nested loop is inefficient, but it works for now and is generic enough
for race in races_json:
    date_obj = datetime.strptime(race["date"].split(' ')[0], "%Y-%m-%d").date() # assume preformated date YYYY-MM-DD 00:00:00 (dateparser.parse default)
    race["date"] = date_obj.strftime("%Y-%m-%d")
    for i in weekends:
        days_diff = (dateparser.parse(weekends[i]["sunday"]).date() - date_obj).days
        if days_diff < 7 and days_diff >=0:
            # preload lat/lon - run out of quota quickly if we geocode client side each time the webapp loads
            url ="https://maps.googleapis.com/maps/api/geocode/json?address=" + race["travellingSchool"] + ",+Canada&key=" + key
            # time.sleep(0.1) # stay within api quota
            geocoding = requests.get(url=url).json()
            coords = geocoding["results"][0]["geometry"]["location"]
            race["travellingSchoolCoords"] = {"lat": coords["lat"], "lng": coords["lng"]}
            # time.sleep(0.1)
            url ="https://maps.googleapis.com/maps/api/geocode/json?address=" + race["raceLocation"] + ",+Canada&key=" + key
            geocoding = requests.get(url=url).json()
            coords = geocoding["results"][0]["geometry"]["location"]
            race["raceLocationCoords"] = {"lat": coords["lat"], "lng": coords["lng"]}

            weekends[i]["race"].append(race)
            
with open('weekendRaceSchedules.json', 'w') as fp:
    json.dump(weekends, fp, indent=4)