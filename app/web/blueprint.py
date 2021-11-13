from flask import Blueprint


def get_client_print(n):
    import config
    "n - номер клиента"
    client_print = Blueprint(f'client_{n}', __name__, template_folder=config.FLASK_TEMPLATES_PATH, static_folder=config.FLASK_STATIC_PATH)
    return client_print
