from MongoDB.conexao import ConexaoMongoDB


class RotinaMongo:
    def __init__(self):
        self.__nm_banco = 'db_projeto_churn'
        self.__conexao = ConexaoMongoDB().client
        self.__banco_mongo = self.__conexao[self.__nm_banco]

    def listar_ufs(self):
        colecao_ufs = self.__banco_mongo['ufs']
        dados = list(colecao_ufs.find())
        self.__conexao.close()
        return dados

    def inserir_ufs(self, dicionario_ufs: dict) -> None:
        """
        Atualiza a coleção de dicionarios 'ufs' do banco 'db_projeto_churn' do MongoDB
        :param dicionario_ufs: dicionario de ufs
        :return: None
        """
        colecao_ufs = self.__banco_mongo['ufs']
        for chave, valor in dicionario_ufs.items():
            colecao_ufs.insert_one({chave: valor})
        self.__conexao.close()
