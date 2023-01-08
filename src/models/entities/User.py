from models.ContactsModel import ContactsModel
from werkzeug.security import generate_password_hash, check_password_hash


class User:

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
        self.userId = None
        self.role = 'd'

    def show(self, search='', sort='', typeSort='', obj_filters={}):

        columns = ['id', 'name', 'last_name', 'patronymic', 'organization', 'post', 'email', 'phone'] # ограничиваю доступную информацию
        obj_filters.fk_holder_id = self.userId  # искать только среди контактов пользователя
        obj_filters.deleted = False  # не показывать удаленные контакты

        obj_data = ContactsModel.show_contascts(columns, search, sort, typeSort, obj_filters)
        if obj_data['err']: return obj_data
        listOfContacts = ContactsModel.make_obj_contacts(columns, obj_data['contacts'])
        return {'contacts': listOfContacts, 'err': ''}

    def delete(self, contact_id):
        ContactsModel.delete_contact(id, self.userId)

    def add_contact(self, new_contact):
        if new_contact.holder and not new_contact.holder == self.userId: 'Недопустимое значение "holder"! Укажите свой id клиента или не используйте в запросе.'
        new_contact.holder = self.userId
        return ContactsModel.add_contact(contact=new_contact)


    # list_parametrs = []  # список параметров которые необходимо изменить
    # list_values = () соответствующие им значения
    def update_contact(self, contact_id, dict_parametrs):
        '''Измененние существующего контакта по набору параметров'''
        ContactsModel.update_contact(contact_id, dict_parametrs, self.userId)

class Admin(User):

    def __init__(self, login, hashPassword) -> None:
        self.login = login
        self.hashPassword = hashPassword
        self.role = 'a'
        self.userId = None

    def show(self, search='', sort='', typeSort='', obj_filters={}):
        columns = ['id', 'name', 'last_name', 'patronymic', 'organization', 'post', 'email', 'phone', 'deleted']
        obj_data = ContactsModel.show_contascts(columns, search, sort, typeSort, obj_filters)
        if obj_data['err']: return obj_data
        listOfContacts = ContactsModel.make_obj_contacts(columns ,obj_data['contacts'])
        return {'contacts': listOfContacts, 'err': ''}



    def delete(self, contact_id):
        ContactsModel.show_contascts()
        return ContactsModel.delete_contact(contact_id)


    def add_contact(self, new_contact):
        if not new_contact.holder: new_contact.holder = self.userId
        return ContactsModel.add_contact(contact=new_contact)

    # list_parametrs = []  # список параметров которые необходимо изменить
    # list_values = () соответствующие им значения
    def update_contact(self, contact_id, dict_parametrs):
        '''Измененние существующего контакта по набору параметров'''
        ContactsModel.update_contact(contact_id, dict_parametrs)
