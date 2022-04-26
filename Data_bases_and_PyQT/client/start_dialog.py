# Стартовый диалог с выбором имени пользователя
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, qApp, QApplication


class UserNameDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ok_pressed = False
        self.setWindowTitle('Ку-ку!')
        self.setFixedSize(175, 93)

        self.label = QLabel('Введите никнейм пользователя: ', self)
        self.label.move(10, 10)
        self.setFixedSize(200, 150)

        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(154, 20)
        self.client_name.move(10, 30)

        self.btn_ok = QPushButton('Начать', self)
        self.btn_ok.move(10, 60)
        self.btn_ok.clicked.connect(qApp.exit)

        self.show()

        # Обработчик кнопки Ок, если поле ввода не пусто, ставим флаг и закрываем приложение
    def click(self):
        if self.client_name.text():
            self.ok_pressed = True
            qApp.exit()


if __name__ == '__main__':
    app = QApplication([])
    dial = UserNameDialog()
    app.exec_()