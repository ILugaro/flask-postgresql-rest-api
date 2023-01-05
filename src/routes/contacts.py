from flask import Blueprint, request, abort, make_response
import json

main = Blueprint('contacts_blueprint', __name__)

from models.UserModel import UserModel

# Entities
from models.entities.User import Admin
from models.entities.User import Default_user
from models.entities.Contact import Contact


def authentication(f):
    def wrapper():
        if not request.authorization: abort(make_response('Требуется basic авторизация по логину и паролю'), 403)
        info_user = UserModel.userInfo(request.authorization["username"])
        if not info_user: abort(make_response('Пользователь не найден'), 403)

        # создания экзампляра Admin или Default_user в зависимости от роли клиента
        if info_user[2] == 'a':
            user = Admin(info_user[0], request.authorization["username"], 'pbkdf2:sha256:' + info_user[1])
        elif info_user[2] == 'd':
            user = Default_user(info_user[0], request.authorization["username"], 'pbkdf2:sha256:' + info_user[1])

        if not user.check_password(request.authorization["password"]): abort(make_response('Неверный пароль'), 403)

        return f(user)

    wrapper.__name__ = f.__name__  # что бы не было ошибки AssertionError
    return wrapper


@main.route('/show', methods=['POST'])
@authentication
def show(user):
    dict_params = {'search': '', 'sort': '', 'typeSort': '', 'filters': None}
    for parametr in request.form:
        if not (parametr in dict_params):
            abort(make_response(f'Неизвестный параметр: "{parametr}"', 400))
        if parametr == 'filters':
            dict_params[parametr] = json.loads(request.form[parametr])
            continue
        dict_params[parametr] = request.form[parametr]
    data = user.show(dict_params['search'], dict_params['sort'], dict_params['typeSort'], dict_params['filters'])
    if data['err']: abort(data['err'], 500)
    return data['contacts']


@main.route('/add', methods=['POST'])
@authentication
def add(user):
    # проверка корректности запроса
    MAY_EXIST = ['name', 'last_name', 'patronymic', 'organization', 'post', 'email', 'phone', 'holder' ]
    for parametr in request.form:
        if not (parametr in MAY_EXIST):
            abort(make_response(f'Неизвестный параметр: "{parametr}"', 400))

    new_contact = Contact()
    for parametr in request.form:
        if parametr == 'phone':
            err = new_contact.setPhone(request.form[parametr])  # вернет None в случае успеха
            if err: abort(make_response(err, 400))
            continue
        if parametr == 'email':
            err = new_contact.setEmail(request.form[parametr]) # вернет None в случае успеха
            if err: abort(make_response(err, 400))
            continue
        new_contact[parametr] = request.form[parametr]


    err = user.add_contact(new_contact=new_contact) # вернет None в случае успеха
    if err: abort(make_response(str(err), 400))
    return (f'Новый контакт добавлен.', 201)
