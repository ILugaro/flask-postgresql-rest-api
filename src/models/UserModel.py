from database.db import get_connection


class UserModel:
    """Клас для работы с таблицой users - добавление, удаление, получение информации"""

    @classmethod
    def userInfo(self, login):
        """Возвращает экземпляр User пользователя от которого пришел API запрос (или None если пользователя нет),
        для будущей проверки его пароля или роли"""
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""SELECT id, password, role FROM users WHERE login = %s""", (login,))
                row = cursor.fetchone()
            return row
        except Exception as ex:
            print(ex)
            return ex

    @classmethod
    def addNewUser(self, user):
        """Добавляет нового пользователя. Возвращает None при успешном добавлении или текст ошибки в случае неудачи"""
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO users (login, password, role) 
                                VALUES (%s, %s, %s)""", (user.login, user.hashPassword.split(':')[-1], user.role))
                connection.commit()
            return None
        except Exception as ex:
            print(ex)
            return ex

    @classmethod
    def delUser(self, login):
        """Удаляет пользователя. Возвращает None при успешном удалении или текст ошибки в случае неудачи"""
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE login = %s", (login,))
                connection.commit()
            return None
        except Exception as ex:
            print(ex)
            return ex
