import os

class ComumPostgreSQL:
    PATH: str = '/'.join([path for path in os.getcwd().split('/')][:6])
    PATH_DB: str = rf"{PATH}/BancoDados/Conexoes"
