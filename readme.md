**Flask + csv = Quiz**
===
![alt text](https://github.com/dzmitry-dp/quiz/blob/master/app/web/static/img/fp.png?raw=true)
Общая логика
---
Скрипт запускается на серверe при загрузке операционной системы, как демон. Папка 'venv' принципиально в корне программы. Это Virtual Environment для Python3 и пакетов установленных через pip install (requirements.txt). 

Сеть
---
Клиенты просматривают html-страницы и взаимодействуют с интерфейсом логики скрипта. Логика скрипта зависит от запросов клиентов. Запросы клиентов - это принудительное обновление браузера.

Скрипт меняет информацию на отображаемых по адресам ниже страницах:

>http://local.host:5000/admin

>http://local.host:5000/teams

>http://local.host:5000/table

>http://local.host:5000/client_{0-4}/game


**Для запуска необходимо**
===
Для того, чтобы скрипт управлял процессом веб-сервера
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
