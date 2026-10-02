from Pipeline.Bronze.MongoDB.conexao import ConexaoMongoDB
from requests import get
from datetime import datetime


class RotinaMongo:
    def __init__(self):
        self.__nm_banco = 'db_projeto_churn'
        self.__conexao = ConexaoMongoDB().client
        self.__banco_mongo = self.__conexao[self.__nm_banco]
        self.__colecao_ufs = self.__banco_mongo['ufs']
        self.__resposta = get(f'https://servicodados.ibge.gov.br/api/v1/localidades/estados').json()

    def listar_ufs(self):
        """
        Listar todos os documentos da coleção ufs do banco 'db_projeto_churn'
        :return: lista de documentos
        """
        colecao_ufs = self.__banco_mongo['ufs']
        dados = list(colecao_ufs.find())
        self.__conexao.close()
        return dados

    def dicionario_ufs(self) -> dict:
        """
        Transforma a lista de dicionarios provenientes do banco em um dicionario de ufs pronto para ser usado
        :return: {'AC': {'nm_uf': 'Acre', 'regiao': 'Norte', 'regiao_sigla': 'Norte'},...}
        """
        lista_ufs = self.listar_ufs()
        ufs_banco = {
            list(uf)[1]: uf[list(uf)[1]] for uf in lista_ufs
        }

        return ufs_banco

    def inserir_ufs(self, dicionario_ufs: dict) -> None:
        """
        Atualiza a coleção de dicionarios 'ufs' do banco 'db_projeto_churn' do MongoDB
        :param dicionario_ufs: dicionario de ufs
        :return: None
        """
        for chave, valor in dicionario_ufs.items():
            self.__colecao_ufs.insert_one({chave: valor})
        self.__conexao.close()

    def consultar_ufs(self, uf: str) -> str:
        """
        Realiza a consulta de um dado do banco mongodb
        :param uf: 'SP'
        :return: {
            '_id': ObjectId('6ab466849847f9064015b303'),
            'SP': {'nm_uf': 'São Paulo', 'regiao_sigla': 'Sudeste', 'regiao': 'Sudeste'}
            }
        """
        documento = self.__colecao_ufs.find_one({uf: {"$exists": True}})

        return documento

    def atualizar_ufs(self, sigla_uf: str, dados: dict):
        """
        Realiza a atualização dos dados no mongodb
        :param sigla_uf: 'SP'
        :param dados: {
            'nm_uf': 'São Paulo', 'regiao_sigla': 'SE', 'regiao': 'Sudeste', 'data_insercao': '02/10/2026 19:29:42'}
        :return: None
        """
        self.__colecao_ufs.update_one(
            {sigla_uf : {"$exists": True}},
            {"$set": {sigla_uf: dados}}
        )


    def requisicao_ufs(self) -> dict:
        """
        Realiza a requisição para o url e retorna a resposta, logo em seguida é formatado em um dicionario apenas os
        dados necessarios para a demanda como
        sigla -> a uf do estado
        nm_uf -> Nome do Estado
        regiao -> Nome da região daquele estado - Nordeste
        regiao_sigla -> Sigla da região daquele estado - NO
        data_insercao -> data hora de atualizacao daquele dado
        :return: {'AC': {'data_insercao': '02/10/2026 18:54:46',
            'nm_uf': 'Acre',
            'regiao': 'Norte',
            'regiao_sigla': 'N'}, ...}
        """
        dicionario_regiao = {}
        for item in self.__resposta:
            dicionario_regiao[item['sigla']] = {
                'nm_uf': item['nome'],
                'regiao_sigla': item["regiao"]['sigla'],
                'regiao': item['regiao']['nome'],
                'data_insercao': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
        return dicionario_regiao

    @staticmethod
    def verificacao_dados_atualizados(dicionario_regiao: dict, dicionario_mongo: dict) -> dict:
        """
        Realiza a comparação entre os dados que estão em 'dicionario_regiao' com os dados de 'dicionario_mongo' para
        que seja atualizado os dados no mongodb caso necessario
        :param dicionario_regiao: {'AC': {'data_insercao': '02/10/2026 18:54:46',
            'nm_uf': 'Acre',
            'regiao': 'Norte',
            'regiao_sigla': 'N'}, ...}
        :param dicionario_mongo: {'AC': {'nm_uf': 'Acre', 'regiao': 'Norte', 'regiao_sigla': 'Norte'},...}
        :return: {'AC': {'status': True}, 'AL': {'status': False}, ...}
        """
        dicionario_verificacao = {}
        for uf in dicionario_regiao:
            lista_status_atual = []
            dicionario_verificacao[uf] = {'status': {}}
            for chave in list(dicionario_regiao[uf].keys())[:-1]:
                if dicionario_regiao[uf][chave] == dicionario_mongo[uf][chave]:
                    lista_status_atual.append(True)
                else:
                    lista_status_atual.append(False)
                dicionario_verificacao[uf].update(
                    {'status': True if True in list(set(lista_status_atual)) else False}
                )
        return dicionario_verificacao

    def rotina_atualizar(self) -> None:
        """
        Realiza a rotina de atualização dos dados do banco no mongodb
        :return: None
        """
        dicionario_regiao = self.requisicao_ufs()
        dicionario_mongo = self.dicionario_ufs()
        dicionario_verificacao = self.verificacao_dados_atualizados(
            dicionario_regiao=dicionario_regiao,
            dicionario_mongo=dicionario_mongo
        )
        for uf in dicionario_verificacao:
            if dicionario_verificacao[uf]['status']:
                self.atualizar_ufs(sigla_uf=uf, dados=dicionario_regiao[uf])

