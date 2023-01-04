import re


class Contact:
    def __init__(self):
        self.name = None
        self.last_name = None
        self.patronymic = None
        self.organization = None
        self.post = None
        self._email = None
        self._phone = None
        self.holder = None

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def setPhone(self, phone):
        if type(phone) == 'number':
            phone = str(phone)
        else:
            phone = re.sub("[-|(|)| r'\s+']", "", phone)
            if phone[0] == '+':
                phone.slice[0]
            if not phone.isdigit():
                return 'Неверный формат номера'
        self._phone = phone

    def getPhone(self):
        return self._phone

    def setEmail(self, email):
        email = email.strip()
        if '@' in email and '.' in email:
            self._email = email
        else: return 'Неверный формат email'

    def getEmail(self):
        return  self._email