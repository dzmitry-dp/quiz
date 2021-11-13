from loguru import logger
import subprocess
import pickle
import csv

import config
from logic.cnf import GameDataClass

class WorkWithCSV:
    @staticmethod
    def read_question(question_number, stage):
        _path = f'{list(config.CATEGORY_QUESTIONS[stage].values())[0]}/questions.csv'
        with open(_path, 'r') as csvfile:
            logger.info(f'Читаю вопросы квиза по адресу {_path}')
            csv_reader = csv.reader(csvfile, delimiter=';')
            questions_list = []
            for row in csv_reader:
                questions_list.append(row[0])

            from random import choice
            random_question = choice(questions_list)
        return random_question, questions_list.index(random_question)

    @staticmethod
    def read_answer_options(stage, row_number):
        _path = f'{list(config.CATEGORY_QUESTIONS[stage].values())[0]}/answer_options.csv'
        with open(_path, 'r') as csvfile:
            logger.info(f'Читаю ответы квиза по адресу {_path}')
            csv_reader = csv.reader(csvfile, delimiter=';')
            answer_list = []
            for row in csv_reader:
                answer_list.append(row)
        return answer_list[row_number]

    @staticmethod
    def read_correct_answer(stage, row_number):
        return 'Вариант 3'

class WebInterface:
    def __init__(self) -> None:
        logger.info('Собираем WebInterface class')
        self._game_data = None

    @staticmethod
    def read_game_data():
        with open(config.PATH_TO_GAME_DATA, 'rb') as file:
            game_data = pickle.load(file)
            logger.info(f'{game_data}')
        return game_data

    @staticmethod
    @logger.catch
    def update_game_data(data, message=None):
        'Данные о игре обновляются каждый раунд'
        with open(config.PATH_TO_GAME_DATA, 'wb') as file:
            logger.info(f'Запись файла {config.PATH_TO_GAME_DATA}. {message}')
            pickle.dump(data, file)

    @property
    @logger.catch
    def game_data(self):
        if self._game_data == None:
            game_data = GameDataClass()
            # после того, как процесс был запущен запишем pid в данный о игре
            game_data.PYTHON_PID = self._get_pid() # сохраняю pip процесса
            self.update_game_data(data=game_data, message='- Это базовые настройки.')
            self._game_data = game_data

        ###
            for x in self._game_data.__dict__:
                print(x, ':', self._game_data.__dict__[x])
        ###

        return self._game_data

    @logger.catch
    def _get_pid(self):
        cmd = f'netstat -tulnp | grep :{config.PORT} && /python'
        process_out = subprocess.run(cmd, shell=True, capture_output=True)
        python_pid = process_out.stdout.decode("utf-8").replace(' ', '').split('LISTEN')[-1].split('/')[0]
        logger.info(f'{process_out}')
        return python_pid

    @logger.catch
    def start_flask(self):
        "Раскручиваем Flask и запускаем браузер"
        logger.info(f'Запускаем Flask отдельным процессом {config.CMD_START_FLASK_APP}')
        p = subprocess.Popen([config.CMD_START_FLASK_APP,], shell=True, stdout=subprocess.PIPE)

        # запускаем браузер по нужному адресу
        import webbrowser
        webbrowser.open_new_tab(f'{config.START_PAGE}')

        # self.game_data()

        # self.update_game_data(data=self._game_data, message='Добавляем pid') # обновляем данные по игре, т.к. появился Flask отдельным процессом
        # и впринципе здесь заканчивается предподготовка приложения

        # p.wait() # ждем на текушем месте, скорее для отладки

    @logger.catch
    def kill_python(self):
        logger.info(f'Убиваю процесс {self.game_data.PYTHON_PID} python')
        subprocess.call(f'kill 9 {self.game_data.PYTHON_PID}', shell=True)
        logger.info('Python убит')
