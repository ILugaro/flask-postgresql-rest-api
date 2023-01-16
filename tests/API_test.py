'''
Тестирование работает только в режиме DEBUG (параметр в файле config.py)
При старте тестирования происходит очистка существующей БД и создается тестовая БД
contacts_for_DefaultUser1.json - база контактов для первого пользователя
contacts_for_DefaultUser2.json - база контактов для второго пользователя
show_test.json - список тестов для POST запроса получения контактов
Структура  show_test.json:
    Каждый словарь - это POST запрос.
    request - это имя теста(target) и выходные данные (запрос и логин/пароль пользователя)
    response - это ожидаемый ответ.
        count - количество контактов в ответе,
        check_data - обязательный параметр в каждом контакте
        status - полученный http код
'''
import requests
from requests.auth import HTTPBasicAuth
import json

url_contacts = 'http://127.0.0.1:5000/api/contacts'
url_listUsers = 'http://127.0.0.1:5000/api/userList'
admin_auth = HTTPBasicAuth('firstAdmin', 'DHsh234ui')
DefaultUser1_auth = HTTPBasicAuth('DefaultUser1', 'PassUser1')
DefaultUser2_auth = HTTPBasicAuth('DefaultUser2', 'PassUser2')


with open('contacts_for_DefaultUser1.json', encoding='utf-8') as f:
    contacts_user_1 = json.load(f)
with open('contacts_for_DefaultUser2.json', encoding='utf-8') as f:
    contacts_user_2 = json.load(f)

with open('show_test.json', encoding='utf-8') as f:
    show_tests = json.load(f)

def contact_creator(contacts, login, password):
    '''создает базу контактов на основе списка с объектами. От имени пользователя login (password - пароль данного клиента)'''
    basic = HTTPBasicAuth(login, password)
    for contact in contacts:
        response = requests.request('POST', url_contacts + '/add', data=contact, auth=basic)

def show(task):
    auth = HTTPBasicAuth(task['requests']['client']['login'], task['requests']['client']['pass'])
    response = requests.request('POST', url_contacts + '/show', data=task["requests"]["data"], auth=auth)
    if not response.status_code == task['response']['status']:
        return f'Для теста "{task["requests"]["target"]}" несоответствующий код ответа ( получен код: {response.status_code})'
    if task['response']["count"] and not task['response']["count"] == len(response.json()):
        return f'Количество полученных контактов не соотвтетствует ожидаемому количеству в тесте "{task["requests"]["target"]}".'
    if task['response']["check_data"]:
        dict_check_data = task['response']["check_data"]
        req = response.json()
        for check in dict_check_data:
            for contact in req:
                if not contact[check] ==  dict_check_data[check]:
                    return f'Полученный контакты в тесте {task["requests"]["target"]} не соответствуют ожидаемым!'
    return None


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
contact_creator(contacts_user_1, 'DefaultUser1', 'PassUser1')
contact_creator(contacts_user_2, 'DefaultUser2', 'PassUser2')

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
response = requests.request('POST', url_contacts + '/show', data ={'filters': '{"name": "Дмитрий", "deleted": false}'}, auth=admin_auth)
res_json = response.json()
contact_id = res_json[0]['id']
if not len(res_json) == 1 or not res_json[0]['name'] == 'Дмитрий':
    print('При удалении стандартным пользователем результат отличаеться от ожидаемого!')
    exit()

response = requests.request('DELETE', url_contacts + '/' + str(contact_id), auth=DefaultUser1_auth)
response = requests.request('POST', url_contacts + '/show', data ={'filters': '{"name": "Дмитрий"}'}, auth=DefaultUser1_auth)
if len(response.json()):
    print(f'Не удалось выполнить удаление контакта id {str(contact_id)} стандартным пользователем!')
    exit()

print('База данных заполнена')

'''Проверка функионала получения контактов. Тесты из файла show_test.json'''
for task in show_tests:
    err = show(task)  # в случае успешного прохождения теста - возвращает None
    if err:
        print(err)
        exit()

print()
print('Тестирование успешно звершено.')

