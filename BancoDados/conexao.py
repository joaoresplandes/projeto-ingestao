import os
from dotenv import load_dotenv
import pyodbc


class DBAuditoria:
    load_dotenv(rf"{'/'.join([path for path in os.getcwd().split('/')][:6])}/Comum/.env_banco")

    def __init__(self):
        self.LOGIN = os.getenv('login_banco')
        self.PWD = os.getenv('senha_banco')
        self.DB = os.getenv('nome_db')
        self.PORT = os.getenv('porta')
        self.HOST = os.getenv('host')
        self.DRIVER = os.getenv('driver')
        self.__ENGINE = (f'DRIVER={self.DRIVER};'
                       f'SERVER={self.HOST};'
                       f'DATABASE={self.DB};'
                       f'UID={self.LOGIN};'
                       f'PWD={self.PWD};'
                       'TrustServerCertificate=yes;')

    @property
    def engine(self):
        return self.__ENGINE
