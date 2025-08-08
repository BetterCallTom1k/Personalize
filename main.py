import requests
import json
import uuid
from typing import Union, Dict

# Конфиденциальные данные лучше вынести в переменные окружения
SBER_ID = "3b4dd2a3-eacc-4d5d-ae85-b62196ad659e"
SBER_AUTH = "M2I0ZGQyYTMtZWFjYy00ZDVkLWFlODUtYjYyMTk2YWQ2NTllOjM4YjcxMDI3LTUyYjgtNDk5YS04ZDg5LWQ3ZTBlMmQxNGM3MA=="
SBER_SECRET = "38b71027-52b8-499a-8d89-d7e0e2d14c70"

class User:
    def __init__(self, name: str, phone: str, email: str):
        self.name = name
        self.phone = phone
        self.email = email


def get_token(auth_token: str, scope: str = "GIGACHAT_API_PERS") -> Union[Dict, int]:
    """
    Получает токен доступа для GigaChat API

    :param auth_token: Basic-токен авторизации
    :param scope: Запрашиваемый уровень доступа
    :return: Ответ сервера в виде словаря или -1 в случае ошибки
    """
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),
        'Authorization': f'Basic {auth_token}'
    }

    data = f'scope={scope}'

    try:
        response = requests.post(url, headers=headers, data=data, verify=False)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
            return -1
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return -1


def create_message(user: 'User') -> str:
    """
    Берет шаблонный текст рассылки и вставляет в него параметры человека.

    :param user: объект класса User - человек, который ведет рассылку.
    :return: Готовый текст с подставленными данными.
    """
    with open("promt_file.txt", "r", encoding="utf-8") as file:
        raw_text = file.read()

    # Заменяем только нужные поля, остальные скобки остаются как есть
    formatted_text = raw_text.format(
        ИМЯ=user.name,
        **{"ВАШ НОМЕР": user.phone, "ВАША ПОЧТА": user.email}
    )

    return formatted_text


def generation_request(auth_token: str, prompt: str, model: str = "GigaChat-2") -> Union[Dict, int]:
    """
    Делает запрос на генерацию текста

    :param auth_token: Bearer-токен авторизации
    :param prompt: Текст запроса
    :param model: Модель для генерации
    :return: Ответ сервера в виде словаря или -1 в случае ошибки
    """
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1,
        "update_interval": 0,
        "profanity_check": True
    }

    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
            return -1
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return -1


#Тестируем токен
# token_response = get_token(SBER_AUTH)
# if token_response != -1:
#     print("Токен успешно получен:")
#     print(json.dumps(token_response, indent=2))
#     giga_token = token_response['access_token']
#
#     # Делаем запрос на генерацию
#     answer = generation_request(giga_token, 'Как сделать get запрос на языке Python')
#
#     if answer != -1:
#         print("\nОтвет от GigaChat:")
#         print(answer['choices'][0]['message']['content'])
#     else:
#         print("Не удалось получить ответ от GigaChat")
# else:
#     print("Не удалось получить токен")

#Тестируем создание текста рассылки
# Artem = User("Артем", "+799999999", "artem.samsonov@mail.ru")
# print(create_message(Artem))