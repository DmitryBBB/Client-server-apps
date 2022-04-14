# Декоратор

# Метод определения модуля(источника запуска)
# .find возвращает индекс первого вхождения запрашиваемой строки
import inspect
import logging
import sys
import traceback


if sys.argv[0].find('client3.py') == -1:
    # Если не клиент то сервер
    LOGGER = logging.getLogger('server')
else:
    # Не сервер значит клиент
    LOGGER = logging.getLogger('client')


# Декоратор (В декораторе @log реализована фиксация
# функции, из которой была вызвана декорированная)

def log(func_log):
    def log_saver(*args, **kwargs):
        ret = func_log(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func_log.__name__} с параметрами {args}, {kwargs} '
                     f'Вызов из модуля {func_log.__module__} '
                     f'Вызов из ф-ции {traceback.format_stack()[0].strip().split()[-1]} '
                     f'Файл запуска: {inspect.getframeinfo(inspect.stack()[1][0])}')
        # caller = getframeinfo(stack()[1][0])

        return ret
    return log_saver
