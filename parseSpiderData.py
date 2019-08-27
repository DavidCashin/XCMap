import json
import pprint
from datetime import datetime, date, timedelta

year = 2019

with open ('sidearm/races.json') as f:
    races_json = json.load(f)

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
    weekends[weekend_index] = {"sunday": dt, "race": []} # initialize empty race array for later
    dt += timedelta(days = 7)
    weekend_index += 1

# this nested loop is inefficient, but it works for now and is generic enough
for race in races_json:
    date_obj = datetime.strptime(race["date"], "%Y-%m-%d").date() # assume preformated date YYYY-MM-DD
    race["date"] = date_obj
    for i in weekends:
        days_diff = (weekends[i]["sunday"] - date_obj).days
        if days_diff < 7 and days_diff >=0:
            weekends[i]["race"].append(race)

pprint.PrettyPrinter(indent=4).pprint(weekends)