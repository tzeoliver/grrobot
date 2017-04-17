# -*- coding: UTF-8 -*-
import httplib2
from pprint import pprint
from random import randint
from time import strftime
from datetime import datetime, timedelta
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def helppi():
    return "/millo(i)n arg(,arg+1,...,arg+n) - Kertoo kuinka kauan on eventtiin nimeltä 'arg' grralendarissa"


def sec_to_string(sec):
    """Returns given argument (seconds) as a natural language string
    """

    months, days = divmod(sec, 2592000)
    days, hours = divmod(days, 86400)
    hours, minutes = divmod(hours, 3600)
    minutes, seconds = divmod(minutes, 60)
    seconds = seconds//60

    return "%s%s%s%s" % (month_to_natural(months), days_to_natural(days), hours_to_natural(hours), minutes_to_natural(minutes))


def month_to_natural(months):
    if months > 1:
        return "%d kuukautta " % months
    elif months == 1:
        return "%d kuukausi " % months
    else:
        return ""


def days_to_natural(days):
    if days > 1:
        return "%d päivää " % days
    elif days == 1:
        return "%d päivä " % days
    else:
        return ""


def hours_to_natural(hours):
    if hours > 1:
        return "%d tuntia " % hours
    elif hours == 1:
        return "%d tunti " % hours
    else:
        return ""


def minutes_to_natural(minutes):
    if minutes > 1:
        return "%d minuuttia " % minutes
    elif minutes == 1:
        return "%d minuutti " % minutes
    else:
        return ""


def seconds_to_natural(seconds):
    if seconds > 1:
        return "%d sekuntia " % seconds
    elif seconds == 1:
        return "%d sekuntti " % seconds
    else:
        return ""


def grraalissa():
    """Selects random response to tell what's happening in Grraali!
    """

    responses = ["Grraalissa ottamassa roppia. Tuu mukkaa!",
                 "Grraalissa hakemassa atmosfääriä. Tuu mukkaa!",
                 "Grraalissa repimässä märkää. Tuu mukkaa!",
                 "Grraalissa yhellä. Tuu mukkaa!",
                 "Grraalissa ottamassa yhden neuvoa-antavan. Tuu mukkaa!"]

    return responses[randint(0, len(responses)-1)]


def events_from_args(real_name):
    """Returns a list of arguments (events) requested by user. Returns 0 if error happens or wrong syntax used.
    """

    name = real_name.strip().lower()
    events = []

    # Pariton määrä lainausmerkkejä, väärä syntaksi
    if name.count('"') % 2 == 1:
        return 0

    while name.find('"') >= 0:
        start = name.find('"')
        end = name[start+1:].find('"')

        events.append(name[start+1:start+end+1].strip())
        name = name[:start] + name[start+end+2:]
        if len(name.strip()) == 0:
            return events
        name = name.strip()

    for item in name.split(" "):
        if len(item) != 0:
            events.append(item.strip())

    return events


def nextGraal(service):
    return millon(service, "Grraali<3")


def millon(service, ev_args):

    cal_id = "0ucntd9b0v19l3o837ui55g82k@group.calendar.google.com"  # Grralenteri<3 id
    from_time = 31  # Aika jolta etsitään seuraava tapahtuman esiintymä

    now = datetime.now()
    today = now.strftime("%Y-%m-%dT%H:%M:%S") + "+02:00"
    d = now + timedelta(from_time)
    month_from_now = d.strftime("%Y-%m-%dT%H:%M:%S") + "+02:00"

    results = []
    new_line = ""
    page_token = None
    while True:
        events = service.events().list(calendarId=cal_id, pageToken=page_token, timeMin=today,
                                       timeMax=month_from_now,singleEvents=True, orderBy="startTime").execute()
        # pprint.pprint(events)
        for eventName in events_from_args(ev_args):
            for event in events["items"]:
                try:
                    if event["summary"].lower().find(eventName) >= 0:
                        if event["summary"] == "Grraali<3":
                            event_time = event["start"]["dateTime"].split("+")
                            event_time = datetime.strptime(event_time[0], "%Y-%m-%dT%H:%M:%S")
                            end_time = event["end"]["dateTime"].split("+")
                            end_time = datetime.strptime(end_time[0], "%Y-%m-%dT%H:%M:%S")
                            if event_time < now < end_time:
                                new_line = grraalissa()
                                break
                            else:
                                new_line = "Vain " + sec_to_string((event_time - now).total_seconds()) + "Grraaliin!"
                                break
                        else:
                            event_time = event["start"]["dateTime"].split("+")
                            event_time = datetime.strptime(event_time[0], "%Y-%m-%dT%H:%M:%S")
                            new_line = sec_to_string((event_time - now).total_seconds()) + "tapahtumaan " + event["summary"]
                            break

                    # print(event['summary'] + "Start time: "+ event['start']['dateTime'])
                    # print("Vain",secToString((event_time-now).total_seconds())+event['summary'],"tapahtumaan!")
                except KeyError as e:
                    print(e)
                    pprint.pprint(event)
                    print("Ei maha mittää")
            if (eventName not in str(results).lower()) and (len(new_line) > 0):
                results.append(new_line)
        page_token = events.get("nextPageToken")
        if not page_token:
            if len(results) == 0:
                return "Hakusanoillasi ei löytynyt yhtään tapahtumaa seuraavan "+str(from_time)+"pv ajalta."
            return "\n".join(results)
