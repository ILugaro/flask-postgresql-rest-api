from models.ContactsModel import ContactsModel
from werkzeug.security import generate_password_hash, check_password_hash
from abc import ABC, abstractmethod

class User(ABC):
    @staticmethod
    def make_hashPassword(password):
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    def check_password(self, password):
        return check_password_hash(self.hashPassword, password)

    '''Абстрактные методы класса'''

    @abstractmethod
    def show(self, search='', sort='', typeSort='', obj_filters={}):
        pass
    @abstractmethod
    def delete(self, contact_id):
        pass

    @abstractmethod

    def delete_contact_irrevocably(contact_id):
        pass
    @abstractmethod
    def update_contact(self, contact_id, dict_parametrs):
        pass
    @abstractmethod
    def add_contact(self, new_contact):
        pass




class Default_user(User):
    '''Класс обычного пользователя со стандартными правами'''
    def __init__(self, login, hashPassword) -> None:
        self.login = login
        self.hashPassword = hashPassword
        self.userId = None
        self.role = 'd'

    # search - строка полнотекстового поиска
    # sort - параметр по которому происходит сортировка
    # typeSort - тип сортировки (reverse/standart)
    # obj_filters - словарь для фильтрации контактов, где ключ это параметр (имя столбца таблицы SQL), а значение - критерий фильтрации.
    #    Контакт проходит отбор при полном соответствии требуемому значению.
    def show(self, search='', sort='', typeSort='', obj_filters={}):

        columns = ['id', 'name', 'last_name', 'patronymic', 'organization', 'post', 'email', 'phone'] # ограничиваю доступную информацию
        obj_filters['holder_id'] = self.userId  # искать только среди контактов пользователя
        obj_filters['deleted'] = False  # не показывать удаленные контакты

        obj_data = ContactsModel.show_contascts(columns, search, sort, typeSort, obj_filters)
        if obj_data['err']: return obj_data
        listOfContacts = ContactsModel.make_obj_contacts(columns, obj_data['contacts'])
        return {'contacts': listOfContacts, 'err': ''}

    def delete(self, contact_id):
        '''Делает для контакта статус "удален", но не удаляет из БД'''
        return ContactsModel.update_contact(contact_id, {'deleted': True}, self.userId)
    @staticmethod
    def delete_contact_irrevocably():
        '''Безвозвратное удаление'''
        return 'Операция недоступна для пользователя со стандартными правами.'

    def add_contact(self, new_contact):
        if new_contact.holder and not new_contact.holder == self.userId: 'Недопустимое значение "holder"! Укажите свой id клиента или не используйте в запросе.'
        new_contact.holder = self.userId
        return ContactsModel.add_contact(contact=new_contact)


    # list_parametrs = []  # список параметров которые необходимо изменить
    # list_values = () соответствующие им значения
    def update_contact(self, contact_id, dict_parametrs):
        '''Измененние существующего контакта по набору параметров'''
        if 'holder_id' in dict_parametrs: return 'Операция недоступна для пользователя со стандартными правами.'
        return ContactsModel.update_contact(contact_id, dict_parametrs, self.userId)

class Admin(User):

    def __init__(self, login, hashPassword) -> None:
        self.login = login
        self.hashPassword = hashPassword
        self.role = 'a'
        self.userId = None

    # search - строка полнотекстового поиска
    # sort - параметр по которому происходит сортировка
    # typeSort - тип сортировки (reverse/standart)
    # obj_filters - словарь для фильтрации контактов, где ключ это параметр (имя столбца таблицы SQL), а значение - критерий фильтрации.
    #    Контакт проходит отбор при полном соответствии требуемому значению.
    def show(self, search='', sort='', typeSort='', obj_filters={}):
        columns = ['id', 'name', 'last_name', 'patronymic', 'organization', 'post', 'email', 'phone', 'deleted', 'holder_id']
        obj_data = ContactsModel.show_contascts(columns, search, sort, typeSort, obj_filters)
        if obj_data['err']: return obj_data
        listOfContacts = ContactsModel.make_obj_contacts(columns ,obj_data['contacts'])
        return {'contacts': listOfContacts, 'err': ''}

    def delete(self, contact_id):
        '''Делает для контакта статус "удален", но не удаляет из БД'''
        return ContactsModel.update_contact(contact_id, {'deleted': True})

    @staticmethod
    def delete_contact_irrevocably(contact_id, holder_id=None):
        '''Безвозвратное удаление'''
        return ContactsModel.delete_contact_irrevocably(contact_id, holder_id)

    def add_contact(self, new_contact):
        if not new_contact.holder: new_contact.holder = self.userId
        return ContactsModel.add_contact(contact=new_contact)

    # list_parametrs = []  # список параметров которые необходимо изменить
    # list_values = () соответствующие им значения
    def update_contact(self, contact_id, dict_parametrs):
        '''Измененние существующего контакта по набору параметров'''
        return ContactsModel.update_contact(contact_id, dict_parametrs)
