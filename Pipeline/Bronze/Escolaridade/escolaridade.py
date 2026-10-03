from Comum.Fontes.origens import Path
from Pipeline.Bronze.Escolaridade.fluxo_db_escolaridade import DBEscolaridade
import polars as pl


class IngestaoEscolaridade:
    def __init__(self):
        self.__tabela_completa = DBEscolaridade().consultar_tb_completo()

    @staticmethod
    def obter_dados_escolaridade() -> list:
        """
        Obtem os dados do arquivo de 'escolaridade.txt'
        :return: ['ID_ESCOLARIDADE;DESC_ESCOLARIDADE\n', '1;Ensino Fundamental Incompleto\n', ...]
        """
        with open(Path.ARQUIVO_ESCOLARIDADE, 'r', encoding='utf-8') as arquivo_txt:
            escolaridades = arquivo_txt.readlines()

        return escolaridades

    @staticmethod
    def tratar_dados_escolaridade(lista_dados_escolaridade: list) -> list:
        """
        Trara e transforma os dados em uma estrutura tabular
        :param lista_dados_escolaridade: ['ID_ESCOLARIDADE;DESC_ESCOLARIDADE\n', '1;Ensino Fundamental Incompleto\n', ...]
        :return: [['ID_ESCOLARIDADE', 'DESC_ESCOLARIDADE'],
                 ['1', 'Ensino Fundamental Incompleto'],
                 ['2', 'Ensino Fundamental Completo'],...
                 ]
        """
        lista_dados_escolaridade = [dado.replace('\n', '').split(';') for dado in lista_dados_escolaridade]

        return lista_dados_escolaridade

    @staticmethod
    def lista_dicionario_dados_escolaridade(lista_dados_escolaridade: list) -> list:
        """
        Cria uma estrutura de lista de dicionarios para verificação de dados com os já inseridos em banco
        :param lista_dados_escolaridade: [
            ['ID_ESCOLARIDADE', 'DESC_ESCOLARIDADE'],
            ['1', 'Ensino Fundamental Incompleto'],
            ...]
        :return: [{'ID_ESCOLARIDADE': '1', 'DESC_ESCOLARIDADE': 'Ensino Fundamental Incompleto'}, ...]
        """
        dados_escolaridade = []
        for linha in range(len(lista_dados_escolaridade[1:])):
            dados_escolaridade.append(
                {
                    nm_coluna: lista_dados_escolaridade[linha + 1][num_coluna]
                    for num_coluna, nm_coluna in enumerate(lista_dados_escolaridade[0])
                }
            )

        return dados_escolaridade

    @staticmethod
    def rotina_tratativa_dados() -> list:
        """
        Executa rotina de tratativas iniciais minimas para organizar os dados para serem inseridos em tabeça ma camada
        bronze
        :return: [{'ID_ESCOLARIDADE': '1', 'DESC_ESCOLARIDADE': 'Ensino Fundamental Incompleto'}, ...]
        """
        ingestao = IngestaoEscolaridade()
        lista_dados_brutos = ingestao.obter_dados_escolaridade()
        dados_tratados = ingestao.tratar_dados_escolaridade(lista_dados_escolaridade=lista_dados_brutos)
        dados_escolaridade = ingestao.lista_dicionario_dados_escolaridade(lista_dados_escolaridade=dados_tratados)

        return dados_escolaridade

    @staticmethod
    def criar_dicionario_dados_escolaridade(lista_dados_escolaridade: list) -> dict:
        """
        Transforma a lista de dados em uma estrutura de dicionario pronta para ser usada em um dataframe
        :param lista_dados_escolaridade: [
            {'ID_ESCOLARIDADE': '1', 'DESC_ESCOLARIDADE': 'Ensino Fundamental Incompleto'}, ...]
        :return:{
            'ID_ESCOLARIDADE': ['1', '2', ...],
            'DESC_ESCOLARIDADE': [Ensino Fundamental Incompleto', 'Ensino Fundamental Completo', ...]
        }
        """
        lista_colunas = []
        for colunas in [list(dicionario.keys()) for dicionario in lista_dados_escolaridade]:
            for coluna in colunas:
                lista_colunas.append(coluna)

        dict_escolaridade = {coluna: [] for coluna in list(set(lista_colunas))}

        for coluna in dict_escolaridade.keys():
            for conjunto in lista_dados_escolaridade:
                dict_escolaridade[coluna].append(conjunto[coluna])

        return dict_escolaridade

    def dados_modificados(self, lista_dados_escolaridade: list) -> list:
        """
        Realiza uma verificação de quais dados tiveram atualização em seus campos para que sejam atualizados em banco,
        retornando apenas a lista com os dados que houveram modificação
        :param lista_dados_escolaridade: [
            {'ID_ESCOLARIDADE': '1', 'DESC_ESCOLARIDADE': 'Ensino Fundamental Incompleto'}, ...
        ]
        :return: [
            {'ID_ESCOLARIDADE': '1', 'DESC_ESCOLARIDADE': 'Ensino Fundamental Incompleto'}, ...
        ]
        """
        lista_linhas = []
        for item in lista_dados_escolaridade:
            try:
                for nm_coluna in self.__tabela_completa.columns[1:len(self.__tabela_completa.columns)-1]:
                    dsc = self.__tabela_completa.filter(
                        pl.col(self.__tabela_completa.columns[0]) == int(item[self.__tabela_completa.columns[0].upper()])
                    )[nm_coluna].to_list()[0]
                    if dsc != item[nm_coluna.upper()]:
                        lista_linhas.append(item)
            except IndexError:
                continue
        if lista_linhas:
            return lista_linhas
        else:
            return []

    def dados_novos(self, lista_dados_escolaridade: list) -> list:
        """
        Verifica os IDS do da lista de 'lista_dados_escolaridade' que ainda não estão no banco, para que sejam
        inseridos como novos dados
        :param lista_dados_escolaridade: [
            {'ID_ESCOLARIDADE': '1', 'DESC_ESCOLARIDADE': 'Ensino Fundamental Incompleto'}, ...
        ]
        :return: [
            {'ID_ESCOLARIDADE': '1', 'DESC_ESCOLARIDADE': 'Ensino Fundamental Incompleto'}, ...
        ]
        """
        novos_registros = []
        for item in lista_dados_escolaridade:
            if int(item[self.__tabela_completa.columns[0].upper()]) not in self.__tabela_completa[self.__tabela_completa.columns[0]].unique().to_list():
                novos_registros.append(item)

        if novos_registros:
            return novos_registros
        else:
            return []

    def rotina_atualizacao_banco(self, lista_dados_escolaridade: list) -> None:
        """
        Rotina de atualização dos dados ja existentes em banco de dados
        :param lista_dados_escolaridade: [
            {'ID_ESCOLARIDADE': '1', 'DESC_ESCOLARIDADE': 'Ensino Fundamental Incompleto'}, ...]
        :return: None
        """
        lista_escolaridade_atualizacao = self.dados_modificados(lista_dados_escolaridade=lista_dados_escolaridade)
        if lista_escolaridade_atualizacao:
            dados_atualizados = self.criar_dicionario_dados_escolaridade(
                lista_dados_escolaridade=lista_escolaridade_atualizacao)
            DBEscolaridade().atualizar_tb_escolaridade(dicionario_dados=dados_atualizados)

    def rotina_dados_novos_banco(self, lista_dados_escolaridade: list) -> None:
        """
        Rotina de inserção de novos dados no banco de dados
        :param lista_dados_escolaridade: [
            {'ID_ESCOLARIDADE': '1', 'DESC_ESCOLARIDADE': 'Ensino Fundamental Incompleto'}, ...]
        :return: None
        """
        lista_escolaridade_novos = self.dados_novos(lista_dados_escolaridade=lista_dados_escolaridade)
        if lista_escolaridade_novos:
            dicionario_dados_novos = self.criar_dicionario_dados_escolaridade(
                lista_dados_escolaridade=lista_escolaridade_novos)
            DBEscolaridade().inserir_tb_escolaridade(dicionario_dados=dicionario_dados_novos)

    def rotina(self) -> None:
        """
        Executa a rotina de ingestão da tabela de escolaridade na camada Bronze
        :return:None
        """
        print('Iniciando Ingestão Escolaridade...')
        dados_escolaridade = self.rotina_tratativa_dados()
        self.rotina_atualizacao_banco(lista_dados_escolaridade=dados_escolaridade)
        self.rotina_dados_novos_banco(lista_dados_escolaridade=dados_escolaridade)
        print('Ingestão escolaridade finalizado!')
