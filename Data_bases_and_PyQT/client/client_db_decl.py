"""БАЗА ДАННЫХ СЕРВЕРА"""
import datetime
import os

from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class ClientDatabase:
    Base = declarative_base()

    # Класс отображение таблицы известных пользователей
    class KnowUsers(Base):
        __tablename__ = 'know_users'
        id = Column(Integer, primary_key=True)
        username = Column(String)

        def __init__(self, user):
            self.id = None
            self.username = user

    # Класс отоброжение таблицы истории сообщений
    class MessageStat(Base):
        __tablename__ = 'message_history'
        id = Column(Integer, primary_key=True)
        contact = Column(String)
        direction = Column(String)
        message = Column(Text)
        date = Column(DateTime)

        def __init__(self, contact, direction, message):
            self.id = None
            self.contact = contact
            self.direction = direction
            self.message = message
            self.date = datetime.datetime.now()

    # Класс отображение списка контактов
    class Contacts(Base):
        __tablename__ = 'contacts'
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)

        def __init__(self, contact):
            self.id = None
            self.name = contact

    # Конструктор класса
    def __init__(self, name):
        # Создаём движок базы данных, поскольку разрешено несколько
        # клиентов одновременно,
        # то каждый должен иметь свою БД.
        # Поскольку клиент мультипоточный,
        # то необходимо отключить проверки на подключения с разных потоков,
        # иначе sqlite3.ProgrammingError
        path = os.path.dirname(os.path.realpath(__file__))
        filename = f'client_{name}.db3'
        self.database_engine = create_engine(f'sqlite:///{os.path.join(path, filename)}',
                                             echo=False,
                                             pool_recycle=7200,
                                             connect_args={'check_same_thread': False})

        # Создаем таблицы
        self.Base.metadata.create_all(self.database_engine)

        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        # Необходимо очистить таблицу контактов, т.к. при запуске они подгружаются с сервера
        self.session.query(self.Contacts).delete()
        self.session.commit()

    def add_contact(self, contact):
        """ Метод добавляющий контакт в базу данных. """
        if not self.session.query(
                self.Contacts).filter_by(
                name=contact).count():
            contact_row = self.Contacts(contact)
            self.session.add(contact_row)
            self.session.commit()

    def contacts_clear(self):
        """ Метод, очищающий таблицу со списком контактов. """
        self.session.query(self.Contacts).delete()
        self.session.commit()

    def del_contact(self, contact):
        """ Метод, удаляющий определённый контакт. """
        self.session.query(self.Contacts).filter_by(name=contact).delete()
        self.session.commit()

    def add_users(self, users_list):
        """ Метод, заполняющий таблицу известных пользователей. """
        self.session.query(self.KnowUsers).delete()
        for user in users_list:
            user_row = self.KnowUsers(user)
            self.session.add(user_row)
        self.session.commit()

    def save_message(self, contact, direction, message):
        """ Метод, сохраняющий сообщение в базе данных. """
        message_row = self.MessageStat(contact, direction, message)
        self.session.add(message_row)
        self.session.commit()

    def get_contacts(self):
        """ Метод, возвращающий список всех контактов. """
        return [contact[0]
                for contact in self.session.query(self.Contacts.name).all()]

    def get_users(self):
        """ Метод возвращающий список всех известных пользователей. """
        return [user[0]
                for user in self.session.query(self.KnowUsers.username).all()]

    def check_user(self, user):
        """ Метод, проверяющий существует ли пользователь. """
        if self.session.query(
                self.KnowUsers).filter_by(
                username=user).count():
            return True
        else:
            return False

    def check_contact(self, contact):
        """ Метод, проверяющий существует ли контакт. """
        if self.session.query(self.Contacts).filter_by(name=contact).count():
            return True
        else:
            return False

    def get_history(self, contact):
        """ Метод, возвращающий историю сообщений с определённым пользователем. """
        query = self.session.query(
            self.MessageStat).filter_by(
            contact=contact)
        return [(history_row.contact,
                 history_row.direction,
                 history_row.message,
                 history_row.date) for history_row in query.all()]



# if __name__ == '__main__':
#     test_db = ClientDatabase('test1')
#     for i in ['test3', 'test4', 'test5']:
#         test_db.add_contact(i)
#     test_db.add_contact('test4')
#     test_db.add_users(['test1', 'test2', 'test3', 'test4', 'test5'])
#     test_db.save_message('test2', 'in',
#                          f'Привет! я тестовое сообщение от {datetime.datetime.now()}!')
#     test_db.save_message('test2', 'out',
#                          f'Привет! я другое тестовое сообщение от {datetime.datetime.now()}!')
#     print(test_db.get_contacts())
#     print(test_db.get_users())
#     print(test_db.check_user('test1'))
#     print(test_db.check_user('test10'))
#     print(sorted(test_db.get_history('test2'), key=lambda item: item[3]))
#     test_db.del_contact('test4')
#     print(test_db.get_contacts())
