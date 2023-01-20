ОПИСАНИЕ ЗАПРОСОВ:

Все запросы требуют Basic авторизацию:

showContacts (POST api/contacts/show) - получение контактов.
 Параметры:
	search - строка полнотекстового поиска для ИФО
	sort - параметр по которому будет происходить сортировка
	typeSort - тип сортировки, standart или reverse
	filters - Именованный массив для фильтрации, где ключ - имя колонки, а значение - условие фильтрации (например {"organization":"почта", "name":"Ольга"}).

addContacts (POST api/contacts/add) - добавление нового параметра
 Параметры:
	name
	last_name
	patronymic - отчество
	organization
	post
	email
	phone
	holder - владелец контакта (может указывать только администратор)

deleteContacts (DELETE api/contacts/<id контакта>) - удаление контакта
 Параметры:
	irrevocable - если True - безвозвратное удаление

updateContacts (PULL api/contacts/<id контакта>) - изменение контакта
 	В качестве параметров атребуты контакта и их новые значения
	
newUser (POST api/userList)
	login
	password
	role - "d" (по умолчанию) или "a". Стандартный пользователь или администратор соответственно. 

deleteUser (DELETE api/userList/<id пользователя>)

RESET (POST api/userList/reset/<id администратора>) - проводит очистку БД контактов и клиентов, кроме указанного администратора
	*Используеться только в режиме DEBUG
	

ОПИСАНИЕ КОДА:

Сервер работает с двумя endpoint (назначение в app.js):
"/api/userList" - работа с авторотационными данными пользователей API сервиса
"/api/contacts" - работа непосредственно с базой контактов

В папке "src\models\entities" есть 2 сущности:
Contact.py - сущность контакта, его поля и методы обработки входящей информации (изменение формата тел. номера)
User.py - сущность, где прописано разделение логики работы с контактами для админов и простых пользователей.

В папке "src\models" в файлах ContactsModel.py и UserModel.py в основном содержатся методы работы с БД.
ContactsModel.py - с SQL таблицей "contacts"
UserModel.py - с SQL таблицей "users"


В файле .env.example требуемые поля для .env

