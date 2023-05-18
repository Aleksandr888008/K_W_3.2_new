import json
import os.path
from datetime import datetime

# path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'operations.json')

def get_operations_data(path):
    """Переводим из словоря json в формат Python. Собираем новый словарь с нужными списками. Выстраиваем по дате операций."""
    with open(path, encoding='utf-8') as file:
        operations = json.load(file)
        return operations

def filter_operations_data(operations):
    """Функция формирует новый словарь из списков по определенным ключам"""
    operation = []  # Собираем новый словарь с нужными списками
    for op in operations:
        if not (op.get('from') and op.get('state')):    #отсортировываем словари, где нет "from"
            continue
        if op["state"] == "EXECUTED":
            date = datetime.strptime(op["date"], '%Y-%m-%dT%H:%M:%S.%f')
            date = date.strftime('%d.%m.%Y')
            operation.append({"date": date,
                              "description": op["description"],
                              "from": op["from"],
                              "to": op["to"],
                              "amount": op["operationAmount"]["amount"],
                              "name": op["operationAmount"]["currency"]["name"],
                              })

    #Выстраиваем по дате операций.
    operation_sort = sorted(operation, key=lambda x: '.'.join(reversed(x["date"].split('.'))), reverse=True)
    return operation_sort


def hide_sender_bill(operation):
    """Функция скрывает цифры карты с 7 по 12 (заменяя их звездочками) и разбивает номер по группам из 4 символов.
    Скрывает номер счета с 1 по 16 цифры (заменяя их звездочками) и оставляет последние 4 цифры.
    Действия функции происходят со счетом или картой операции - "from" (откуда идет списание средств).
    """

    card_dig_len = 16
    bank_account_digits = 20

    hide_start = 6
    hide_end = 12
    hidden_simbols = hide_end - hide_start

    bill_credintials = " ".join(operation["from"].split(" ")[:-1])  #забираем начало карты или счета Visa Gold
    bill_numbers = operation["from"].split(" ")[-1] #забираем только цифры 42342345

    if len(bill_numbers) == card_dig_len:
        masked_bill_numbers = bill_numbers[:hide_start] + "*" * hidden_simbols + bill_numbers[hide_end:]    #заменяем цифры на *
        numbers_str = str(masked_bill_numbers)
        mask = ' '.join(numbers_str[i:i+4] for i in range(0, len(numbers_str), 4))  #разбиваем на групы по 4 цифры
        full_masked_bill = [bill_credintials, mask] #собираем список
        return " ".join(full_masked_bill) #собираем через пробел окончательный вариант вывода карты Maes 243245******
    else:
        masked_bill_numbers_check = bill_numbers.replace(bill_numbers[:-4], "**")   #заменяем цифры на *
        full_masked_bill_check = [bill_credintials, masked_bill_numbers_check]  #собираем список
        return " ".join(full_masked_bill_check) #собираем через пробел окончательный вариант вывода счёта


def hide_sender_bill_to(operation):
    """Функция скрывает цифры карты с 7 по 12 (заменяя их звездочками) и разбивает номер по группам из 4 символов.
    Скрывает номер счета с 1 по 16 цифры (заменяя их звездочками) и оставляет последние 4 цифры.
    Действия функции происходят со счетом или картой операции - "to" (приход средств).
    """
    card_dig_len = 16
    bank_account_digits = 20

    hide_start = 6
    hide_end = 12
    hidden_simbols = hide_end - hide_start

    bill_credintials = " ".join(operation["to"].split(" ")[:-1])
    bill_numbers = operation["to"].split(" ")[-1]

    if len(bill_numbers) == card_dig_len:
        masked_bill_numbers = bill_numbers[:hide_start] + "*" * hidden_simbols + bill_numbers[hide_end:]
        numbers_str = str(masked_bill_numbers)
        mask = ' '.join(numbers_str[i:i+4] for i in range(0, len(numbers_str), 4))
        full_masked_bill = [bill_credintials, mask]
        return " ".join(full_masked_bill)
    else:
        masked_bill_numbers_check = bill_numbers.replace(bill_numbers[:-4], "**")
        full_masked_bill_check = [bill_credintials, masked_bill_numbers_check]
        return " ".join(full_masked_bill_check)


def show(operation_show):
    """Выводим список из 5 операций"""

    operations = []
    for i in operation_show[:5]:
        operation = f'{i["date"]} {i["description"]}\n{hide_sender_bill(i)} -> {hide_sender_bill_to(i)}\n{i["amount"]} {i["name"]}\n{"-" * 60}\n'
        operations.append(operation)
    return "".join(operations)



