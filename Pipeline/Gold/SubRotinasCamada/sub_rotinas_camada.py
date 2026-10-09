import polars as pl


class SubRotinasCamada:

    @staticmethod
    def selecionar_colunas_entrada(tabela: pl.DataFrame) -> pl.DataFrame:
        tabela = tabela.select(tabela.columns[:-1])

        return tabela
