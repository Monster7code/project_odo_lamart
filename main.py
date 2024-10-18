import requests
from requests.auth import HTTPBasicAuth

# Задайте ваши параметры
JIRA_URL = 'https://your-domain.atlassian.net'  # Замените на ваш URL Jira
USERNAME = 'your-email@example.com'  # Замените на ваш email
API_TOKEN = 'your_api_token'  # Замените на ваш API токен


def get_user_account_id(email):
    # URL для получения информации о пользователе
    url = f"{JIRA_URL}/rest/api/3/user/search?username={email}"

    # Выполнение GET-запроса
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

    # Проверка статуса ответа
    if response.status_code == 200:
        users = response.json()
        if users:
            return users[0]['accountId']  # Возвращаем первый найденный accountId
        else:
            print("Пользователь не найден.")
            return None
    else:
        print(f"Ошибка: {response.status_code} - {response.text}")
        return None


def get_user_teams(user_account_id):
    # URL для получения команд пользователя
    url = f"{JIRA_URL}/rest/tempo-teams/1/team?accountId={user_account_id}"

    # Выполнение GET-запроса
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

    # Проверка статуса ответа
    if response.status_code == 200:
        teams = response.json()
        return teams
    else:
        print(f"Ошибка: {response.status_code} - {response.text}")
        return None


# Замените на email сотрудника, для которого вы хотите получить команды
user_email = 'user_email@example.com'  # Например, 'john.doe@example.com'

# Получение accountId по email
user_account_id = get_user_account_id(user_email)

if user_account_id:
    # Получение команд
    teams = get_user_teams(user_account_id)

    if teams:
        print("Команды сотрудника:")
        for team in teams:
            print(f"- {team['name']} (ID: {team['id']})")