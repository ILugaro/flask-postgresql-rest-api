import requests
from requests.auth import HTTPBasicAuth
import json

url_contacts = 'http://127.0.0.1:5000/api/contacts'
url_listUsers = 'http://127.0.0.1:5000/api/userList'
admin_auth = HTTPBasicAuth('firstAdmin', 'DHsh234ui')
DefaultUser1_auth = HTTPBasicAuth('DefaultUser1', '"PassUser1')
DefaultUser2_auth = HTTPBasicAuth('DefaultUser2', 'PassUser2')



def contact_creator(file, login, password):
    '''создает базу контактов на основе файла. От имени пользователя login (password - пароль данного клиента)'''
    with open(file, encoding='utf-8') as f:
        contacts = json.load(f)
    basic = HTTPBasicAuth(login, password)
    for contact in contacts:
        response = requests.request('POST', url_contacts + '/add', data=contact, auth=basic)


'''Очистка БД'''
response = requests.request('POST', url_listUsers + '/reset', auth=admin_auth)
response = requests.request('POST', url_contacts + '/show', auth=admin_auth)
if len(response.json()) == 0:
    print('База данных очищена')
else:
    print('Ошибка при очистке базы данных')
    exit()

'''Создание дополнительных клиентов'''
response = requests.request('POST', url_listUsers, auth=admin_auth, data={"login": "Admin2", "password": "Qwerty123", "role": "a"})
response = requests.request('POST', url_listUsers, auth=admin_auth, data= {"login": "DefaultUser1", "password": "PassUser1", "role": "d"})
response = requests.request('POST', url_listUsers, auth=admin_auth, data= {"login": "DefaultUser2","password": "PassUser2"})  # проверка присвоения роли стандартного пользователя по умолчанию

'''Наполнение контактами с файла JSON'''
contact_creator('contacts_for_DefaultUser1.json', 'DefaultUser1', 'PassUser1')
contact_creator('contacts_for_DefaultUser2.json', 'DefaultUser2', 'PassUser2')

'''Удаление контакта администратором'''
response = requests.request('POST', url_contacts + '/show', data ={'filters': '{"name": "Виктор", "deleted": false}'}, auth=admin_auth)
res_json = response.json()
if not len(res_json) == 1 or not res_json[0]['name'] == 'Виктор':
    print('При удалении администратором результат отличаеться от ожидаемого!')
    exit()
contact_id = res_json[0]['id']
response = requests.request('DELETE', url_contacts + '/' + str(contact_id), auth=admin_auth)
response = requests.request('POST', url_contacts + '/show', data ={'filters': '{"name": "Виктор"}'}, auth=admin_auth)
if not response.json()[0]['deleted']:
    print(f'Не удалось выполнить удаление контакта id {str(contact_id)} администратором!')
    exit()

'''Удаление контакта стандартным пользователем'''
response = requests.request('POST', url_contacts + '/show', auth=admin_auth)
res_json = response.json()
if not len(res_json) == 1 or not res_json[0]['name'] == 'Дмитрий':
    print('При удалении стандартным пользователем результат отличаеться от ожидаемого!')
    exit()
response = requests.request('DELETE', url_contacts + '/' + str(contact_id), auth=admin_auth)
response = requests.request('POST', url_contacts + '/show', data ={'filters': '{"name": "Дмитрий"}'}, auth=admin_auth)
print(response.json())
if not len(response.json()) == 0:
    print(f'Не удалось выполнить удаление контакта id {str(contact_id)} стандартным пользователем!')
    exit()

print('База данных заполнена')



