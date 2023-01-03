from flask import Blueprint, request, abort, make_response

main = Blueprint('contacts_blueprint', __name__)

from models.UserModel import UserModel

# Entities
from models.entities.User import Admin
from models.entities.User import Default_user

def authentication(f):
    def wrapper():
        if not request.authorization: abort(make_response('Требуется basic авторизация по логину и паролю'), 403)
        info_user = UserModel.userInfo(request.authorization["username"])
        if not info_user: abort(make_response('Пользователь не найден'), 403)

        # создания экзампляра Admin или Default_user в зависимости от роли клиента
        if info_user[1] == 'a': user = Admin(request.authorization["username"], 'pbkdf2:sha256:' + info_user[0])
        elif info_user[1] == 'd': user = Default_user(request.authorization["username"], 'pbkdf2:sha256:' + info_user[0])

        if not user.check_password(request.authorization["password"]): abort(make_response('Неверный пароль'), 403)

        return f(user)
    wrapper.__name__ = f.__name__  # что бы не было ошибки AssertionError
    return wrapper



@main.route('/show', methods=['POST'])
@authentication
def show(user):

    return 'test'







    

