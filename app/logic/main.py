"Главный файл логики игры"
from loguru import logger

from logic.action import WebInterface


class Master(WebInterface):
    "Логика запуска скрипта со статусом 'сервер'"
    def __init__(self) -> None:
        super().__init__() # собираю web интерфейс

    @property
    def preload(self):
        "Подготовка веб интерфейса"
        from logic.thread import MyThread
        #  отдельным потоком даем команду на запуст отдельного процесса
        t = MyThread(name='start_web_server', target=self.start_flask)
        t.run()
        logger.info('-- Запустил отдельным потоком WebInterface.start_flask    ()')
        # t.join() # ожидаем завершения потока
        # logger.info('Поток action.start_web() завершен')

    def call_the_client(self):
        # идет опрос клиентов
        logger.info('-- Обзваниваем клиентов')
    
