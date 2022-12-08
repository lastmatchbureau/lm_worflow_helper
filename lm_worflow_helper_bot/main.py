from calendar_processor import \
    CalendarProcessor, \
    types, \
    ADMIN_USERS, \
    bot, \
    calendars_folder_path, \
    os, \
    logger, \
    ADMIN_TG_ID, \
    datetime
from keyboards import tracking_keyboard_generator, end_tracking_keyboard_generator

cp = CalendarProcessor()


def admin_only(func):
    def wrapped(message: types.Message):
        if message.from_user.username in ADMIN_USERS:
            func(message)
        else:
            bot.send_message(message.chat.id, 'Команда доступна только админам!')

    return wrapped


def parse_tracking_message(callback: types.CallbackQuery):
    unix_start_time = int(callback.data.split("_")[2])
    start_t = datetime.datetime.fromtimestamp(unix_start_time) + datetime.timedelta(hours=3)
    end_t = datetime.datetime.fromtimestamp(callback.message.date) + datetime.timedelta(hours=3)
    logger.debug(f'Start time for {callback.from_user.username}:' + datetime.datetime.fromtimestamp(
        callback.message.date).time().__str__() +
                 f'\nEnd time for {callback.from_user.username}:' + datetime.datetime.fromtimestamp(
        callback.message.date).time().__str__())
    return f"Отсчёт времени завершен!\n" \
           f"lastmatch © @{callback.from_user.username}\n" \
           f"[🕦 {start_t.strftime('%H:%M')} — {end_t.strftime('%H:%M')}]\n" \
           f"[🕦 Прошло — {(end_t - start_t)}]"


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.chat.id, "Отправь файл календаря с расширением .ics, "
                                      "например из https://calendar.google.com/")


@bot.message_handler(commands=['get_schedule'])
def get_schedule(message: types.Message):
    schedules = "Расписание:\n"
    for root, dirs, files in os.walk(calendars_folder_path):
        for file in files:
            schedules += cp.parse_calendar(os.path.join(root, file))
    if schedules != "Расписание:\n":
        bot.send_message(message.chat.id, schedules)
    else:
        bot.send_message(message.chat.id, 'Календарей не найдено(')


@bot.message_handler(content_types=['document'])
def process_report(message: types.Message):
    calendar_path = cp.download_calendar(message)
    if calendar_path is not None:
        bot.send_message(message.chat.id, 'Календарь сохранен!')
        if calendar_path: logger.debug(str(calendar_path) + " -- CALENDAR SAVED!")


@bot.message_handler(commands=['track_time'])
def track_time(message: types.Message):
    bot.send_message(message.chat.id, "Трекинг времени", reply_markup=tracking_keyboard_generator(message))


@bot.message_handler(commands=['delete'])
@admin_only
def delete_calendars(message: types.Message):
    if message.from_user.username in ADMIN_USERS:
        for root, dirs, files in os.walk(calendars_folder_path):
            for file in files:
                os.remove(os.path.join(root, file))
                logger.debug(os.path.join(root, file) + "-- DELETED!")
        bot.send_message(message.chat.id, 'Календари удалены!')


@bot.callback_query_handler(lambda callback: 'begin' in callback.data)
def begin_tracking(callback: types.CallbackQuery):
    bot.reply_to(callback.message, 'Время пошло!\nЧтобы завершить отсчёт времени жми кнопку:',
                 reply_markup=end_tracking_keyboard_generator(callback))
    return True


@bot.callback_query_handler(lambda callback: 'end' in callback.data and str(callback.from_user.id) in callback.data)
def end_tracking(callback: types.CallbackQuery):
    bot.send_message(callback.from_user.id, parse_tracking_message(callback))
    return True


while True:
    try:
        bot.polling()
    except Exception as e:
        logger.debug("ERROR! " + str(e))
        bot.send_message(ADMIN_TG_ID, str(e))
        bot.send_document(ADMIN_TG_ID, open('debug.log', 'rb'))
