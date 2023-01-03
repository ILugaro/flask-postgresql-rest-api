from models.UserModel import UserModel
from werkzeug.security import generate_password_hash, check_password_hash


class User():
    # запретить создание экземпляра

    def __init__(self, login, hashPassword) -> None:
        self.login = login
        self.hashPassword = hashPassword
        self.role = None
        self.userId = None

    def show(self):
        raise NotImplementError(f'В дочернем классе должен быть метод {self.__name__}')

    def delete(self):
        raise NotImplementError(f'В дочернем классе должен быть метод {self.__name__}')

    def change(self):
        raise NotImplementError(f'В дочернем классе должен быть метод {self.__name__}')

    def make_hashPassword(password):
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    def check_password(self, password):
        return check_password_hash(self.hashPassword, password)


class Default_user(User):
    def __init__(self, login, hashPassword) -> None:
        self.login = login
        self.hashPassword = hashPassword
        self.role = 'd'

    def show(self, search, sort, typeSort, obj_filters):
        COLUMNS = 'id, name, last_name, patronymic, organization, post, email, phone'  # ограничиваю доступную информацию
        obj_filters.fk_holder_id = self.userId  # искать только среди контактов пользователя
        obj_filters.deleted = False  # не показывать удаленные контакты

        UserModel.show_contascts(COLUMNS, search, sort, typeSort, obj_filters)

        # сделать удаление служебной информации
        print('dfsdf')

    def delete(self, id):
        UserModel.delete_contact(id, self.userid)

    def add_contact(self, contact):
        contact.holder = self.userId
        UserModel.add_contact(contact, self.userId)

    def change_contact(self, contact, key):
        if not contact.holder:
            contact.holder = self.userId
        elif not contact.holder == self.userId:
            return "Невозможно изменить контакт другого пользователя"
        UserModel.contact(contact, key)


class Admin(User):

    def __init__(self, login, hashPassword) -> None:
        self.login = login
        self.hashPassword = hashPassword
        self.role = 'a'

    def show(self, search, sort, typeSort, obj_filters):
        COLUMNS = '*'
        UserModel.show_contascts(COLUMNS, search, sort, typeSort, obj_filters)

    def delete(self, id):
        UserModel.delete_contact(id)

    def add_contact(contact):
        UserModel.add_contact(contact)

    def change_contact(contact, key):
        UserModel.contact(contact, key)
