# ОШИБКИ

class IncorrectDataRecivedError(Exception):
    # Исключение -некорректные данные получены от сокета
    def __str__(self):
        return 'Принято некорректное сообщение от удаленного компьютера'


class NonDictInputError(Exception):
    # Исключение - аргумент ф-ии не словарь
    def __str__(self):
        return 'аргумент ф-ии не словарь'


class ReqFieldMissingError(Exception):
    # Ошибка - отсутствует обязательно поле в принятом словаре
    def __init__(self, missing_field):
        self.missing_field = missing_field

    def __str__(self):
        return f'В Принятом словаре отсутствует обязательное поле {self.missing_field}'
