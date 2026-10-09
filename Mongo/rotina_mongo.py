from Mongo.Conexao.conexao_mongo import ConexaoMongoDB


class Mongo:
    def __init__(self):
        self.__nm_banco = 'db_projeto_churn'
        self.__conexao = ConexaoMongoDB().client
        self.__banco_mongo = self.__conexao[self.__nm_banco]

    @property
    def banco_mongo(self):
        return self.__banco_mongo

    @property
    def conexao_mongo(self):
        return self.__conexao

    def listar_colecao(self, nm_colecao: str) -> list:
        """
        Listar todos os documentos da coleção ufs do banco 'db_projeto_churn'
        :return: lista de documentos
        """
        colecao = self.__banco_mongo[nm_colecao]
        dados = list(colecao.find())

        return dados

    def obter_dicionario_colecao(self, nm_colecao: str) -> dict:
        """
        Transforma a lista de dicionarios provenientes do banco em um dicionario de ufs pronto para ser usado
        :return: {'AC': {'nm_uf': 'Acre', 'regiao': 'Norte', 'regiao_sigla': 'Norte'},...}
        """
        lista_colecao = self.listar_colecao(nm_colecao=nm_colecao)
        ufs_banco = {
            list(item)[1]: item[list(item)[1]] for item in lista_colecao
        }

        return ufs_banco

    def fechar_conexao_mongo_db(self) -> None:
        """
        Fecha a conexao com o mongodb
        :return: None
        """
        self.__conexao.close()

    def inserir_dados_colecao(self, dicionario_colecao: dict, nm_colecao: str) -> None:
        """
        Atualiza a coleção de dicionarios 'ufs' do banco 'db_projeto_churn' do MongoDBUFS
        :param nm_colecao: informar o nome da colecao -> 'ufs'
        :param dicionario_colecao: dicionario de ufs
        :return: None
        """
        for chave, valor in dicionario_colecao.items():
            self.__banco_mongo[nm_colecao].insert_one({chave: valor})

    def atualizar_colecao(self, chave: str, dados: dict, nm_colecao: str):
        """
        Realiza a atualização dos dados no mongodb
        :param nm_colecao: informar o nome da colecao -> 'ufs'
        :param chave: 'SP'
        :param dados: {
            'nm_uf': 'São Paulo', 'regiao_sigla': 'SE', 'regiao': 'Sudeste', 'data_insercao': '02/10/2026 19:29:42'}
        :return: None
        """
        self.__banco_mongo[nm_colecao].update_one(
            {chave : {"$exists": True}},
            {"$set": {chave: dados}}
        )
