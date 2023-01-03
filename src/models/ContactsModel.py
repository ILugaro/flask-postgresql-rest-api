from database.db import get_connection


class ContactModel():

    def add_contact(self, contact):
        """Добавляет нового пользователя. Возвращает None при успешном добавлении или текст ошибки в случае неудачи"""
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO contacts (name, last_name, patronymic, organization, post, email, phone, holder) 
                                VALUES (%s, %s, %s)""", (
                    contact.name, contact.last_name, contact.patronymic, contact.organization, contact.post,
                    contact.email,
                    contact.phone, contact.holder))
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

    def show_contascts(self, columns, search, sort, typeSort, obj_filters):
        str_filter = ''
        if obj_filters:
            str_filter = ''
            for parametr in obj_filters:
                if str_filter: str_filter += ' AND '
                str_filter += f'{parametr} = {obj_filters[parametr]} '
        str_sort = ''
        if sort:
            str_sort = 'ORDER BY ' + sort
            if typeSort == 'revers':
                str_sort += 'DESC'
        str_search = ''
        if search:
            str_search = f'AND tsv @@ plainto_tsquery("russian", {search});'

        str_SQL = ''
        if str_filter: str_SQL + str_filter
        if str_sort:
            if str_SQL: str_SQL += ' AND '
            str_SQL += str_sort
        if str_search:
            if str_SQL: str_SQL += ' AND '
            str_SQL += str_search
        if str_SQL: str_SQL = ' WHERE ' + str_SQL

        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute('SELECT ' + columns + ' FROM contacts WHERE' + str_SQL)
                row = cursor.fetchone()
            return row
        except Exception as ex:
            print(ex)
            return ex

    def change_contact(self, contact, key):

        try:
            connection = get_connection()

        except Exception as ex:
            print(ex)
            return ex
