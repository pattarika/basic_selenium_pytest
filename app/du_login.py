class Login():

    def __init__(self, credentialFile):
        self.file = open(credentialFile, 'r')
        self.credential = {}
        for line in self.file:
            x = line.split(',')
            username = x[0]
            password = x[1]
            c = len(password)-1
            self.credential[username] = password[0:c]

    def get_credential(self):
        return list(self.credential)

    def get_index_by_username(self, username):
        for i, x in enumerate(self.credential):
            if x == username:
                return i

    def get_pwd_by_username(self, username):
        for i, x in enumerate(self.credential):
            if x == username:
                return self.credential[x]

    def get_pwd_by_index(self, index):
        values = list(self.credential.values())
        return values[index]
