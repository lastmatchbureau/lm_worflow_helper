import pathlib
from lm_worflow_helper_bot import codecs, ics, bot, datetime, os
import pytz
utc=pytz.timezone('Europe/Moscow')


def event_in_7_days_from_now(event: ics.Event):
    datetime_now = datetime.datetime.now().replace(tzinfo=utc)
    begin_time = event.begin.datetime.replace(tzinfo=utc)
    end_time = event.end.datetime.replace(tzinfo=utc)
    return end_time > datetime_now and begin_time < (datetime_now + datetime.timedelta(days=7))


def parse_event(event: ics.Event):
    return f"[{event.begin.datetime.replace(tzinfo=utc).strftime('%d.%m')} — 🕦 {event.begin.datetime.replace(tzinfo=utc).strftime('%H:%M')} — {event.end.datetime.replace(tzinfo=utc).strftime('%H:%M')}]\n"


def parse_username(calendar_path: str):
    return calendar_path.replace('_calendar.ics', '').replace('..\\calendars\\', '')


def parse_calendar(calendar_path: str):
    print(calendar_path)
    with codecs.open(calendar_path, 'r', 'utf-8') as f:
        c = ics.Calendar(str(f.read()))
        username = parse_username(calendar_path)
        no_time = True
        parsed_calendar = f"lastmatch © @{username}\n"
        for event in c.events:
            print(event)
            if "lastmatch" in str(event.name).lower():
                if event_in_7_days_from_now(event):
                    parsed_calendar += parse_event(event)
                    no_time = False
        if no_time:
            return f"В ближайшую неделю {username} занят.\n\n"
        else:
            return parsed_calendar


def download_calendar(message):
    obj = bot.get_file(message.document.file_id)
    obj = bot.download_file(obj.file_path)
    calendar_path = f'../calendars/{message.chat.username}_calendar.ics'
    with open(calendar_path, 'w') as f:
        try:
            f.write(str(obj.decode(encoding='utf-8')))
            return calendar_path
        except UnicodeDecodeError as e:
            print(e)
            bot.send_message(message.chat.id, "Ошибка при сохранении календаря.\n"
                                              "Пожалуйста, убедитесь в том, что файл не был поврежден!\n"
                                              "Если нужна помощь, пиши @Olejius")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Отправь файл календаря с расширением .ics, "
                                      "например из https://calendar.google.com/")


@bot.message_handler(commands=['get_schedule'])
def get_schedule(message):
    schedules = "Расписание:\n"
    for root, dirs, files in os.walk(pathlib.Path('..\calendars')):
        for file in files:
            schedules += parse_calendar(os.path.join(root, file))
    if schedules != "Расписание:\n":
        bot.send_message(message.chat.id, schedules)
    else:
        bot.send_message(message.chat.id, 'Календарей не найдено(')


@bot.message_handler(content_types=['document'])
def process_report(message):
    calendar_path = download_calendar(message)
    bot.send_message(message.chat.id, 'Календарь сохранен!')


@bot.message_handler(commands=['delete'])
def delete_calendars(message):
    for root, dirs, files in os.walk('../calendars'):
        print(root, files)
        for file in files:
            os.remove(os.path.join(root, file))
    bot.send_message(message.chat.id, 'Календари удалены!')


while True:
    try:
        bot.polling()
    except Exception as e:
        bot.send_message(231584958, e.args)
