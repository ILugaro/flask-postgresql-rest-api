from models.ContactsModel import ContactsModel
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
        columns = ['id', 'name', 'last_name', 'patronymic', 'organization', 'post', 'email', 'phone'] # ограничиваю доступную информацию
        obj_filters.fk_holder_id = self.userId  # искать только среди контактов пользователя
        obj_filters.deleted = False  # не показывать удаленные контакты

        ContactsModel.show_contascts(columns, search, sort, typeSort, obj_filters)

        # сделать удаление служебной информации
        print('dfsdf')

    def delete(self, id):
        ContactsModel.delete_contact(id, self.userid)

    def add_contact(self, contact):
        contact.holder = self.userId
        ContactsModel.add_contact(contact, self.userId)

    def change_contact(self, contact, key):
        if not contact.holder:
            contact.holder = self.userId
        elif not contact.holder == self.userId:
            return "Невозможно изменить контакт другого пользователя"
        ContactsModel.contact(contact, key)


class Admin(User):

    def __init__(self, login, hashPassword) -> None:
        self.login = login
        self.hashPassword = hashPassword
        self.role = 'a'

    def show(self, search='', sort='', typeSort='', obj_filters=''):
        colums = ['id', 'name', 'last_name', 'patronymic', 'organization', 'post', 'email', 'phone', 'deleted']
        obj_data = ContactsModel.show_contascts(colums, search, sort, typeSort, obj_filters)
        if obj_data['err']: return obj_data
        listOfContacts = ContactsModel.make_obj_contacts(colums ,obj_data['contacts'])
        return {'contacts': listOfContacts, 'err':''}



    def delete(id):
        ContactsModel.delete_contact(id)

    def add_contact(contact):
        ContactsModel.add_contact(contact)

    def change_contact(contact, key):
        ContactsModel.contact(contact, key)
