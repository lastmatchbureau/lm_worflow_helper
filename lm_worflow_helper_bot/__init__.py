import os
import pathlib
from telebot import TeleBot, types
from loguru import logger
import sqlite3

logger.add('debug.log', format="{time} {level} {message}", level="DEBUG", rotation='10 KB', compression='zip')

calendars_folder_path = os.path.join(pathlib.Path(__name__).parent, 'calendars')

ADMIN_USERS = ['Killmarnok', 'ar_k_s', 'borisshikhman']

try:
    os.mkdir(calendars_folder_path)
    logger.debug(f"Calendars dir created at: {calendars_folder_path}!")
except:
    logger.debug("Calendars dir existed!")


os.environ['TG_API_BOT'] = '5851418035:AAGJohY7SJAFz0ixwca8GdklzqlDoX0p0yA'
bot = TeleBot(os.environ['TG_API_BOT'])
logger.debug("TeleBot is online!\n")

ADMIN_TG_ID = 231584958