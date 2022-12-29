"""Кастомные исключения."""


import logging


class WrongValuesError(Exception):
    def __init__(self):
        self.__msg = 'Данные не валидны!'

    def __call__(self, *args, **kwargs):
        logging.error(self.__msg)


class WrongSaveError(Exception):
    pass
