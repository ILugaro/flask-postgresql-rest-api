Сервер работает с двумя endpoint (назначение в app.js):
"/api/userList" - работа с авторотационными данными пользователей API сервиса
"/api/contacts" - работа непосредственно с базой контактов

В папке "src\models\entities" есть 2 сущности:
Contact.py - сущность контакта, его поля и методы обработки входящей информации (изменение формата тел. номера)
User.py - сущность, где прописано разделение логики работы с контактами для админов и простых пользователей.

В папке "src\models" в файлах ContactsModel.py и UserModel.py в основном содержатся методы работы с БД.
ContactsModel.py - с SQL таблицей "contacts"
UserModel.py - с SQL таблицей "users"


В настойках env должны быть поля:

SECRET_KEY
PGSQL_HOST
PGSQL_USER
PGSQL_PASSWORD
PGSQL_DATABASE
