import requests
import json
import os

from dotenv import load_dotenv
load_dotenv()


def send_sms(phones, text, total_price=0):
    login = os.getenv("SMSC_LOGIN")       # Логин в smsc
    password = os.getenv("SMSC_PASSWORD")  # Пароль в smsc
    sender = os.getenv("SMSC_SENDER")    # Имя отправителя
    # Возможные ошибки
    errors = {
        1: 'Ошибка в параметрах.',
        2: 'Неверный логин или пароль.',
        3: 'Недостаточно средств на счете Клиента.',
        4: 'IP-адрес временно заблокирован из-за частых ошибок в запросах. Подробнее',
        5: 'Неверный формат даты.',
        6: 'Сообщение запрещено (по тексту или по имени отправителя).',
        7: 'Неверный формат номера телефона.',
        8: 'Сообщение на указанный номер не может быть доставлено.',
        9: 'Отправка более одного одинакового запроса на передачу SMS-сообщения либо более пяти одинаковых запросов на получение стоимости сообщения в течение минуты. '
    }
    # Отправка запроса
    url = "http://smsc.ru/sys/send.php?login=%s&psw=%s&phones=%s&mes=%s&cost=%d&sender=%s&fmt=3" % (
        login, password, phones, text, total_price, sender)
    response = requests.get(url)
    answer = response.json()
    if 'error_code' in answer:
        # Возникла ошибка
        return errors[answer['error_code']]
    else:
        if total_price == 1:
            # Не отправлять, узнать только цену
            print('Будут отправлены: %d SMS, цена рассылки: %s' %
                  (answer['cnt'], answer['cost'].encode('utf-8'))
                  )
        else:
            # СМС отправлен, ответ сервера
            return answer
