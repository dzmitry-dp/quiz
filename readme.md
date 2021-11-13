**Web-серверная программа quize.**
===
![alt text](https://github.com/dzmitry-dp/quiz/blob/master/app/web/static/img/fp.png?raw=true)
Общая логика
---
Скрипт запускается на web-серверe при загрузке операционной системы, как демон. На web-сервере нужен Linux, папка 'venv' в корне программы (Virtual Environment), Python3 и пакеты установленные через pip install (requirements.txt). 

Сеть
---
Клиенты просматривают веб-страницы и взаимодействуют с интерфейсом логики скрипта. Логика скрипта зависит от запросов клиентов. Запросы клиентов - 'это принудительное обновление веб-страницы.

Локальная сеть
---
Запуск скрипта изменяет отображаемые по адресам ниже страницы.

>http://local.host:5000/admin

>http://local.host:5000/teams

>http://local.host:5000/table

>http://local.host:5000/client_{0-4}/game


**Для запуска необходимо**
===
Для того, чтобы скрипт управлял процессов веб-сервера
---
>~$ sudo apt install net-tools

Virtual Environment
---
Папка с окружением в корне каталога Local_Quize_Server/

>~$ python3.10 -m venv ./Local_Quize_Server/venv

После активации виртуального окружения установим все необходимые пакеты:
>~$ pip install -r requirements.txt

Start Script
---
Автоматический запуск скрипта на сервере заказчика при загрузке Linux без графического интерфейса.

>~$ ./quiz.sh

Настройки параметров выполняется в файле ./app/config.py
