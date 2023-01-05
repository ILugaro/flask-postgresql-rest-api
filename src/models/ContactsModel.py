from database.db import get_connection


class ContactsModel:

    def add_contact(contact):
        """Добавляет нового пользователя. Возвращает None при успешном добавлении или текст ошибки в случае неудачи"""
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO contacts (name, last_name, patronymic, organization, post, email, phone, holder_id) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (
                    contact.name, contact.last_name, contact.patronymic, contact.organization, contact.post,
                    contact.getEmail(), contact.getPhone(), contact.holder))
                connection.commit()
            return None
        except Exception as ex:
            print(ex)
            return ex

    def delete_contact(self, id, holder):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM user WHERE id = %s AND fk_holder_id = %s", (id, holder))
                connection.commit()
            return None
        except Exception as ex:
            print(ex)
            return ex

    @staticmethod
    def show_contascts(list_columns =['*'], search='', sort='', typeSort='', obj_filters=None):
        columns = ",".join(list_columns)
        str_filter = ''
        if obj_filters:
            str_filter = ''
            for parametr in obj_filters:
                if str_filter: str_filter += ' AND '
                str_filter += f"{parametr} = '{obj_filters[parametr]}' "
        str_sort = ''

        str_search = ''
        if search:
            str_search = f"tsv @@ plainto_tsquery('russian', '{search}');"
        str_SQL = ''
        if str_filter:
            str_SQL += str_filter
        if str_search:
            if str_SQL: str_SQL += ' AND '
            str_SQL += str_search
        if str_SQL: str_SQL = ' WHERE ' + str_SQL

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
                print('SELECT ' + columns + ' FROM contacts' + str_SQL)
                cursor.execute("SELECT " + columns + " FROM contacts" + str_SQL)
                rows = cursor.fetchall()
            return {'contacts': rows, 'err': ''}
        except Exception as ex:
            print(ex)
            return {'contacts': None, 'err': ex}

    def change_contact(self, contact, key):

        try:
            connection = get_connection()

        except Exception as ex:
            print(ex)
            return ex

    @staticmethod
    def make_obj_contacts(list_columns, list_contacts):
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