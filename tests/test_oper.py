from src.oper import get_operations_data, filter_operations_data, show

test_data = [{
    "id": 863064926,
    "state": "EXECUTED",
    "date": "2019-12-08T22:46:21.935582",
    "operationAmount": {
      "amount": "41096.24",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    },
    "description": "Открытие вклада",
    "to": "Счет 90424923579946435907"
  },
  {
    "id": 594226727,
    "state": "CANCELED",
    "date": "2018-09-12T21:27:25.241689",
    "operationAmount": {
      "amount": "67314.70",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Перевод организации",
    "from": "Visa Platinum 1246377376343588",
    "to": "Счет 14211924144426031657"
  },
  {
    "id": 716496732,
    "state": "EXECUTED",
    "date": "2018-04-04T17:33:34.701093",
    "operationAmount": {
      "amount": "40701.91",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    },
    "description": "Перевод организации",
    "from": "Visa Gold 5999414228426353",
    "to": "Счет 72731966109147704472"
  }]

test_data_to = [{
    "id": 214024827,
    "state": "EXECUTED",
    "date": "2018-12-20T16:43:26.929246",
    "operationAmount": {
      "amount": "70946.18",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    },
    "description": "Перевод организации",
    "from": "Счет 10848359769870775355",
    "to": "Счет 21969751544412966366"
  }]

test_data_to_1 = [{
    "id": 895315941,
    "state": "EXECUTED",
    "date": "2018-08-19T04:27:37.904916",
    "operationAmount": {
      "amount": "56883.54",
      "currency": {
        "name": "USD",
        "code": "USD"
      }
    },
    "description": "Перевод с карты на карту",
    "from": "Visa Classic 6831982476737658",
    "to": "Visa Platinum 8990922113665229"
  }]

def test_get_operations_data():
    assert get_operations_data("operations.json") is not None
    assert type(get_operations_data("operations.json")) is list

def test_filter_operations_data():
    assert filter_operations_data(test_data) == [{
    "date": "04.04.2018",
    "description": "Перевод организации",
    "from": "Visa Gold 5999414228426353",
    "to": "Счет 72731966109147704472",
    "amount": "40701.91",
    "name": "USD"}]

def test_show():
    filtered_test_data = filter_operations_data(test_data)  #проверка карта -> счёт
    assert show(filtered_test_data) == f'04.04.2018 Перевод организации\nVisa Gold 5999 41** **** 6353 -> Счет **4472\n40701.91 USD\n{"-" * 60}\n'

    filtered_test_data_to = filter_operations_data(test_data_to)    #проверка счёт -> счёт
    assert show(filtered_test_data_to) == f'20.12.2018 Перевод организации\nСчет **5355 -> Счет **6366\n70946.18 USD\n{"-" * 60}\n'

    filtered_test_data_to_1 = filter_operations_data(test_data_to_1)    #проверка карта -> карта
    assert show(filtered_test_data_to_1) == f'19.08.2018 Перевод с карты на карту\nVisa Classic 6831 98** **** 7658 -> Visa Platinum 8990 92** **** 5229\n56883.54 USD\n{"-" * 60}\n'
