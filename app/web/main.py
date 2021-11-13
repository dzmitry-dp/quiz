from loguru import logger
from flask import Flask, render_template

from blueprint import get_client_print
import web_config
from logic.action import WebInterface, WorkWithCSV
import view


def create_app(name=__name__):
    "n - номер клиента"
    import os
    app = Flask(name, template_folder=web_config.config.FLASK_TEMPLATES_PATH, static_folder=web_config.config.FLASK_STATIC_PATH)
    app.config.from_object(web_config.FlaskConfiguration)
    
    for n in range(2):
        # 0 - клиент сам сервер
        # 1 - клиент_1
        bl_pt = get_client_print(n)
        
        @bl_pt.route('/master_game', methods=['POST', 'GET'])
        def in_the_game_client():
            logger.info('Вызвали страницу /master_game')
            from copy import copy
            game_data = WebInterface.read_game_data()

            if game_data.STAGE == 5:
                game_data.STAGE = 0
                game_data.QUESTION_NUMBER = 0
                WebInterface.update_game_data(game_data, 'сбрасываю STAGE на 0')
                return view.get_started_main_page()
            else:
                return render_template('round.html', round_number=game_data.STAGE +1 )

        @bl_pt.route('/question', methods=['POST', 'GET'])
        def page_question_client():
            logger.info('Вызвали страницу /question')
            game_data = WebInterface.read_game_data()

            if game_data.STAGE == 0:
                rule = '20s/20b'
                category = next(iter(web_config.config.CATEGORY_QUESTIONS[0]))
            elif game_data.STAGE == 1:
                rule = '20s/30b'
                category = next(iter(web_config.config.CATEGORY_QUESTIONS[1]))
            elif game_data.STAGE == 2:
                rule = '30s/50b'
                category = next(iter(web_config.config.CATEGORY_QUESTIONS[2]))
            elif game_data.STAGE == 3:
                rule = '40s/70b'
                category = next(iter(web_config.config.CATEGORY_QUESTIONS[3]))
            elif game_data.STAGE == 4:
                rule = '60s/100b'
                category = next(iter(web_config.config.CATEGORY_QUESTIONS[4]))
            
            if game_data.QUESTION_NUMBER < 10:
                question, _row_number_in_csv = WorkWithCSV.read_question(game_data.QUESTION_NUMBER, game_data.STAGE) # читаю вопрос
                answer_options = WorkWithCSV.read_answer_options(game_data.STAGE, _row_number_in_csv) # читаю варианты ответов
                answer = WorkWithCSV.read_correct_answer(game_data.STAGE, _row_number_in_csv) # читаю правильный ответ
                game_data.QUESTION_NUMBER += 1
                WebInterface.update_game_data(game_data, 'Увеличиваю QUESTION_NUMBER на 1')
                return render_template(
                    'main_client.html',
                    rule=rule,
                    category_name=category,
                    question=question,
                    answer_options=answer_options,
                    answer = answer,
                    question_number=game_data.QUESTION_NUMBER,
                    )

            if game_data.QUESTION_NUMBER == 10:
                # закончился раунд из 10ти вопросов
                if game_data.STAGE == 4:
                    # если это был последний раунд, то устанавливаем STAGE=5 для того, чтобы система отработала на выход из игры
                    game_data.STAGE = 5
                    WebInterface.update_game_data(game_data, 'устанавливаю STAGE на 5')
                    return view.get_teams_table()
                game_data.STAGE += 1
                game_data.QUESTION_NUMBER = 0
                WebInterface.update_game_data(game_data, 'Увеличиваем STAGE на 1')
                return in_the_game_client()

        app.register_blueprint(bl_pt, url_prefix=f'/client_{n}')
        logger.info(f'Web-Server: На локальном web сервере организованы страницы для client_{n}\n')
    
    return app

if __name__ == '__main__':

    view.client.run()
    logger.info('Web-Server: Was stoped')