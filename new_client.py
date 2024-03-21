import sys
import socket
from threading import Thread

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QFontDialog, QInputDialog, QMessageBox
from PySide6.QtGui import QFont
from design_client import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        # вызовем метод родительского класса
        super(MainWindow, self).__init__()

        # создадим объект
        self.ui = Ui_MainWindow()
        # инициализируем нашу форму
        self.ui.setupUi(self)

        self.s = socket.socket()
        t = Thread(target=self.client_thread)
        t.daemon = True
        t.start()

        self.ui.send.clicked.connect(self.click)

    def click(self):
        self.ui.text.clear()

    def client_thread(self):

        self.s.connect(('127.0.0.1', 50025))
        self.s.send('test'.encode())
        while True:
            message = self.s.recv(1024).decode()
            self.ui.messages.addItem(message)


if __name__ == "__main__":

    # Создадим Qt Application
    app = QApplication(sys.argv)
    # Создадим и покажем главное окно
    window = MainWindow()
    # Показываем окно
    window.show()
    # Запустим приложение
    sys.exit(app.exec())
