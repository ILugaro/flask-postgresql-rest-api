import requests
from requests.auth import HTTPBasicAuth
import json

url_contacts = 'http://127.0.0.1:5000/api/contacts'
url_listUsers = 'http://127.0.0.1:5000/api/userList'
admin_auth = HTTPBasicAuth('firstAdmin', 'DHsh234ui')


def contact_creator(file, login, password):
    '''создает базу контактов на основе файла. От имени пользователя login (password - пароль данного клиента)'''
    with open(file, encoding='utf-8') as f:
        contacts = json.load(f)

    basic = HTTPBasicAuth(login, password)
    for contact in contacts:
        response = requests.request('POST', url_contacts + '/add', data=contact, auth=basic)
        print(response.text)

'''Очистка БД'''
response = requests.request('POST', url_listUsers + '/reset', auth=admin_auth)
response = requests.request('POST', url_contacts + '/show', auth=admin_auth)
if len(response.json()) == 0:
    print('База данных очищена')
else:
    print('Ошибка при очистке базы данных')
    exit()

'''Создание дополнительных клиентов'''
with open('clients.json', encoding='utf-8') as f:
    clients = json.load(f)
for client in clients:
    print(client)
    response = requests.request('POST', url_listUsers, auth=admin_auth, data=client)

'''Наполнение контактами с файла JSON'''
contact_creator('contacts_for_DefaultUser1.json', 'DefaultUser1', 'PassUser1')
contact_creator('contacts_for_DefaultUser2.json', 'DefaultUser2', 'PassUser2')

response = requests.request('POST', url_contacts + '/show', data ={'name': 'Виктор'}, auth=admin_auth)

response = requests.request('DELETE', url_contacts + '/', auth=admin_auth)

print('База данных заполнена')

#тест полнотектового поиска:
tests = [{'requests':
            {'target': 'Полнотектовый поиск админом',
             'data': {'search': ''},
             'client': {'login': '', 'pass': ''}},
          'response':
              {'count': 1,
               'check_data': {},
               'status': ''}},
          {'requests':
            {'target': 'Полнотектовый поиск админом',
             'data': {'search': ''},
             'client': {'login': '', 'pass': ''}},
          'response':
              {'count': 1,
               'check_data': {},
               'status': ''}}
         ]


