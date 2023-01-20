from flask import Flask

from config import config

# Routes
from routes import contacts
from routes import userList

app = Flask(__name__)

def page_not_found(error):
    return "<h1>Not found page</h1>", 404

@app.route('/')
def hello_world():
    return 'Flask Dockerized123'


if __name__ == '__main__':
    app.config.from_object(config['development'])

    # Blueprints
    app.register_blueprint(contacts.main, url_prefix='/api/contacts')  # операции с контактами
    app.register_blueprint(userList.main, url_prefix='/api/userList')  # операции со списком пользователей REST API

    # Обработчик ошибок
    app.register_error_handler(404, page_not_found)
    app.run(host='0.0.0.0')
