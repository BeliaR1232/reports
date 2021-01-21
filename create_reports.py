from datetime import datetime

from utils import (get_request, create_dir, rename_old_reports)

TASKS_URL = 'https://json.medrating.org/todos'
USERS_URL = 'https://json.medrating.org/users'


def get_users_data(users_url: str) -> list:
    users = get_request(url=users_url)

    if users:
        users_data = list()
        for user in users:
            if len(user) > 1:  # т.к может прийти невалидный объект
                users_data.append({'id': user.get('id'),
                                   'name': user.get('name'),
                                   'username': user.get('username'),
                                   'email': user.get('email'),
                                   'company_name': user.get('company').get('name'),
                                   })
        return users_data


def get_tasks_data(tasks_url: str) -> list:
    tasks = get_request(url=tasks_url)

    if tasks:
        tasks_data = list()
        for task in tasks:
            if len(task) > 1:  # т.к может прийти невалидный объект
                if len(task['title']) > 48:
                    task['title'] = task['title'][:48] + '...'
                tasks_data.append(task)
        return tasks_data


def get_tasks_for_user(user: dict, tasks: list) -> dict:
    tasks_for_user = {'tasks': {'completed_tasks': [], 'unfinished_tasks': []}}

    for task in tasks:
        if task['userId'] == user['id']:
            if task['completed']:
                tasks_for_user['tasks']['completed_tasks'].append(task['title'])
            else:
                tasks_for_user['tasks']['unfinished_tasks'].append(task['title'])

    return tasks_for_user


def get_report_text(user: dict, tasks: list) -> str:
    tasks = get_tasks_for_user(user=user, tasks=tasks)

    count_completed_tasks = len(tasks['tasks']['completed_tasks'])
    count_unfinished_tasks = len(tasks['tasks']['unfinished_tasks'])
    count_tasks = count_unfinished_tasks + count_completed_tasks

    completed_tasks = "\n".join(tasks['tasks']['completed_tasks'])
    unfinished_tasks = "\n".join(tasks['tasks']['unfinished_tasks'])

    time = datetime.now().strftime('%d.%m.%Y %H:%M')
    report_text = f'Отчёт для {user["company_name"]}.\n{user["name"]} <{user["email"]}> {time}\nВсего задач:' \
                  f' {count_tasks}\n\nЗавершённые задачи ({count_completed_tasks}):\n{completed_tasks}\n\n' \
                  f'Оставшиеся задачи ({count_unfinished_tasks}):\n{unfinished_tasks}'

    return report_text


def create_report() -> None:
    users = get_users_data(USERS_URL)
    tasks = get_tasks_data(TASKS_URL)
    dir_path = create_dir()

    if users is not None and tasks is not None:
        for user in users:
            file_path = f'{dir_path}/{user["username"]}.txt'
            data = get_report_text(user=user, tasks=tasks)
            rename_old_reports(user=user, files_path=dir_path)
            try:
                with open(file_path, 'w') as file:
                    file.write(data)
                    print(f'Отчёт для пользователя {user["name"]} был создан.')
            except OSError:
                print(f'Отчёт для пользователя {user["name"]} не был создан.')
    else:
        print('Данные не получены.')


if __name__ == "__main__":
    create_report()
