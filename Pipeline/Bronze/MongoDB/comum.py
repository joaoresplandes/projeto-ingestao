import os


class ComumMongo:
    PATH: str = '/'.join([path for path in os.getcwd().split('/')][:6])
    PATH_MONGO = rf'{PATH}/Comum'


if __name__ == '__main__':
    print(ComumMongo.PATH_MONGO)
