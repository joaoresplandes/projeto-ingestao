import polars as pl
from numpy import median


class TransformParticipacao:
    def __init__(self, tabela: pl.DataFrame):
        self.__tabela = tabela
        self.__desvio_padrao = self.__tabela['vlr_coparticipacao'].std() * 4


    def dados_outliers(self) -> pl.DataFrame:
        """
        Retorna a tabela filtrada que tem como 'vlr_coparticipacao' maior que 4 x Desvio Padrao da propria coluna
        :return: pl.DataFrame filtrada
        """
        tabela = self.__tabela.filter(
            (pl.col('vlr_coparticipacao').is_null()) |
            (pl.col('vlr_coparticipacao') >= self.__desvio_padrao)
        )

        return tabela

    def dados_nao_outliers(self) -> pl.DataFrame:
        """
        Retorna a tabela filtrada que tem como 'vlr_coparticipacao' abaixo de 4 x Desvio Padrao da propria coluna
        :return: pl.DataFrame filtrada
        """
        tabela = self.__tabela.filter(
            (~pl.col('vlr_coparticipacao').is_null()) &
            (pl.col('vlr_coparticipacao') < self.__desvio_padrao)
        )

        return tabela


    def obter_mediana(self) -> int:
        """
        retorna a mediana da coluna vlr_coparticipacao, ja desconsiderando os valores None
        :return: 3912
        """
        mediana = int(
            round(
                median(
                    [
                        valor for valor in self.__tabela['vlr_coparticipacao'].to_list() if valor is not None
                    ]
                ), 0
            )
        )

        return mediana

    @staticmethod
    def tabela_completa(tb_n_outliers: pl.DataFrame, tb_outliers: pl.DataFrame) -> pl.DataFrame:
        """
        Realiza a concatenacao da tabela 'tb_n_outliers' que contem os vlr_coparticipacao com valores abaixo de 4 x STD,
        com a tabela 'tb_outliers' que sofreram alterações em seus registros de vlr_coparticipacao
        :param tb_n_outliers: tabela com vlr_coparticipacao sem alteracao
        :param tb_outliers: tabela com dados de vlr_coparticipacao preenchidos pela mediana da propria coluna
        """
        tabela_resultado = pl.concat(
            [
                tb_n_outliers,
                tb_outliers.with_columns(pl.col('vlr_coparticipacao').cast(pl.Int64))
            ]
        )

        return tabela_resultado


    def executar(self) -> pl.DataFrame:
        """
        Rotina de tratamento da coluna 'vlr_coparticipacao'
        :return: pl.DataFrame
        """
        tabela_outliers = self.dados_outliers()
        if not tabela_outliers.is_empty():
            tabela_outliers = tabela_outliers.with_columns(pl.lit(self.obter_mediana()).alias('vlr_coparticipacao'))
            return self.tabela_completa(
                tb_n_outliers=self.dados_nao_outliers(),
                tb_outliers=tabela_outliers
            ).sort(by='id')
        else:
            return self.__tabela
