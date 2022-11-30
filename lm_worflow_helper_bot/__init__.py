import os
import pathlib

from telebot import TeleBot
import ics
import codecs
import datetime

calendars_folder_path = os.path.join(pathlib.Path(__name__), 'calendars')
try:
    os.mkdir(calendars_folder_path)
    print(f"Calendars dir created at: {calendars_folder_path}!")
except:
    print("Calendars dir existed!")


os.environ['TG_API_BOT'] = '5825095498:AAFUbxz_7cexnzCvzJl-F3-3J7JF2ARKSdA'
bot = TeleBot(os.environ['TG_API_BOT'])
print("TeleBot is online!\n")