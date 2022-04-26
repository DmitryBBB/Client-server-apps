import datetime


from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class ServerDB:
    # Функция declarative_base(), что определяет новый класс Base,
    # от которого будут унаследованы все наши ORM-классы.
    Base = declarative_base()

    # Отображение Таблицы - Все пользователи
    class AllUsers(Base):
        __tablename__ = 'Users'  # название таблицы
        # Поля таблицы и соответствия критериям
        id = Column(Integer, primary_key=True)
        name = Column(String, unique=True)
        last_login = Column(DateTime)  # время последнего подключения

        # инициализация полей
        def __init__(self, username):

            self.name = username
            self.last_login = datetime.datetime.now()
            self.id = None
    # Отображение Таблицы - Активные пользователи
    class ActiveUsers(Base):
        __tablename__ = 'Active_users'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('Users.id'), unique=True)  # связь с таблицей Users по id(уникально)
        ip_address = Column(String)
        port = Column(Integer)
        login_time = Column(DateTime)  # время подключения

        def __init__(self, user_id, ip_address, port, login_time):
            self.user = user_id
            self.ip_address = ip_address
            self.port = port
            self.login_time = login_time
            self.id = None

    # Отображение Таблицы - История входа
    class LoginHistory(Base):
        __tablename__ = 'Login_history'
        id = Column(Integer, primary_key=True)
        name = Column(String, ForeignKey('Users.id'), unique=True)
        ip = Column(String)
        port = Column(Integer)
        date_time = Column(DateTime)

        def __init__(self, name, ip, port, date):
            self.id = None
            self.name = name
            self.date_time = date
            self.ip = ip
            self.port = port



    # Таблица контактов пользователей
    class UserContacts(Base):
        __tablename__ = 'Contacts'
        id = Column(Integer, primary_key=True)
        user = Column(ForeignKey('Users.id'))
        contact = Column(ForeignKey('Users.id'))

        def __init__(self, user, contact):
            self.id = None
            self.user = user
            self.contact = contact

    # Таблица истории пользователей
    class UsersHistory(Base):
        __tablename__ = 'History'
        id = Column(Integer, primary_key=True)
        user = Column(ForeignKey('Users.id'))
        sent = Column(Integer)
        accepted = Column(Integer)

        def __init__(self, user):
            self.id = None
            self.user = user
            self.sent = 0
            self.accepted = 0

    def __init__(self, path):
        # Создаём движок базы данных
        # echo=False - отключает вывод на экран sql-запросов)
        # pool_recycle - по умолчанию соединение с БД через 8 часов простоя обрывается
        # Чтобы этого не случилось необходимо добавить pool_recycle=7200 (переустановка
        #    соединения через каждые 2 часа)
        self.database_engine = create_engine(f'sqlite:///{path}', echo=False, pool_recycle=7200,
                                             connect_args={'check_same_thread': False})

        # СОЗДАЕМ ТАБЛИЦЫ
        self.Base.metadata.create_all(self.database_engine)

        # СОЗДАЕМ СЕССИЮ
        Session = sessionmaker(bind=self.database_engine)
        self.session = Session()

        # Если в таблице активных пользователей есть записи, то их необходимо удалить
        # Когда устанавливаем соединение, очищаем таблицу активных пользователей
        self.session.query(self.ActiveUsers).delete()
        self.session.commit()  # сохраняем изменение

    # Функция регистрирует пользователя при входи и записывает этот факт в базу
    def user_login(self, username, ip_address, port):
        # print(username, ip_address, port)
        # Запрос в таблицу AllUsers на наличие там пользователя с таким именем
        rez = self.session.query(self.AllUsers).filter_by(name=username)

        # Если имя пользователя есть в таблице, обновляем время последнего входа
        if rez.count():
            user = rez.first()
            user.last_conn = datetime.datetime.now()

        # Если нет такого пользователя, создаем нового
        else:
            # Создаем экземпляр класса self.AllUsers, через который передаем данные в таблицу
            user = self.AllUsers(username)
            self.session.add(user)
            # Коммит здесь нужен для того, чтобы создать нового пользователя,
            # id которого будет использовано для добавления в таблицу активных пользователей
            self.session.commit()
            user_in_history = self.UsersHistory(user.id)
            self.session.add(user_in_history)

        # Создаем запись в таблицу ActiveUsers о факте входа
        # Создаём экземпляр класса self.ActiveUsers, через который передаём данные в таблицу
        new_active_user = self.ActiveUsers(user.id, ip_address, port, datetime.datetime.now())
        self.session.add(new_active_user)

        # Создаем экземпляр класса self.LoginHistory, через который передаём данные в таблицу
        history = self.LoginHistory(user.id, ip_address, port, datetime.datetime.now())
        self.session.add(history)
        # Сохраняем изменения
        self.session.commit()

    # Функция фиксирует отключения пользователей
    def user_logout(self, username):
        # запрашиваем пользователя, что покидает нас, получаем запись из таблицы AllUsers
        user = self.session.query(self.AllUsers).filter_by(name=username).first()
        # Удаляем его из таблицы активный пользователей
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        # Сохраняем изменения
        self.session.commit()

    # Функция фиксирует передачу сообщений и делает соответствующие отметки в БД
    def process_message(self, sender, recipient):
        # Получаем ID отправителя и получателя
        sender = self.session.query(self.AllUsers).filter_by(name=sender).first().id
        recipient = self.session.query(self.AllUsers).filter_by(name=recipient).first().id
        # запрашиваем строки из истории и увеличиваем счетчик
        sender_row = self.session.query(self.UsersHistory).filter_by(user=sender).first()
        sender_row.sent += 1
        recipient_row = self.session.query(self.UsersHistory).filter_by(user=recipient).first()
        recipient_row.accepted += 1
        self.session.commit()

    # Функция добавляет контакт для пользователя
    def add_contact(self, user, contact):
        # получаем ID пользователей
        user = self.session.query(self.AllUsers).filter_by(name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(name=contact).first()
        # проверка на дубль и что контакт может сущестоввать(полю пользователь мы доверяем)
        if not contact or self.session.query(self.UserContacts).filter_by(user=user.id, contact=contact.id).count():
            return

        # Создаем объект и заносим его в базу
        contact_row = self.UserContacts(user.id, contact.id)
        self.session.add(contact_row)
        self.session.commit()

    # функция удаляет контакт из БД
    def remove_contact(self, user, contact):
        # Получаем ID пользователей
        user = self.session.query(self.AllUsers).filter_by(name=user).first()
        contact = self.session.query(self.AllUsers).filter_by(name=contact).first()
        # Проверяем что контакт может существовать
        if not contact:
            return

        # удаляем требуемое
        self.session.query(self.UserContacts).filter(
            self.UserContacts.user == user.id,
            self.UserContacts.contact == contact.id
        ).delete()
        self.session.commit()

    # Функция возвращает список последних пользователей со временем последнего входа
    def users_list(self):
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login,
        )
        return query.all()  # возвращаем список котежей

    # Функция возвращает список активных пользователей
    def active_users_list(self):
        # Запрашиваем соединение таблиц и собираем тюплы имя, адрес, порт, время.
        query = self.session.query(
            self.AllUsers.name,
            self.ActiveUsers.ip_address,
            self.ActiveUsers.port,
            self.ActiveUsers.login_time
        ).join(self.AllUsers)
        # Возвращаем список кортежей
        return query.all()

    # функция возвращает историю входа по пользвателю или по всем пользователям
    def login_history(self, username=None):
        # Запрашиваем историю входа
        query = self.session.query(self.AllUsers.name,
                                   self.LoginHistory.date_time,
                                   self.LoginHistory.ip,
                                   self.LoginHistory.port
                                   ).join(self.AllUsers)
        # Если было указано имя пользователя, то фильтруем по нему
        if username:
            query = query.filter(self.AllUsers.name == username)
        return query.all()

    # функция возвращает список контактов пользователя
    def get_contacts(self, username):
        # запрашиваем указанного пользователя
        user = self.session.query(self.AllUsers).filter_by(name=username).one()
        # запрашиваем его список контактов
        query = self.session.query(self.UserContacts, self.AllUsers.name).filter_by(user=user.id). \
            join(self.AllUsers, self.UserContacts.contact == self.AllUsers.id)
        # выбираем только имена пользователей и возвращаем их
        return [contact[1] for contact in query.all()]

    # Функция возвращает количество переданных и полученных сообщений

    def message_history(self):
        query = self.session.query(
            self.AllUsers.name,
            self.AllUsers.last_login,
            self.UsersHistory.sent,
            self.UsersHistory.accepted,

        ).join(self.AllUsers)
        # Возвращаем список кортежей
        return query.all()



if __name__ == '__main__':
    test_db = ServerDB('server_base.db3')
    test_db.user_login('1111', '192.168.1.113', 8080)
    test_db.user_login('McG2', '192.168.1.113', 8081)
    print(test_db.users_list())
    # print(test_db.active_users_list())
    # test_db.user_logout('McG')
    # print(test_db.login_history('re'))
    # test_db.add_contact('test2', 'test1')
    # test_db.add_contact('test1', 'test3')
    # test_db.add_contact('test1', 'test6')
    # test_db.remove_contact('test1', 'test3')
    test_db.process_message('McG2', '1111')
    print(test_db.message_history())

# if __name__ == '__main__':
#     db = ServerDB()
#     db.user_login('client_1', '192.168.1.4', 8888)
#     db.user_login('client_2', '192.168.1.5', 7777)
#     # выводим список кортежей - активных пользователей
#     print(db.active_users_list())
#     # выполянем 'отключение' пользователя
#     db.user_logout('client_1')
#     print(db.users_list())
#     # выводим список активных пользователей
#     print(db.active_users_list())
#     db.user_logout('client_2')
#     print(db.users_list())
#     print(db.active_users_list())
#
#     # запрашиваем историю входов по пользователю
#     db.login_history('client_1')
#     # # выводим список известных пользователей
#     print(db.users_list())
