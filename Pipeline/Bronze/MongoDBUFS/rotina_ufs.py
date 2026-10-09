from Mongo.rotina_mongo import Mongo
from requests import get
from datetime import datetime


class RotinaMongo(Mongo):
    def __init__(self):
        super().__init__()
        self.__resposta = get(f'https://servicodados.ibge.gov.br/api/v1/localidades/estados').json()

    def consultar_ufs(self, uf: str, nm_colecao) -> str:
        """
        Realiza a consulta de um dado do banco mongodb
        :param nm_colecao: informar o nome da colecao -> 'ufs'
        :param uf: 'SP'
        :return: {
            '_id': ObjectId('6ab466849847f9064015b303'),
            'SP': {'nm_uf': 'São Paulo', 'regiao_sigla': 'Sudeste', 'regiao': 'Sudeste'}
            }
        """
        documento = self.banco_mongo[nm_colecao].find_one({uf: {"$exists": True}})

        return documento

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
                try:
                    if dicionario_regiao[uf][chave] == dicionario_mongo[uf][chave]:
                        lista_status_atual.append(True)
                    else:
                        lista_status_atual.append(False)
                    dicionario_verificacao[uf].update(
                        {'status': True if True in list(set(lista_status_atual)) else False}
                    )
                except KeyError:
                    continue
        return dicionario_verificacao

    @staticmethod
    def verificacao_dados_novos(dicionario_regiao: dict, dicionario_mongo: dict) -> list:
        """
        Realiza a comparação entre os dados que estão em 'dicionario_regiao' com os dados de 'dicionario_mongo' para
        que seja atualizado os dados no mongodb caso necessario
        :param dicionario_regiao: {'AC': {'data_insercao': '02/10/2026 18:54:46',
            'nm_uf': 'Acre',
            'regiao': 'Norte',
            'regiao_sigla': 'N'}, ...}
        :param dicionario_mongo: {'AC': {'nm_uf': 'Acre', 'regiao': 'Norte', 'regiao_sigla': 'Norte'},...}
        :return: [{'AC': {'status': True}, 'AL': {'status': False}, ...}]
        """
        lista_dicionario_dados_novos = []
        for uf in dicionario_regiao:
            try:
                dicionario_mongo[uf]
            except KeyError:
                lista_dicionario_dados_novos.append({uf: dicionario_regiao[uf]})
        return lista_dicionario_dados_novos

    def rotina_atualizar(self, nm_colecao: str) -> None:
        """
        Realiza a rotina de atualização dos dados do banco no mongodb
        :return: None
        """
        dicionario_regiao = self.requisicao_ufs()
        dicionario_mongo = self.obter_dicionario_colecao(nm_colecao=nm_colecao)
        dicionario_verificacao = self.verificacao_dados_atualizados(
            dicionario_regiao=dicionario_regiao,
            dicionario_mongo=dicionario_mongo
        )
        for uf in dicionario_verificacao:
            if dicionario_verificacao[uf]['status']:
                self.atualizar_colecao(chave=uf, dados=dicionario_regiao[uf], nm_colecao=nm_colecao)

    def rotina_inserir(self, nm_colecao: str) -> None:
        """
        Realiza a rotina de inserir os novos dados do banco no mongodb
        :return: None
        """
        dicionario_regiao = self.requisicao_ufs()
        dicionario_mongo = self.obter_dicionario_colecao(nm_colecao=nm_colecao)
        lista_dados_novos = self.verificacao_dados_novos(
            dicionario_regiao=dicionario_regiao,
            dicionario_mongo=dicionario_mongo
        )
        for dado in lista_dados_novos:
            self.inserir_dados_colecao(dicionario_colecao=dado, nm_colecao=nm_colecao)

    def rotina_ufs_mongo(self) -> None:
        """
        Rotina principal do fluxo de verificação de dados novos e desatualizados da colecao 'ufs' do banco
        'db_projeto_churn'
        :return: None
        """
        self.rotina_atualizar(nm_colecao='ufs')
        self.rotina_inserir(nm_colecao='ufs')
        self.fechar_conexao_mongo_db()