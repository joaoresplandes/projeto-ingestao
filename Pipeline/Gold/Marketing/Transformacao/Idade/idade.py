import polars as pl
from math import trunc
from numpy import median



class TransformIdade:
    def __init__(self, tabela: pl.DataFrame):
        self.__tabela = tabela


    def filter_idades_validas(self) -> pl.DataFrame:
        """
        Retorna a tabela com as idades validas entre 0 e 100
        :return: pl.DataFrame
        """
        tabela = self.__tabela.filter(
            (pl.col('idade') >= 0) &
            (pl.col('idade') <= 100)
        )

        return tabela


    def obter_mediana_idade(self) -> int:
        """
        OBtem a mediana da coluna de idade
        :return: 45
        """
        lista_mediana = self.__tabela['idade'].to_list()
        mediana = int(trunc(median(lista_mediana)))

        return mediana

    def filter_idades_nao_validas(self) -> pl.DataFrame:
        """
        Filtra as linhas com idades classificadas como outliers (Menor que 0 e maior que 100), trocando os valores
        atuais pela mediana da coluna, ja que a média pode ser distorcida por esses valores
        :return: pl.DataFrame
        """
        tabela = self.__tabela.filter(

            (pl.col('idade') < 0) |
            (pl.col('idade') > 100)

        )

        tabela = tabela.with_columns(pl.lit(self.obter_mediana_idade()).alias('idade'))

        return tabela

    @staticmethod
    def tabela_completa(tb_idades_validas: pl.DataFrame, tb_idades_nao_validas: pl.DataFrame) -> pl.DataFrame:
        """
        Realiza a concatenacao da tabela 'tb_idades_validas' que contem as idades dentro do intervalor, com a tabela
        'tb_idades_nao_validas' que sofreram alterações em sesu registros de idade
        :param tb_idades_validas: tabela com idade sem alteracao
        :param tb_idades_nao_validas: tabela com dados de idade alterados pela mediana
        :return: pl.DataFrame -> tabela completa
        """
        tabela_resultado = pl.concat(
            [
                tb_idades_validas,
                tb_idades_nao_validas.with_columns(pl.col('idade').cast(pl.Int64))
            ]
        )

        return tabela_resultado


    def executar(self):
        """
        Rotina de tratamento da coluna de idade
        :return: pl.DataFrame
        """
        tabela_idades_validas = self.filter_idades_validas()
        tabela_idades_nao_validas = self.filter_idades_nao_validas()
        return self.tabela_completa(
            tb_idades_validas=tabela_idades_validas,
            tb_idades_nao_validas=tabela_idades_nao_validas
        )
