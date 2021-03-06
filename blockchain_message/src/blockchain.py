import hashlib
from typing import List

from solc import compile_files
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

from blockchain_message.src.core import Message, Contact


class OutOfIdentitiesException(Exception):
    """
    Thrown when the system has run out of room for new identities.
    """

    def __init__(self, message):
        """
        Default constructor.
        :param message: The text of the exception detail.
        """
        super().__init__(message)


# noinspection PyUnresolvedReferences
class Blockchain(object):
    """
    Provides functions for interacting directly with the smart contract.
    """

    def __init__(self):
        """
        Sets up Ethereum interaction variables and compiles the contract, allowing web3 to call functions directly.
        """
        with open('./.blkchnmsg/contract', 'r') as f:
            self.addr = f.readline().strip()
            self.addr_2 = f.readline()
        compiled = compile_files(['./../contract/contracts/BlckChnMsgStorage.sol'])
        compiled_manager = compile_files(["./../contract/contracts/IdentityManager.sol"])
        self.contract_interface = compiled['./../contract/contracts/BlckChnMsgStorage.sol:BlckChnMsgStorage']
        self.manager_interface = compiled_manager["./../contract/contracts/IdentityManager.sol:IdentityManager"]
        self.w3 = Web3(HTTPProvider("http://localhost:7545"))
        self.contract = self.w3.eth.contract(abi=self.contract_interface['abi'],
                                             bytecode=self.contract_interface['bin'])
        self.manager_contract = self.w3.eth.contract(abi=self.manager_interface['abi'],
                                                     bytecode=self.manager_interface['bin'])

    def new_identity(self, uname: str, password: str) -> int:
        """

        :param uname:
        :param password:
        :return:
        """
        with open("./.blkchnmsg/{0}".format(uname), "w") as f:
            f.write(hashlib.sha224(bytes(password, 'utf8')).hexdigest())
        abi = self.manager_interface['abi']
        contract = self.w3.eth.contract(address=self.addr_2, abi=abi, ContractFactoryClass=ConciseContract)
        contract.new_identity(uname, transact={'from': self.w3.eth.accounts[0]})
        addr = contract.new_identity(uname)
        return addr

    def get_my_identity(self, uname: str, password: str) -> int:
        """
        Used to either log in or register a new identity.

        :param uname: The username we need the address for.
        :param password: The password used for authentication.
        :return: The unique identifier associated with uname.
        """
        abi = self.manager_interface['abi']
        contract = self.w3.eth.contract(address=self.addr_2, abi=abi, ContractFactoryClass=ConciseContract)
        addr = contract.get_identity(uname)
        if addr == 999:
            addr = self.new_identity(uname, password)
            return addr
        else:
            try:
                with open("./.blkchnmsg/{0}".format(uname), "r") as f:
                    pass_hash = f.readline()
                if hashlib.sha224(bytes(password, 'utf8')).hexdigest() == pass_hash:
                    return addr
                else:
                    return 99999
            except FileNotFoundError:
                return 999999

    def get_identity(self, uname: str) -> int:
        """

        :param uname: The username we need the address for.
        :return: The unique identifier associated with uname.
        """
        abi = self.manager_interface['abi']
        contract = self.w3.eth.contract(address=self.addr_2, abi=abi, ContractFactoryClass=ConciseContract)
        return contract.get_identity(uname)

    def get_balance(self) -> float:
        """

        :return: The current ETH balance.
        """
        return self.w3.eth.getBalance(self.w3.eth.accounts[0])

    def submit(self, message: Message):
        """
        Commits a transaction to the blockchain that enacts sending a message.
        :param message: The message object being sent across Ethereum.
        """
        abi = self.contract_interface['abi']
        contract = self.w3.eth.contract(address=self.addr, abi=abi, ContractFactoryClass=ConciseContract)

        msg_id = message.id
        to_user = message.to.uname
        fr_user = message.fr.uname
        msg_text = message.text
        sign = message.sign
        message_body = ('{0}♣{1}♣{2}♣{3}♣{4}'.format(msg_id, to_user, fr_user, msg_text, sign))
        message_body.encode('utf8')

        to_user = int(message.to.address)
        contract.store(to_user, message_body, transact={'from': self.w3.eth.accounts[0]})

    def retrieve(self, user: Contact, last_message: int, contact_list: List[Contact]) -> List[Message]:
        """

        :param user: The user to download new messages for.
        :param last_message: The last message ID that the local database was aware of.
        :param contact_list: The current database of known contacts.
        :return: The list of all new messages.
        """
        abi = self.contract_interface['abi']
        contract = self.w3.eth.contract(address=self.addr, abi=abi)

        result = contract.functions.retrieve(int(user.address), last_message).call()

        messages = list()

        res_list = result.split('♠')
        for x in res_list:
            y = x.split('♣')
            c: Contact = None
            if len(y) == 5:
                for z in contact_list:
                    if z.uname == y[2]:
                        c = z
                if c is None:
                    c = Contact('', y[2], '')
                messages.append(Message(int(y[0]), user, c, y[3], y[4], False))
        return messages
