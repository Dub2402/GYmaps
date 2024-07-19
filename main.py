from Parser import Parser
from dublib.Methods.System import Cls

Cls()

Value = input("Введите g - для парсинга google maps, y - для yandex maps. Или нажмите enter для парсинга обоих сайтов.")
parser = Parser()
if Value == "g": parser.ParseGM()
elif Value == "y": parser.ParseYM()
else:
    parser.ParseYM()
    parser.ParseGM()