from calendar_processor import types


def tracking_keyboard_generator(message: types.Message):
    tg_id = message.from_user.id
    tracking = types.InlineKeyboardMarkup()
    tracking.row_width = 1
    tracking.add(types.InlineKeyboardButton('Начать отслеживание', callback_data=f'begin_{tg_id}'))
    return tracking


def end_tracking_keyboard_generator(callback: types.CallbackQuery):
    tg_id = callback.from_user.id
    tracking = types.InlineKeyboardMarkup()
    tracking.row_width = 1
    tracking.add(types.InlineKeyboardButton('Завершить отслеживание', callback_data=f'end_{tg_id}_{callback.message.date}'))
    return tracking
