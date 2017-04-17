# -*- coding: UTF-8 -*-
from pprint import pprint
from random import randint
from time import strftime
from datetime import datetime, timedelta


def helppi():
    return "Käyttö: /oispa kaljaa/kalijaa/olutta."


def if_only_beer():
    """Olutta myydään kaupoissa klo 9.00 - 21.00 välisenä aikana.
    Tämän jälkeen sitä myydään vielä baarissa ~klo 3.30 asti.
    """
    this_hour = datetime.now().hour
    this_minute = datetime.now().minute

    if 9 <= this_hour < 21:
        return "Kaupastahan sitä saa!"
    elif (this_hour >= 21) or (this_hour < 4):
        if (this_hour < 4) and (this_minute >= 30):
            return "Valomerkki tais tulla jo. Mee kotia!"
        return "Baaristahan sitä saa!"
    elif 4 <= this_hour < 9:
        return "Ei saa ostettua mistään :("


def if_only_liquor():
    """Viinaa myydään Alkoissa arkisin klo 9.00 - 20.00 ja
    lauantaisin klo 9.00 - 18.00 välisenä aikana.
    Sunnuntaisin Alko on suljettu.
    Tämän jälkeen sitä myydään vielä baarissa ~klo 3.30 asti.
    """
    weekday = datetime.now().weekday()
    this_hour = datetime.now().hour
    this_minute = datetime.now().minute

    # TODO Redo this with check to Alko websites for opening hours

    if weekday <= 4:
        # ma-pe
        if 9 <= this_hour < 20:
            return "Alkostahan sitä saa!"
        elif (this_hour >= 20) or (this_hour < 4):
            if (this_hour < 4) and (this_minute >= 30):
                return "Valomerkki tais tulla jo. Mee kotia!"
            return "Baaristahan sitä saa!"
        elif 4 <= this_hour < 9:
            return "Ei saa ostettua mistään :("
    elif weekday == 5:
        # lauantai
        if 9 <= this_hour < 18:
            return "Alkostahan sitä saa!"
        elif (this_hour >= 18) or (this_hour < 4):
            if (this_hour < 4) and (this_minute >= 30):
                return "Valomerkki tais tulla jo. Mee kotia!"
            return "Baaristahan sitä saa!"
        elif 4 <= this_hour < 9:
            return "Ei saa ostettua mistään :("
    elif weekday == 6:
        # sunnuntai
        if 9 <= this_hour < 4:
            if (this_hour < 4) and (this_minute >= 30):
                return "Valomerkki tais tulla jo. Mee kotia!"
            return "Baaristahan sitä saa!"
        elif 4 <= this_hour < 9:
            return "Ei saa ostettua mistään :("
