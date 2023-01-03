import re


class Contact:
    def __init__(self):
        self.name = None
        self.last_name = None
        self.patronymic = None
        self.organization = None
        self.post = None
        self.email = None
        self.__phone = None
        self.holder = None

    def setPhone(self, phone):
        if type(phone) == 'number':
            phone = str(phone)
        else:
            phone = re.sub("[-|(|)]", "", phone)
            if phone[0] == '+':
                phone.slice[0]
            if not phone.isdigit():
                return 'Неверный формат номера'
        self.__phone = phone
