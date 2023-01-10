"""endpoint /userList - REST для управляения списком пользователей в SQL таблице users"""
from flask import Blueprint, request, abort, make_response

main = Blueprint('userList_blueprint', __name__)

from models.UserModel import UserModel

# Entities
from models.entities.User import User
from models.entities.User import Admin
from models.entities.User import Default_user
from models.ContactsModel import ContactsModel
from config import DevelopmentConfig


def admin_only(f):
    def wrapper(*args, **kwargs):
        if not request.authorization: abort(make_response('Требуется basic авторизация по логину и паролю'), 403)
        info_user = UserModel.userInfo(request.authorization["username"])
        if not info_user: abort(make_response('Пользователь не найден'), 403)
        # создания экзампляра Admin или Default_user в зависимости от роли клиента
        if info_user[2] == 'a': user = Admin(request.authorization["username"], 'pbkdf2:sha256:' + info_user[1])
        elif info_user[2] == 'd': user = Default_user(request.authorization["username"], 'pbkdf2:sha256:' + info_user[1])

        if not user.check_password(request.authorization["password"]): abort(make_response('Неверный пароль'), 403)
        if not user.role == 'a':
            abort(make_response('Для данной операции необходимы права администратора'), 403)
        return f(user, *args, **kwargs)
    wrapper.__name__ = f.__name__  # что бы не было ошибки AssertionError
    return wrapper

def debug_only(f):
    '''функция будет выполнена только при установке в файле config.py: DEBUG = True'''
    def wrapper(*args, **kwargs):
        if not DevelopmentConfig.DEBUG: abort(make_response('Очистка БД возможно только в режиме DEBUG'), 403)
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__  # что бы не было ошибки AssertionError
    return wrapper

@main.route('/', methods=['POST'])
@admin_only
def addNewUser(user):
    MUST_HAVE = ['login', 'password'];  # обязательные параметры
    MAY_HAVE = ['login', 'password', 'role'];  # возможные параметры
    for parametr in MUST_HAVE:
        if not parametr in request.form:
            abort(make_response(f'Отсутствует обязательный параметр: "{parametr}"', 400))
    for parametr in request.form:
        if not parametr in MAY_HAVE:
            abort(make_response(f'Неизвестный параметр: "{parametr}"', 400))
    login = request.form['login']
    if UserModel.userInfo(login): abort((make_response(f'Пользователь с  логином {login} уже существует!')), 400)

    password = request.form['password']
    if len(password) < 6:
        abort((make_response('Длина пароля должна быть более шести символов!')), 400)
    if password.isdigit():
        abort((make_response('Пароль не должен состоять только из цифр!')), 400)

    if 'role' in request.form: role = request.form['role']
    else: role = 'd'  # по умолчанию пользователь з дефолтными правами

    if role == 'a':
        newUser = Admin(login, User.make_hashPassword(password))
    elif role == 'd':
        newUser = Default_user(login, User.make_hashPassword(password))
    else:
        abort((make_response('Значение "role" может быть только "d"(client) или "a"(admin)')), 400)

    err = UserModel.addNewUser(newUser)
    if err: abort(make_response(str(err)), 500)
    return (f'Пользователь {newUser.login} добавлен.', 201)


@main.route('/<login>', methods=['DELETE'])
@admin_only
def delUser(user, login):
    if not UserModel.userInfo(login):
        abort((make_response(f'Пользователь с логином {login} отсутствует!')), 400)
    err = UserModel.delUser(login)  # вернет None в случае успеха
    if err: abort(make_response(str(err)), 500)
    return ('', 204)  # статус 204 отправляется без сообщения



@main.route('/reset', methods=['POST'])
@debug_only
@admin_only
def reset(user):
    '''Используеться для тестирования, только в режиме DEBUG (файл config.py). Удаляет все контакты и всех клиентов кроме клиента выполняющего данный запрос'''
    err = ContactsModel.clear_contacts()  # вернет None в случае успеха
    if err: abort(make_response(str(err)), 500)
    err = UserModel.clear_users(user.login) # вернет None в случае успеха
    if err: abort(make_response(str(err)), 500)
    return ('База данных очищена.', 200)
