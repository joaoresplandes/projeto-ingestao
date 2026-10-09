import os


class ComumMongo:
    PATH: str = '/'.join([path for path in os.getcwd().split('/')][:6])
    PATH_MONGO = rf'{PATH}/Mongo/Conexao'
