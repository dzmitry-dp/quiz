###
LOGIN = 'Quize'
PASSWORD = '123'

###
# web адреса интерфейса
ADDRESS = 'http://127.0.0.1'
# ADDRESS = 'http://172.31.121.97'
PORT = '5000'

###
START_PAGE = f'{ADDRESS}:{PORT}/admin'
# START_PAGE = f'{ADDRESS}:{PORT}/game'

###
# команды автоматического запуска web интерфейса
import os
# cmd = 'firefox http://127.0.0.1:5000/admin'
CWD_PATH = os.getcwd()
CMD_START_FLASK_APP = f'{CWD_PATH}/venv/bin/python {CWD_PATH}/app/web/main.py'

###
# путь к файлу с названиями команд
# файл обновляется при каждом посещении страницы /teams
TEAMS_CSV_PATH = './app/logic/data/teams.csv'
FLASK_TEMPLATES_PATH = './app/web/templates'
FLASK_STATIC_PATH = './app/web/static'

###
# даммые о игре хранятся в файле
PATH_TO_GAME_DATA = 'game_data.pickle'

# сериалиованный объект процесса Python
FLASK_SUBPROCESS = 'flask_process.pickle'

# названия категорий игры
CATEGORY_QUESTIONS = [
    {'category_1': './app/logic/data/category_1'},
    {'category_2': './app/logic/data/category_2'},
    {'category_3': './app/logic/data/category_3'},
    {'category_4': './app/logic/data/category_4'},
    {'category_5': './app/logic/data/category_5'},
]