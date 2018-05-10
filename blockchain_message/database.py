import shelve
from typing import List

from blockchain_message.core import Contact, Message


class MessageNotFoundException(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class Database (object):
    def __init__(self):
        """

        """
        with shelve.open("~/.blkchnmsg/db") as db:
            self.contacts: List[Contact] = db['contacts']
            self.messages: List[Message] = db['messages']

    def __pull(self):
        """

        """
        with shelve.open("~/.blkchnmsg/db") as db:
            self.contacts: List[Contact] = db['contacts']
            self.messages: List[Message] = db['messages']

    def __commit(self):
        """

        """
        with shelve.open("~/.blkchnmsg/db") as db:
            db['contacts']: List[Contact] = self.contacts
            db['messages']: List[Message] = self.messages

    def __max_msgid(self) -> int:
        """

        :return:
        """
        m: int = 0
        for x in self.messages:
            if x.id > m:
                m = x.id
        return m

    def add_contact(self, uname: str, addr: str, email: str) -> bool:
        """

        :param uname:
        :param addr:
        :param email:
        :return:
        """
        self.contacts.append(Contact(addr, uname, email))
        self.__commit()
        return True

    def del_contact(self, name: str) -> bool:
        """

        :param name:
        :return:
        """
        for x in self.contacts:
            if x.uname is name:
                self.contacts.remove(x)
                self.__commit()
                return True
        return False

    def insert(self, to: Contact, fr: Contact, text: str) -> bool:
        """

        :param to:
        :param fr:
        :param text:
        :return:
        """
        self.messages.append(Message(self.__max_msgid()+1, to, fr, text))
        self.__commit()
        return True

    def delete(self, msgid: int) -> bool:
        """

        :param msgid:
        :return:
        """
        for x in self.messages:
            if x.id is msgid:
                self.messages.remove(x)
                self.__commit()
                return True
        return False

    def read(self, msgid: int) -> Message:
        """

        :param msgid:
        :return:
        """
        for x in self.messages:
            if x.id is msgid:
                return x
        raise MessageNotFoundException


if __name__ == '__main__':
    import doctest
    doctest.testmod()
