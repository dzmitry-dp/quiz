"Замораживаем данные о игре при помощи "

import config

class GameDataClass:
    'Класс который сериализуется для сохранения данных о игре'
    def __init__(self) -> None:
        self.START_PAGE = config.START_PAGE
        self.PATH_TO_GAME_DATA = config.PATH_TO_GAME_DATA
        self.STAGE = 0 # текущий раунд игры
        self.PYTHON_PID = None # pid процесса python flask
        self.QUESTION_NUMBER = 0

    def __repr__(self) -> str:
        return f'''\n
        START_PAGE = {self.START_PAGE}
        PATH_TO_GAME_DATA = '{self.PATH_TO_GAME_DATA}'
        STAGE = {self.STAGE}
        PYTHON_PID = {self.PYTHON_PID}
        QUESTION_NUMBER = {self.QUESTION_NUMBER}
        '''
