'''
Communication Utility with Cell Router
'''

# ssh wrapper library
import paramiko

class CellRouterUtil():
    # TODO: refactor username, password into environment variables
    def __init__(self):
        self.__address = '10.123.123.33'
        self.__username = 'admin'
        self.__password = '1pmlamsh'

    @property
    def address(self):
        return self.__address

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password


    # TODO Refactor username and password into environment variables
    def enableWifi(self):
        print 'enabling wifi'

        client = paramiko.SSHClient()
        client.connect(self.__address, username=self.__username, password=self.__password)

        print 'created client connection'

    def disableWifi(self):
        print 'disabling wifi'

if (__name__ == '__main__'):
    cellRouterUtil = CellRouterUtil()
    cellRouterUtil.enableWifi()
    cellRouterUtil.disableWifi()
