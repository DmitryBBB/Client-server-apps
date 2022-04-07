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
        __tablename__ = 'all_users'  # название таблицы
        # Поля таблицы и соответствия критериям
        id = Column(Integer, primary_key=True)
        login = Column(String, unique=True)
        last_conn = Column(DateTime)  # время последнего подключения

        # инициализация полей
        def __init__(self, login):
            self.login = login
            self.last_conn = datetime.datetime.now()

    # Отображение Таблицы - Активные пользователи
    class ActiveUsers(Base):
        __tablename__ = 'active_users'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.id'), unique=True)  # связь с таблицей all_users по id(уникально)
        ip = Column(String)
        port = Column(Integer)
        time_conn = Column(DateTime)  # время подключения

        def __init__(self, user, ip, port, time_conn):
            self.user = user
            self.ip = ip
            self.port = port
            self.time_conn = time_conn

    # Отображение Таблицы - История входа
    class LoginHistory(Base):
        __tablename__ = 'login_history'
        id = Column(Integer, primary_key=True)
        user = Column(String, ForeignKey('all_users.id'), unique=True)
        ip = Column(String)
        port = Column(Integer)
        last_conn = Column(DateTime)

        def __init__(self, user, ip, port, last_conn):
            self.user = user
            self.ip = ip
            self.port = port
            self.last_conn = last_conn

    def __init__(self):
        # Создаём движок базы данных
        # SERVER_DATABASE - sqlite:///server_base.db3
        # echo=False - отключает вывод на экран sql-запросов)
        # pool_recycle - по умолчанию соединение с БД через 8 часов простоя обрывается
        # Чтобы этого не случилось необходимо добавить pool_recycle=7200 (переустановка
        #    соединения через каждые 2 часа)
        self.database_engine = create_engine('sqlite:///server_base.db3', echo=False, pool_recycle=7200)

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
        rez = self.session.query(self.AllUsers).filter_by(login=username)

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
        user = self.session.query(self.AllUsers).filter_by(login=username).first()
        # Удаляем его из таблицы активный пользователей
        self.session.query(self.ActiveUsers).filter_by(user=user.id).delete()
        # Сохраняем изменения
        self.session.commit()

    # Функция возвращает список последних пользователей со временем последнего входа
    def users_list(self):
        query = self.session.query(
            self.AllUsers.login,
            self.AllUsers.last_conn,
        )
        return query.all()  # возвращаем список котежей

    # Функция возвращает список активных пользователей
    def active_users_list(self):
        # Запрашиваем соединение таблиц и собираем тюплы имя, адрес, порт, время.
        query = self.session.query(
            self.AllUsers.login,
            self.ActiveUsers.ip,
            self.ActiveUsers.port,
            self.ActiveUsers.time_conn
        ).join(self.AllUsers)
        # Возвращаем список кортежей
        return query.all()

    # функция возвращает историю входа по пользвателю или по всем пользователям
    def login_history(self, username=None):
        # Запрашиваем историю входа
        query = self.session.query(self.AllUsers.login,
                                   self.LoginHistory.last_conn,
                                   self.LoginHistory.ip,
                                   self.LoginHistory.port
                                   ).join(self.AllUsers)
        # Если было указано имя пользователя, то фильтруем по нему
        if username:
            query = query.filter(self.AllUsers.login == username)
        return query.all()


if __name__ == '__main__':
    db = ServerDB()
    db.user_login('client_1', '192.168.1.4', 8888)
    db.user_login('client_2', '192.168.1.5', 7777)
    # выводим список кортежей - активных пользователей
    print(db.active_users_list())
    # выполянем 'отключение' пользователя
    db.user_logout('client_1')
    print(db.users_list())
    # выводим список активных пользователей
    print(db.active_users_list())
    db.user_logout('client_2')
    print(db.users_list())
    print(db.active_users_list())

    # запрашиваем историю входов по пользователю
    db.login_history('client_1')
    # # выводим список известных пользователей
    print(db.users_list())