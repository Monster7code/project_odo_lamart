import requests
from requests.auth import HTTPBasicAuth

# Задайте ваши параметры
JIRA_URL = 'https://your-domain.atlassian.net'  # Замените на  URL Jira
USERNAME = 'your-email@example.com'  # Замените на  email
API_TOKEN = 'your_api_token'  # Замените на API токен


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


def get_user_issues(user_account_id):
    # URL для получения задач пользователя
    jql_query = f'assignee={user_account_id}'
    url = f"{JIRA_URL}/rest/api/3/search?jql={jql_query}&fields=summary,customfield_10002"  # идентификатор поля story points

    # Выполнение GET-запроса
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, API_TOKEN))

    # Проверка статуса ответа
    if response.status_code == 200:
        return response.json().get('issues', [])
    else:
        print(f"Ошибка: {response.status_code} - {response.text}")
        return []


user_email = 'user_email@example.com'

# Получение accountId по email
user_account_id = get_user_account_id(user_email)

if user_account_id:
    # Получение задач пользователя
    issues = get_user_issues(user_account_id)

    if issues:
        print("Задачи сотрудника:")
        for issue in issues:
            story_points = issue['fields'].get('customfield_10002', 0)  # идентификатор поля story points
            print(f"- Issue: {issue['key']}, Summary: {issue['fields']['summary']}, Story Points: {story_points}")
    else:
        print("Нет задач для отображения.")