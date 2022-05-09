import logging

logger = logging.getLogger('server_dist')


# Дескриптор для описания порта
class Port:
    def __set__(self, instance, value):
        # value - 7777
        if not 1023 < value < 65536:
            logger.critical(
                f'Попытка запуска  ервера с указанием неподходящего порта {value},'
                f' допустимы значения от 1024 до 65536')
            exit(1)
        # Если порт прошел проверку добавляем его в список атрибутов экземпляра
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        # owner - <class '__main__.Server'>
        # name - port
        self.name = name
