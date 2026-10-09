import polars as pl


class SubRotinasCamada:

    @staticmethod
    def selecionar_colunas_entrada(tabela: pl.DataFrame) -> pl.DataFrame:
        """
        Seleciona as colunas, removendo a ultima coluna, sabendo que esta coluna é uma coluna de data de atualizacao
        do dataframe de entrada
        :param tabela: pl.DataFrame
        :return: pl.DataFrame
        """
        tabela = tabela.select(tabela.columns[:-1])

        return tabela
