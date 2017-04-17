# -*- coding: UTF-8 -*-
import os
import sys
import time
import httplib2
import threading
import random
from pprint import pprint
import telepot
import logging
import grralendar
import grrtilastot
import oispaolutta
from time import strftime
from datetime import datetime, timedelta
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

"""
$ python3.5 grrobot.py <token> <service_account_name>

Usage:
/help - Gives help
/grraali - Tells how long to next Graali
/millo(i)n arg(,arg+1,...,argn) - Tells how long to next event named 'arg' in the grralendar
/roll xdy - Rolls x number of y dice and returns results
/di - Tells who are Master of Science of the Grr<3!
/oispa kaljaa/kalijaa/olutta - Tells where you can get beer!
/kirjaa - Log your drinking!
"""

message_with_inline_keyboard = None
groupId = 0


def roll_dice(num, die):
    num = int(num)
    die = int(die)
    s = []
    i = 0
    while i < num:
        s.append(random.randint(1, die))
        i += 1
    return s


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print("Chat: ", content_type, chat_type, chat_id)

    pprint(msg)

    # print("Keneltä: ",msg["from"]["first_name"] , "ID", msg["from"]["id"])

    if content_type != "text":
        return

    command = msg["text"].lower()
    command = command.split(" ")

    if command[0] in ["/help", "/start"]:
        helppi = "Grrobotin yleiset komennot:\n" +\
                "Milloin seuraava Grraali<3: /grraali\n" +\
                "Milloin seuraava tapahtuma x: /milloin x\n" +\
                "Kirjaa oluesi tietokantaan: /kirjaa 'koko'\n" +\
                "Valittele oluen tarvetta: /oispa kalijaa\n" +\
                "Heitä noppaa: /roll xdy\n" +\
                "Useissa komennoissa on oma helppi joka toimii /'komento' help -rimpsulla."

        bot.sendMessage(msg["from"]["id"], helppi)

    elif command[0] == "/grraali":
        bot.sendMessage(chat_id, grralendar.nextGraal(service))

    elif command[0] in ["/millon", "/milloin"]:
        if len(command) >= 2:
            bot.sendMessage(chat_id, grralendar.millon(service, " ".join(command[1:])))
        else:
            bot.sendMessage(msg["from"]["id"], grralendar.helppi())

    # Hassuttelu hupsuttelu komennot, hihi!

    elif command[0] == "/kirjaa":
        if len(command) >= 2:
            return_id, return_message = grrtilastot.beer_records(command[1:], msg)
            bot.sendMessage(return_id, return_message)
        else:
            bot.sendMessage(msg["from"]["id"], grrtilastot.helppi())

    elif command[0] == "/oispa":
        if len(command) >= 2:
            if command[1] in ["kaljaa", "kalijaa", "olutta", "mallasjuomaa"]:
                bot.sendMessage(chat_id, oispaolutta.if_only_beer())
            # elif command[1] in ["viinaa","viskiä"]:
            #    bot.sendMessage(chat_id, oispaolutta.ifOnlyLiquor())
        else:
            bot.sendMessage(msg["from"]["id"], oispaolutta.helppi())

    elif command[0] == "/roll":
        if len(command) >= 2:
            try:
                dice = command[1].split("d")

                if (int(dice[0]) > 100) or (int(dice[1]) > 100):
                    return
                result = roll_dice(dice[0], dice[1])

                answer = "%s = %d" % (str(result), sum(result))
                bot.sendMessage(chat_id, answer)
            except Exception as e:
                print e
                helppi = "Heitä noppaa '/roll xdy', jossa x on noppien määrä ja y nopan sivujen määrä."
                bot.sendMessage(msg["from"]["id"], helppi)
        else:
            helppi = "Heitä noppaa '/roll xdy', jossa x on noppien määrä ja y nopan sivujen määrä."
            bot.sendMessage(msg["from"]["id"], helppi)

TOKEN = sys.argv[1]  # get token from command-line
service_account_name = sys.argv[2]

"""Set calendar service"""
scopes = ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/calendar"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("keyfile.json", scopes=scopes)
# Delegated credentials
http_auth = credentials.authorize(httplib2.Http())
service = build(serviceName="calendar", version="v3", http=http_auth)

"""Start Bot"""
bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)

bot.message_loop({"chat": on_chat_message})
print("Listening ...")

# Keep the program running.
while 1:
    time.sleep(10)
