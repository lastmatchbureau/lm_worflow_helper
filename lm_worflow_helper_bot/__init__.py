import os
import pathlib
import pytz
from telebot import TeleBot, types
import ics
import codecs
import datetime
from loguru import logger

logger.add('debug.log', format="{time} {level} {message}", level="DEBUG", rotation='10 KB', compression='zip')

calendars_folder_path = os.path.join(pathlib.Path(__name__).parent, 'calendars')

ADMIN_USERS = ['Killmarnok', 'ar_k_s', 'borisshikhman']

try:
    os.mkdir(calendars_folder_path)
    logger.debug(f"Calendars dir created at: {calendars_folder_path}!")
except:
    logger.debug("Calendars dir existed!")


os.environ['TG_API_BOT'] = '5825095498:AAFUbxz_7cexnzCvzJl-F3-3J7JF2ARKSdA'
bot = TeleBot(os.environ['TG_API_BOT'])
logger.debug("TeleBot is online!\n")