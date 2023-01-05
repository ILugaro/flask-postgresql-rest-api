import requests

url = "http://127.0.0.1:5000/api/contacts/add"

contacts=[{'name': 'Дмитрий',
'last_name': 'Соколов',
'patronymic': 'Александрович',
'organization': 'Стройбуд',
'email': 'My_mail@gmail.com',
'phone': '41-52-47',},
{'name': 'Сергей',
 'last_name': 'Гордиенко',
 'patronymic': '',
 'organization': 'Стройбуд',
 'post': 'директор'},
{'name': 'Федор',
  'last_name': 'Матвиенко',
  'phone': '70991485536'},
{'name': 'Ольга',
  'last_name': 'Федорова',
  'patronymic': 'Валерьевна',
  'organization': 'Налоговая',
  'post': 'Директор',
  'email': 'testmail@mail.ru'},
{'organization': 'Монтаж-ГОСТ',
  'post': 'Слесарь',
  'phone': '+7(099) 246 1306'},
{'name': 'Коля',
 'last_name': 'Соколов',
 'post': 'Слесарь',
 'phone': '+7(099) 246 1306'}]

headers = {
  'Authorization': 'Basic Zmlyc3RBZG1pbjpESHNoMjM0dWk='
}

for contact in contacts:
    response = requests.request("POST", url, headers=headers, data=contact)
    print(response.text)

