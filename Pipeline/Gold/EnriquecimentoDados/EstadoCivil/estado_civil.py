from Pipeline.Gold.EnriquecimentoDados.bases_complementares import PathBasesComplementares
import polars as pl
import json


class EstadoCivil:
    def __init__(self, tabela: pl.DataFrame):
        self.__tabela = tabela
        self.__dados_estado_civil = self.obter_tabela_estado_civil()

    @staticmethod
    def obter_tabela_estado_civil():
        with open(PathBasesComplementares.ARQUIVO_ESTADO_CIVIL, 'r', encoding='utf-8') as arquivo_json:
            dados_estado_civil = json.loads(arquivo_json.read())

        return dados_estado_civil

    def criar_dataframe_estado_civil(self):
        dict_estado_civil = {
            'ID_EC': [],
            'DSC_EC': []
        }
        for item in self.__dados_estado_civil:
            dict_estado_civil['ID_EC'].append(item['ID_EC'])
            dict_estado_civil['DSC_EC'].append(item['DSC_EC'])

        return pl.DataFrame(dict_estado_civil)

    def complementar_tabela_original(self, tabela_estado_civil: pl.DataFrame ) -> pl.DataFrame:
        """
        Com a tabela estado civil, complementa com os seus dados a tabela original através das colunas de
        'codestadocivil' e 'ID_EC', assim enrriquecendo a tabela original com mais informações de estado civil
        :param tabela_estado_civil: DataFrame de estado civil
        :return: tabela de marketing com informações complementares de estado civil
        """
        tabela_mkt = self.__tabela.join(
            tabela_estado_civil,
            left_on='codestadocivil',
            right_on='ID_EC',
            how='left'
        )

        return tabela_mkt

    def executar(self) -> pl.DataFrame:
        """
        Executa o processo de enrriquecimento de informações referente a estado civil
        :return: tabela original complementada com informações de estado civil
        """
        tb_estado_civil = self.criar_dataframe_estado_civil()
        tabela_final = self.complementar_tabela_original(
            tabela_estado_civil=tb_estado_civil
        )

        return tabela_final
