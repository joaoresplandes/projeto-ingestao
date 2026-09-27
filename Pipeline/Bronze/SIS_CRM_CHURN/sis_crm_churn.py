from Comum.comum import Path
from Pipeline.Bronze.SIS_CRM_CHURN.fluxo_db_sis_crm_churn import DBSisChurn
from unidecode import unidecode
from pprint import pprint
import polars as pl
from datetime import datetime



class Extrair:
    def __init__(self):
        self.path_arquivo = Path.FONTE_PROJETO
        self.__tabela_completa = DBSisChurn().consultar_tb_completo()

    @property
    def tabela_completa(self):
        return self.__tabela_completa

    def extrair_arquivo(self) -> list:
        """
        Com o método with, carrega o conteudo do arquivo .txt no codigo
        :return: string dos dados carregados
        """
        with open(self.path_arquivo, 'r', encoding='utf-8') as arquivo:
            dados = arquivo.readlines()

        return dados

    @staticmethod
    def obter_conjunto_dados(dados: list) -> list:
        """
        Converte os dados em string estrurados em listas, com a primeira sendo o titulo das colunas e as demais listas
        sendo os dados da tabela
        :param dados: dados em string
        :return: lista de dados estruturados
        """
        conjunto = [
            [valor.strip() for valor in linha.replace('\t', ',').replace('\n', '').split(',')]
            for linha in dados
        ]

        return conjunto

    @staticmethod
    def tratar_colunas(lista_colunas: list) -> list:
        """
        Transforma todos dos valores da coluna em caixa baixa com o método .lower()
        :param lista_colunas: lista de colunas com tamanhos variados
        :return: lista de colunas com todos os valores em caixa baixa
        """
        lista_colunas = [unidecode(coluna).lower() for coluna in lista_colunas]

        return lista_colunas

    def dicionario_dados(self, conjunto_dados: list) -> dict:
        """
        Com os dados separados em linhas por listas, é possível criar uma estrutura de dicionario com cada um dos
        valores da primiera lista com chaves e seus respectivos valores em sua lista de valores, respectivo a posição
        atual de cada uma das demais listas
        :param conjunto_dados: listas de dados
        :return: dicionarios de chaves sendo cada um dos valores da primeira lista e seus respectivos valores em lista
        """
        dict_tabela = {}
        for i, coluna in enumerate(self.tratar_colunas(conjunto_dados[0])):
            lista_dados = []
            for dado in conjunto_dados[1:]:
                lista_dados.append(dado[i].upper())
            dict_tabela[coluna] = lista_dados

        return dict_tabela

    @staticmethod
    def lista_dicionario_dados_banco(lista_dados_sis_crm: list) -> list:
        """
        Cria uma estrutura de dados em dicionario de forma que possa ser conferida linha a linhda
        :param lista_dados_sis_crm: [['ID', 'cpf', 'nome', 'sobrenome', 'idgenero', ...]]
        :return: [{'id': '506', 'cpf': '123.456.789-01', 'nome': 'Alice', ...]
        """
        dados_sis_crm_churn = [
            {
                nm_coluna.lower(): lista_dados_sis_crm[linha + 1][num_coluna]
                for num_coluna, nm_coluna in enumerate(lista_dados_sis_crm[0])
            }
            for linha in range(len(lista_dados_sis_crm[1:]))
        ]

        return dados_sis_crm_churn

    def executar_extracao(self):
        """
        Função que executa todas as etapas sequenciais de extração dos dados do arquivo .txt inicial
        :return: [{'id': '506', 'cpf': '123.456.789-01', 'nome': 'Alice', ...]
        """
        dados = self.extrair_arquivo()
        lista_dados = self.obter_conjunto_dados(dados=dados)
        lista_dicionario_dados = self.lista_dicionario_dados_banco(lista_dados_sis_crm=lista_dados)

        return lista_dicionario_dados


    def verifica_dados_novos(self, dados_sis_crm_churn: list) -> list:
        """
        Verifica se os dados de 'dados_sis_crm_churn' ja se encontram no banco, caso não, são inseridos em uma nova
        lista para serem inseridos em banco
        :param dados_sis_crm_churn: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        :return: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        novos_registros_crm_churn = []
        for linha in dados_sis_crm_churn:
            if int(linha['id']) not in [
                    int(num_id)
                    for num_id in self.__tabela_completa[self.__tabela_completa.columns[0]].unique().to_list()
                ]:
                novos_registros_crm_churn.append(linha)

        return novos_registros_crm_churn

    def verifica_dados_atualizados(self, dados_sis_crm_churn: list) -> list:
        """
        Verifica se os dados de 'dados_sis_crm_churn' contem no banco e se houve alteração em alguma coluna para que
        seja atualizados
        :param dados_sis_crm_churn: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        :return: [{'id': '1', 'cpf': '123.456.789-01', 'nome': 'Alice', 'sobrenome': 'Alves', ...}]
        """
        registros_atualizados_sis_crm_churn = []
        for item in dados_sis_crm_churn:
            try:
                for nm_coluna in self.__tabela_completa.columns[1:len(self.__tabela_completa.columns) - 1]:
                    dsc = self.__tabela_completa.filter(
                        pl.col(self.__tabela_completa.columns[0]) == int(item[self.__tabela_completa.columns[0]])
                    )[nm_coluna].to_list()[0]
                    if dsc != item[nm_coluna]:
                        registros_atualizados_sis_crm_churn.append(item)
            except IndexError:
                continue

        return registros_atualizados_sis_crm_churn

    def rotina_novos_dados(self, lista_dicionario_dados_churn: list) -> None:
        """
        Rotina de inserção de dados novos na tabela de 'tb_sis_crm_churn' na camada bronze
        :param lista_dicionario_dados_churn: [{'id': '506', 'cpf': '123.456.789-01', 'nome': 'Alice', ...]
        :return: None
        """
        lista_novos_dados_crm_churn = self.verifica_dados_novos(dados_sis_crm_churn=lista_dicionario_dados_churn)
        if lista_novos_dados_crm_churn:
            DBSisChurn().inserir_tb_sis_crm_churn(lista_dicionario_dados=lista_novos_dados_crm_churn)
            print(f'{len(lista_novos_dados_crm_churn)} dado(s) novo(s) inserido(s) em banco!')
        else:
            print(f'{len(lista_novos_dados_crm_churn)} dado(s) novo(s) inserido(s) em banco!')

    def rotina_dados_atualizados(self, lista_dicionario_dados_churn: list) -> None:
        """
        Rotina de atualização dos dados de 'tb_sis_crm_churn' da camada bronze
        :param lista_dicionario_dados_churn: [{'id': '506', 'cpf': '123.456.789-01', 'nome': 'Alice', ...]
        :return:
        """
        lt_dados_atualizados_crm_churn = self.verifica_dados_atualizados(dados_sis_crm_churn=lista_dicionario_dados_churn)
        if lt_dados_atualizados_crm_churn:
            # DBSisChurn().inserir_db_sis_crm_churn(lista_dicionario_dados=lt_dados_atualizados_crm_churn)
            print(f'{len(lt_dados_atualizados_crm_churn)} dado(s) atualizado(s) em banco!')
        else:
            print(f'{len(lt_dados_atualizados_crm_churn)} dado(s) atualizado(s) em banco!')

    def rotina(self):
        lista_dados_sis_crm_churn = self.executar_extracao()
        self.rotina_novos_dados(lista_dicionario_dados_churn=lista_dados_sis_crm_churn)
        self.rotina_dados_atualizados(lista_dicionario_dados_churn=lista_dados_sis_crm_churn)


if __name__ == '__main__':
    # Extrair().rotina()
    final = []
    lista_dados_sis_crm_churn = Extrair().executar_extracao()
    for dado in lista_dados_sis_crm_churn:
        lista_dados_original = list(dado.values())
        lista_dados_original.append(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        lista_dados_original.append(lista_dados_original[0])
        del lista_dados_original[0]
        final.append(tuple(lista_dados_original))

    print(final)
    # tabela = Extrair().tabela_completa
    # dados_banco = Extrair().verifica_dados_novos(dados_sis_crm_churn=lista_dados_sis_crm_churn)
    #
    # placeholder = ', '.join('?' for _ in dados_banco[0].keys()) + ', ?'
    # print(placeholder)
    #
    # for dado in dados_banco:
    #     lista_dados_original = list(dado.values())
    #     lista_dados_original.append(str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    #     final.append(tuple(lista_dados_original))
    #
    # print(final)
