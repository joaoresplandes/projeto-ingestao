from Comum.Fontes.origens import Path
from BancoDados.rotina_banco import RotinaBanco
from Pipeline.Bronze.EstadoCivil.fluxo_db_estado_civil import DBEstadoCivil
from json import loads
import polars as pl


class IngestaoEstadoCivil(RotinaBanco):
    def __init__(self):
        self.__nm_tb_estado_civil: str = 'projeto_churn.bronze.tb_estado_civil'
        super().__init__()
        self.__tabela_completa = self.tabela(nm_tabela=self.__nm_tb_estado_civil)


    @staticmethod
    def obter_dados_estado_civil() -> list:
        """
        Obtem todos os dados do arquivo .json, onde tem as informações de estado civil
        :return: [{'ID_EC': 1, 'DSC_EC': 'Solteiro(a)'}, {'ID_EC': 2, 'DSC_EC': 'Casado(a)'}]
        """
        with open(Path.ARQUIVO_ESTADO_CIVIL, 'r', encoding='utf-8') as arquivo_json:
            dados_estado_civil = loads(arquivo_json.read())

        return dados_estado_civil

    @staticmethod
    def dicionario_estado_civil(lista_estado_civil: list) -> dict:
        """
        Transforma a lista de dicionarios em um dicionario puro
        :param lista_estado_civil: [{'ID_EC': 1, 'DSC_EC': 'Solteiro(a)'}, {'ID_EC': 2, 'DSC_EC': 'Casado(a)'}]
        :return: {'ID_EC': [1, 2, ...], 'DSC_EC': ['Solteiro(a)', 'Casado(a)', ...]}
        """
        dict_estado_civil = {
            'ID_EC': [],
            'DSC_EC': []
        }
        for conjunto in lista_estado_civil:
            dict_estado_civil['ID_EC'].append(conjunto['ID_EC'])
            dict_estado_civil['DSC_EC'].append(conjunto['DSC_EC'])

        return dict_estado_civil

    @staticmethod
    def dados_modificados(lista_estado_civil: list, tabela_banco: pl.DataFrame) -> list:
        """
        Realiza uma verificação de quais dados tiveram atualização em seus campos para que sejam atualizados em banco,
        retornando apenas a lista com os dados que houveram modificação
        :param lista_estado_civil: [{'ID_EC': 1, 'DSC_EC': 'Solteiro(a)'}, {'ID_EC': 2, 'DSC_EC': 'Casado(a)'}]
        :param tabela_banco: tabela de estado civil do banco de dados
        :return: [{'ID_EC': 1, 'DSC_EC': 'Solteiro(a)'}]
        """
        lista_linhas = []
        for item in lista_estado_civil:
            try:
                for nm_coluna in tabela_banco.columns[1:len(tabela_banco.columns)-1]:
                    dsc = tabela_banco.filter(
                        pl.col(tabela_banco.columns[0]) == item[tabela_banco.columns[0].upper()]
                    )[nm_coluna].to_list()[0]
                    if dsc != item[nm_coluna.upper()]:
                        lista_linhas.append(item)
            except IndexError:
                continue
        if lista_linhas:
            return lista_linhas
        else:
            return []

    @staticmethod
    def dados_novos(lista_estado_civil: list, tabela_banco: pl.DataFrame) -> list:
        """
        Verifica os IDS do da lista de 'lista_estado_civil' que ainda não estão no banco, para que sejam inseridos como
        novos dados
        :param lista_estado_civil: [{'ID_EC': 1, 'DSC_EC': 'Solteiro(a)'}, {'ID_EC': 2, 'DSC_EC': 'Casado(a)'}]
        :param tabela_banco: tabela de estado civil do banco de dados
        :return: [{'ID_EC': 1, 'DSC_EC': 'Solteiro(a)'}]
        """
        novos_registros = []
        for item in lista_estado_civil:
            if item[tabela_banco.columns[0].upper()] not in tabela_banco[tabela_banco.columns[0]].unique().to_list():
                novos_registros.append(item)

        if novos_registros:
            return novos_registros
        else:
            return []

    def rotina_atualizacao_banco(self, lista_estado_civil: list) -> None:
        """
        Rotina de atualização dos dados ja existentes em banco de dados
        :param lista_estado_civil: [{'ID_EC': 1, 'DSC_EC': 'Solteiro(a)'}, {'ID_EC': 2, 'DSC_EC': 'Casado(a)'}]
        :return: None
        """
        lista_estado_civil_atualizacao = self.dados_modificados(
            lista_estado_civil=lista_estado_civil,
            tabela_banco=self.__tabela_completa
        )
        if lista_estado_civil_atualizacao:
            dicionario_dados_atualizados = self.dicionario_estado_civil(
                lista_estado_civil=lista_estado_civil_atualizacao)
            DBEstadoCivil().atualizar_tb_estado_civil(dicionario_dados=dicionario_dados_atualizados)

    def rotina_dados_novos_banco(self, lista_estado_civil: list) -> None:
        """
        Rotina de inserção de novos dados no banco de dados
        :param lista_estado_civil: [{'ID_EC': 1, 'DSC_EC': 'Solteiro(a)'}, {'ID_EC': 2, 'DSC_EC': 'Casado(a)'}]
        :return: None
        """
        lista_estado_civil_novos = self.dados_novos(
            lista_estado_civil=lista_estado_civil,
            tabela_banco=self.__tabela_completa
        )
        if lista_estado_civil_novos:
            dicionario_dados_novos = self.dicionario_estado_civil(lista_estado_civil=lista_estado_civil_novos)
            DBEstadoCivil().inserir_tb_estado_civil(dicionario_dados=dicionario_dados_novos)

    def rotina(self) -> None:
        """
        Rotina do fluxo de ingestão da tabela de 'Estado Civil'
        :return: None
        """
        print('Iniciando Ingestão Estado Civil...')
        lista_estado_civil = self.obter_dados_estado_civil()
        self.rotina_atualizacao_banco(lista_estado_civil=lista_estado_civil)
        self.rotina_dados_novos_banco(lista_estado_civil=lista_estado_civil)
        print('Ingestão estado civil finalizado!')
