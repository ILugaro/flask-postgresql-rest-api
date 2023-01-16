from flask import Blueprint, request, abort, make_response
import json

main = Blueprint('contacts_blueprint', __name__)

from models.UserModel import UserModel

# Entities
from models.entities.User import Admin
from models.entities.User import Default_user
from models.entities.Contact import Contact


def authentication(f):
    '''Проверка логина и пароля. В случае успеха возвращает экземпляр клиента, в ином случае прерывает запрос'''
    def wrapper(*args, **kwargs):
        if not request.authorization: abort(make_response('Требуется basic авторизация по логину и паролю', 403))
        dict_info_user = UserModel.userInfo(request.authorization["username"])
        if dict_info_user['err']: abort(make_response(dict_info_user['err'], 500))
        info_user = dict_info_user['data']
        if not info_user: abort(make_response('Неверный логин', 403))

        # создания экзампляра Admin или Default_user в зависимости от роли клиента
        if info_user[2] == 'a':
            user = Admin(request.authorization["username"], 'pbkdf2:sha256:' + info_user[1])
        elif info_user[2] == 'd':
            user = Default_user(request.authorization["username"], 'pbkdf2:sha256:' + info_user[1])
        user.userId = info_user[0]
        if not user.check_password(request.authorization["password"]): abort(make_response('Неверный пароль!', 403))

        return f(user,*args, **kwargs)

    wrapper.__name__ = f.__name__  # что бы не было ошибки AssertionError
    return wrapper


@main.route('/show', methods=['POST'])
@authentication
def show(user):
    '''запрос контактов'''
    dict_params = {'search': '', 'sort': '', 'typeSort': '', 'filters': {}}
    for parametr in request.form:
        if not (parametr in dict_params):
            abort(make_response(f'Неизвестный параметр: "{parametr}"', 400))
        if parametr == 'filters':
            dict_params[parametr] = json.loads(request.form[parametr])
            continue
        if parametr == 'typeSort':
            if not 'sort' in request.form: abort(make_response('Указан "typeSort" без указания параметра "sort"', 400))
            if not (request.form['typeSort'] == 'standart' or 'reverse'): return abort(make_response('Недопустимое значение "typeSort". Укажите "standart" или "reverse".', 400))
        dict_params[parametr] = request.form[parametr]
    data = user.show(dict_params['search'], dict_params['sort'], dict_params['typeSort'], dict_params['filters'])
    if data['err']: abort(make_response(data['err'], 500))
    return data['contacts']


@main.route('/add', methods=['POST'])
@authentication
def add(user):
    '''добавление нового контакта'''
    # проверка корректности запроса
    MAY_EXIST = ['name', 'last_name', 'patronymic', 'organization', 'post', 'email', 'phone', 'holder' ]
    for parametr in request.form:
        if not (parametr in MAY_EXIST):
            abort(make_response(f'Неизвестный параметр: "{parametr}"', 400))

    new_contact = Contact()
    for parametr in request.form:
        if parametr == 'phone':
            err = new_contact.setPhone(request.form[parametr])  # вернет None в случае успеха
            if err: abort(make_response(str(err), 400))
            continue
        if parametr == 'email':
            err = new_contact.setEmail(request.form[parametr]) # вернет None в случае успеха
            if err: abort(make_response(str(err), 400))
            continue
        new_contact[parametr] = request.form[parametr]

    err = user.add_contact(new_contact=new_contact) # вернет None в случае успеха
    if err: abort(make_response(str(err), 400))
    return (f'Новый контакт добавлен.', 201)



@main.route('/<contact_id>', methods=['DELETE'])
@authentication
def delete(user, contact_id):
    '''удаление контакта'''
    if 'irrevocable' in request.form and request.form['irrevocable']:  # если запрашивается безвозвратное удаление
        err = user.delete_contact_irrevocably(contact_id) # вернет None в случае успеха
    else:
        err = user.delete(contact_id) # вернет None в случае успеха
    if err: abort(make_response(str(err), 400))
    return ('', 204)  # статус 204 отправляется без сообщения

@main.route('/<contact_id>', methods=['PUT'])
@authentication
def update_contact(user, contact_id):
    '''изменение существующего контакта'''
    dict_parametrs = {}
    temp_contact = Contact()

    # проверка корректности запроса
    MAY_EXIST = ['name', 'last_name', 'patronymic', 'organization', 'post', 'email', 'phone', 'holder_id']
    for parametr in request.form:
        if not (parametr in MAY_EXIST):
            abort(make_response(f'Неизвестный параметр: "{parametr}"', 400))

        if parametr == 'phone':
            err = temp_contact.setPhone(request.form[parametr])  # вернет None в случае успеха
            if err: abort(make_response(str(err), 400))
            dict_parametrs[parametr] = temp_contact.getPhone()
            continue
        if parametr == 'email':
            err = temp_contact.setEmail(request.form[parametr])  # вернет None в случае успеха
            if err: abort(make_response(str(err), 400))
            dict_parametrs[parametr] = temp_contact.getEmail()
            continue
        dict_parametrs[parametr] = request.form[parametr]

    err = user.update_contact(contact_id, dict_parametrs) # вернет None в случае успеха
    if err: abort(make_response(str(err), 400))
    return (f'Контакт id {contact_id} был изменен.', 200)
