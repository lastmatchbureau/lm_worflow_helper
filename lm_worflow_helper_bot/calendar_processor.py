import datetime, ics, codecs, telebot.types as types, pathlib, pytz
from __init__ import bot, ADMIN_TG_ID, calendars_folder_path, os, calendars_folder_path, logger, types, ADMIN_USERS

utc = pytz.timezone('Europe/Moscow')


class CalendarProcessor:
    plus_hours = datetime.timedelta(hours=3)

    def event_in_7_days_from_now(self, event: ics.Event):
        datetime_now = datetime.datetime.now().replace(tzinfo=utc)
        begin_time = event.begin.datetime + self.plus_hours
        end_time = event.end.datetime + self.plus_hours
        return end_time > datetime_now and begin_time < (datetime_now + datetime.timedelta(days=7))

    def parse_event(self, event: ics.Event):
        e_begin_datetime = event.begin.datetime + self.plus_hours
        e_end_datetime = event.end.datetime + self.plus_hours
        return f"[{e_begin_datetime.strftime('%d.%m')} — 🕦 {e_begin_datetime.strftime('%H:%M')} — {e_end_datetime.strftime('%H:%M')}]\n"

    @staticmethod
    def parse_username(calendar_path: str):
        return calendar_path.replace('_calendar.ics', '').replace('./calendars/', '').replace('.\\calendars\\', '')

    def parse_calendar(self, calendar_path: str):
        with codecs.open(calendar_path, 'r', 'utf-8') as f:
            c = ics.Calendar(str(f.read()))
            username = self.parse_username(calendar_path)
            no_time = True
            parsed_calendar = f"lastmatch © @{username}\n"
            for event in sorted(c.events, key=lambda event: event.begin.datetime):
                if "lastmatch" in str(event.name).lower():
                    if self.event_in_7_days_from_now(event):
                        parsed_calendar += self.parse_event(event)
                        no_time = False
            if no_time:
                return f"В ближайшую неделю {username} занят.\n\n"
            else:
                return parsed_calendar

    @staticmethod
    def save_calendar_to_file(calendar_path, obj: bytes, message: types.Message):
        with open(calendar_path, 'w') as f:
            try:
                f.write(str(obj.decode(encoding='utf-8')))
                logger.debug(f"Calendar from {message.from_user.username} saved at: {calendar_path}")
                return calendar_path
            except UnicodeDecodeError as e:
                bot.send_message(ADMIN_TG_ID, e.args)
                bot.send_message(message.chat.id, "Ошибка при сохранении календаря.\n"
                                                  "Пожалуйста, убедитесь в том, что файл не был поврежден!\n"
                                                  "Если нужна помощь, пиши @Olejius")

    @staticmethod
    def download_calendar(message: types.Message):
        obj = bot.get_file(message.document.file_id)
        if '.ics' == obj.file_path[-4::]:
            obj = bot.download_file(obj.file_path)
            calendar_file_path = pathlib.Path(f'{calendars_folder_path}/{message.from_user.username}_calendar.ics')
            CalendarProcessor.save_calendar_to_file(calendar_file_path, obj, message)
            return calendar_file_path
        else:
            return None
