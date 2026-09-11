import os
from dotenv import load_dotenv


class DBAuditoria:
    load_dotenv(rf"{'\\'.join([path for path in os.getcwd().split('\\')])}\\{'.env'}")

    def __init__(self):
        self.LOGIN = os.getenv('login_banco')
        self.PWD = os.getenv('senha_banco')
        self.NAME = 'master'
        self.PORT = '1433'
        self.HOST = r'localhost\DEVSQLSERVER'
        self.ENGINE = ('DRIVER={ODBC Driver 18 for SQL Server};'
                       f'SERVER={self.HOST};'
                       f'DATABASE={self.NAME};'
                       f'UID={self.LOGIN};'
                       f'PWD={self.PWD};'
                       'TrustServerCertificate=yes;')