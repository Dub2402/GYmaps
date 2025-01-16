from Parser import Parser
from dublib.Methods.System import Clear
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QVBoxLayout, QWidget
import sys
from threading import Thread

Clear()

class Window(QWidget):
	# Конструктор приложения.
	def __init__(self):
		super().__init__()

		# Размер окна приложения.
		self.resize(640, 200)

		# Название приложения.
		self.setWindowTitle("GYmaps")
		self.setStyleSheet("background-color: grey")

		# Фон приложения.
		layout = QVBoxLayout()
		self.setLayout(layout)

		# Поле ввода текста.
		self.input = QLineEdit()

		# Размер поля.
		self.input.setFixedWidth(600)

		# Положение поля.
		layout.addWidget(self.input, alignment= Qt.AlignmentFlag.AlignCenter)

		# Создание кнопки.
		self.button = QPushButton("Начать парсинг данных")

		# Переход по ссылке при нажатии кнопки.
		self.button.clicked.connect(self.EnterUrl)

		# Создание кнопки.
		layout.addWidget(self.button)
		self.parser = None
		

#==========================================================================================#
#>>>>> ВВОД ССЫЛКИ ДЛЯ ПАРСИНГА <<<<< #
#==========================================================================================#

	# Ввод ссылки для парсинга сайта.
	def EnterUrl(self):
		if not self.parser: self.parser = Parser()
		Url = self.input.text()

		if "yandex" in Url:
			self.button.setText("Идёт парсинг данных ⏳")
			self.button.setEnabled(False)
			self.thread = Thread(target = self.parser.ParseYM, args=[Url, self.button])
			self.thread.start()

		if "google" in Url:
			self.button.setText("Идёт парсинг данных ⏳")
			self.button.setEnabled(False)
			self.thread = Thread(target = self.parser.ParseGM, args=[Url, self.button])
			self.thread.start()
			
			
#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ СКРИПТА <<<<< #
#==========================================================================================#

# Создаем экземпляр класса.
app = QApplication(sys.argv)
app.setStyle('fusion')
# Иконка приложения.
app.setWindowIcon(QtGui.QIcon("auth.ico"))

# Создаем виджет.
window = Window()
# Открытие окна приложения.
window.show()

#==========================================================================================#
# >>>>> вЫХОД ИЗ ПРИЛОЖЕНИЯ <<<<< #
#==========================================================================================#

# Выход из приложения.
sys.exit(app.exec())
