from aiogram.filters.callback_data import CallbackData


class ButtonCallback(CallbackData, prefix='btn'):
    cb_prefix: str
    cb_id: int