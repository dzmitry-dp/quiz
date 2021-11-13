import os
import csv
from loguru import logger
from flask import render_template, request

from main import create_app
from web_config import _port
import config
from logic.action import WebInterface

logger.info('Web-Server: Буду создавать приложение Flask')
client = create_app(name='web_server') # сервер
logger.info('Web-Server: Flask создан!')

def rewrite_teams_csv_file(team_name_list, points_round_1=0, points_round_2=0, points_round_3=0, points_round_4=0, points_round_5=0):
    with open(config.TEAMS_CSV_PATH, 'w') as csvfile:
        logger.info('Web-Server: Открываем teams.csv на перезапись')
        csv_writer = csv.writer(csvfile, delimiter=';')
        for name in team_name_list:
            csv_writer.writerow([name, points_round_1, points_round_2, points_round_3, points_round_4, points_round_5])

def add_to_teams_csv_file(team_name, points_round_1=0, points_round_2=0, points_round_3=0, points_round_4=0, points_round_5=0):
    with open(config.TEAMS_CSV_PATH, 'a') as csvfile:
        logger.info('Web-Server: Открываем teams.csv на добавление')
        csv_writer = csv.writer(csvfile, delimiter=';',)
        csv_writer.writerow([team_name, points_round_1, points_round_2, points_round_3, points_round_4, points_round_5])

def open_csv_teams_file():
    line_count = 0 # количество строк в csv файле teams
    with open(config.TEAMS_CSV_PATH, 'r') as csvfile:
        logger.info('Web-Server: Открываем teams.csv на чтение')
        csv_reader = csv.reader(csvfile, delimiter=';')
        team_name_list = []
        teams_points = {}
        for row in csv_reader:
            team_name_list.append(row[0])
            teams_points[row[0]] = row[1:]
            line_count += 1
    logger.info(f'{teams_points}')
    return team_name_list, line_count, teams_points

def remove_teams_csv_file():
    try:
        os.remove(config.TEAMS_CSV_PATH)
        logger.info('Web-Server: Удалил teams.csv')
    except FileNotFoundError:
        logger.info('Web-Server: Файл не найден. teams.csv')

def messages_in_teams_form_line(line_count=0):
    if line_count == 0:
        message = 'Write the name of the first team ...'
    elif line_count == 1:
        message = 'Write the name of the second team ...'
    elif line_count == 2:
        message = 'Write the name of the third team ...' 
    elif line_count == 3:
        message = 'Write the name of the fourth team ...'
    return message

@client.route("/", methods=['POST', 'GET'])
def choice_client_server():
    logger.info('Web-Server: Вызвали адрес /')
    return render_template('index.html')

@client.route("/admin", methods=['POST', 'GET'])
def get_started_main_page():
    logger.info('Web-Server: Вызвали адрес /admin')

    remove_teams_csv_file()
    from logic.action import WebInterface

    iWeb = WebInterface()
    game_data = iWeb.game_data

    return render_template('main_server.html')

# del name from csv file
@client.route("/del", methods=['GET', 'POST'])
def delete_team_name():
    logger.info('Web-Server: Вызвали адрес /del')
    del_name = request.form.get('del', '')
    line_count = 0 # количество строк в файле
    with open(config.TEAMS_CSV_PATH, 'r') as csvfile:
        logger.info('Web-Server: Открываем teams.csv на чтение для удаления имени команды')
        csv_reader = csv.reader(csvfile, delimiter=';')
        team_name_list = []
       
        logger.info(f'Web-Server: Имя на удаление из списка {del_name}') 
        for row in csv_reader:
            if row[0] == del_name: # если имя на удаление, то не добавляем его в список имен
                pass
            else:
                team_name_list.append(row[0])
                line_count += 1
            
    team_name = request.form.get('name', '')

    if team_name == '':
        pass
    elif team_name not in team_name_list:
        team_name_list.append(team_name)
        line_count += 1

    rewrite_teams_csv_file(team_name_list)
    
    return get_started_teams_forms(team_name_list, line_count)

# press New Game
@client.route("/teams", methods=['POST', 'GET'])
def get_started_teams_forms(team_name_list=None, line_count=None):
    # по нажатию на NEW GAME на web странице
    logger.info('Web-Server: Вызвали адрес /teams')
    
    if request.method == "GET":
        remove_teams_csv_file()
        team_name_list = []
        rewrite_teams_csv_file(team_name_list)
        return render_template('teams_forms.html', team_number=messages_in_teams_form_line(), team_name_list=team_name_list)

    if request.method == "POST":
        try:
            team_name = request.form['name'] # название команды которой вводит ведущий
        except KeyError:
            team_name = ''

        if team_name != '': # если небыло название команды, то страница возвращает ''
            # если имя команды не пустая строка
            add_to_teams_csv_file(
                team_name=team_name,
            )
            team_name_list, line_count, teams_points = open_csv_teams_file()
            
            if line_count == 4:
                return get_teams_table()
        
        elif team_name == '': # если небыло название команды, то страница возвращает ''
            # если имя - пустая строка
            if team_name_list == None and line_count == None:
                team_name_list, line_count, teams_points = open_csv_teams_file()

        return render_template('teams_forms.html', team_number=messages_in_teams_form_line(line_count), team_name_list=team_name_list)


# show Big screen table
@client.route("/table", methods=['GET', 'POST'])
def get_teams_table():
    logger.info('Web-Server: Вызвали адрес /table')
    team_name_list, line_count, teams_points = open_csv_teams_file()
    points_dict = {}
    for team in teams_points:
        points_dict[team] = [ teams_points[team], str(sum([int(x) for x in teams_points[team]])) ]
    return render_template('teams_table.html', team_name_list=team_name_list, points_dict=points_dict)

# press Reset
@client.route("/shutdown", methods=['GET', ])
def reset_server():
    logger.info('Web-Server: Вызвали адрес /shutdown')
    from logic.action import kill_python
    kill_python()
    return 'Restart your computer'