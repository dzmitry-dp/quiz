from loguru import logger

from logic.main import Master
# import logic.cnf as cnf # импортируем стартовые данные по игре


logger.add('game.log', format='{time}:{level}:{message}', rotation='100 KB', compression='zip', level='INFO')

try:
    quize_obj = Master()
    logger.info('1. Объект quize собран')

    quize_obj.preload()
    logger.info('--- Подготовили интерфейс. Далее обзвон всех клиентов ---')
    # подключаем клиентов
    quize_obj.call_the_client()
    logger.info('--- Собрали всех клиентов ---')

    circle = input('Убить Python? 1. Yes. q. Close script\n---\n')
    
    if circle == '1':
        quize_obj.kill_python()
    elif circle == 'q':
        pass
    else:
        pass

except KeyboardInterrupt:
    logger.info('KeyboardInterrupt')
    quize_obj.kill_python()
    exit()

logger.info('Скрипт закончил свою работу!')
exit()