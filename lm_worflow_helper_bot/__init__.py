import os
from telebot import TeleBot
import ics
import codecs
import datetime
try:
    os.mkdir('../calendars')
    print("Calendars dir created!")
except:
    print("Calendars dir existed!")


os.environ['TG_API_BOT'] = '5825095498:AAFUbxz_7cexnzCvzJl-F3-3J7JF2ARKSdA'
bot = TeleBot(os.environ['TG_API_BOT'])
print("TeleBot is online!\n")