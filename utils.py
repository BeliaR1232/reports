import os
from datetime import datetime

import requests


def get_request(url: str) -> list:
    try:
        req = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('Ошибка соединения. Проверьте подключение к интернету.')
    else:
        return req.json()


def create_dir() -> str:
    path = os.getcwd()
    try:
        if not os.path.exists(f'{path}/tasks'):
            os.mkdir('tasks')
    except OSError:
        print('Не получилось создать директорию')
    files_path = f'{path}/tasks'

    return files_path


def rename_old_reports(user: dict, files_path: str) -> None:
    file_path = f'{files_path}/{user.get("username")}.txt'

    if os.path.exists(file_path):
        date_time_created = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d.%m.%Y %H:%M')  # ИЗВИНИТЕ(
        new_file_name = f'{files_path}/old_{user["username"]}_{date_time_created}.txt'
        os.rename(file_path, new_file_name)
