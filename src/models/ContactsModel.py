from src.database.db import get_connection
from src.models.entities.Contact import Contact


class ContactsModel:
    def add_contact(contact: Contact):
        """Добавляет нового пользователя. Возвращает None при успешном добавлении или текст ошибки в случае неудачи"""

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO contacts (name, last_name, patronymic, organization, post, email, phone, holder_id) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (
                        contact.name,
                        contact.last_name,
                        contact.patronymic,
                        contact.organization,
                        contact.post,
                        contact.getEmail(),
                        contact.getPhone(),
                        contact.holder,
                    ),
                )
                connection.commit()
            return None
        except Exception as ex:
            print(ex)
            return ex

    @staticmethod
    def delete_contact_irrevocably(id, holder=None):
        """
        Удаляет контакт из БД по его id.
        holder - это id пользователя кто владеет контактом (защита от удаления чужих контактов)
        Если holder не указан (то есть holder='*') - защита удаления чужих контактов не задействована
        """

        str_SQL = f"DELETE FROM contacts WHERE id = {id}"
        if holder:
            str_SQL += f"AND holder_id = {holder}"
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(str_SQL)
                connection.commit()
                if cursor.statusmessage == 'DELETE 0':
                    return f'Удаление контакта с id "{id}" не удалось. Проверьте корректность указанного id контакта'
            return None
        except Exception as ex:
            print(ex)
            return ex

    @staticmethod

    def show_contascts(list_columns=['*'], search='', sort='', typeSort='', obj_filters=None):
        """
        Запрос нужных контактов

        list_columns - колонки которые будут получены с SQL
        search - строка полнотекстового поиска
        sort - параметр сортировки
        typeSort - тип сортировки (reverse/standart)
        obj_filters - словарь для фильтрации, где ключ - имя колонки, а значение - условие фильтрации.
        """

        columns = ",".join(list_columns)
        str_filter = ''
        if obj_filters:
            str_filter = ''
            for parametr in obj_filters:
                if str_filter:
                    str_filter += ' AND '
                if (
                    parametr == 'deleted' or parametr == 'holder_id'
                ):  # отдельное условие сравнения для служебных параметров
                    str_filter += f"{parametr} = '{obj_filters[parametr]}' "
                    continue
                str_filter += f"{parametr} ~* '{obj_filters[parametr]}' "
        str_sort = ''

        str_search = ''
        if search:
            str_search = f"tsv @@ plainto_tsquery('russian', '{search}');"
        str_SQL = ''
        if str_filter:
            str_SQL += str_filter
        if str_search:
            if str_SQL:
                str_SQL += ' AND '
            str_SQL += str_search
        if str_SQL:
            str_SQL = ' WHERE ' + str_SQL

        # то что не требует WHERE и AND:
        if sort:
            str_sort = ' ORDER BY ' + sort
            if typeSort == 'reverse':
                str_sort += ' DESC'
        if str_sort:
            str_SQL += str_sort

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT " + columns + " FROM contacts" + str_SQL)
                rows = cursor.fetchall()
            return {'contacts': rows, 'err': ''}
        except Exception as ex:
            print(ex)
            return {'contacts': None, 'err': ex}

    @staticmethod
    def make_obj_contacts(list_columns, list_contacts):
        """Делает из полученных от SQL данных именованный массив в формате выдачи."""

        obj_contacts = []
        len_columns = len(list_columns)

        for contact in list_contacts:
            obj = {}
            column = 0
            while column < len_columns:
                if not contact[column] is None:
                    obj[list_columns[column]] = contact[column]
                column += 1
            obj_contacts.append(obj)
        return obj_contacts

    @staticmethod
    def update_contact(contact_id, dict_parametrs, holder=None):
        """
        Изменяет контакт по его id.
        holder - это id пользователя кто владеет контактом (защита от изменения чужих контактов)
        Если holder не указан (то есть holder='*') - защита удаления чужих контактов не задействована
        """

        str_SQL = f'UPDATE contacts SET '
        for parametr in dict_parametrs:
            str_SQL += f"{parametr} = '{dict_parametrs[parametr]}',"
        str_SQL = str_SQL[:-1] + f' WHERE id = {contact_id}'
        if holder:
            str_SQL += f' AND holder_id = {holder}'
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(str_SQL)
                connection.commit()
                if cursor.statusmessage == "UPDATE 0":
                    return (
                        f'Невозможно выполнить изменение контакта "{contact_id}". Проверьте корректность id.'
                    )
            return None
        except Exception as ex:
            print(ex)
            return ex

    @staticmethod
    def clear_contacts():
        """Очистка БД контактов (только для DEBUG режима)"""

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('TRUNCATE contacts')
                connection.commit()
            return None
        except Exception as ex:
            print(ex)
            return ex
