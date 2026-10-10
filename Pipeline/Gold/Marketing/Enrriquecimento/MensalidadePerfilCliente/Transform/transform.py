import polars as pl


class Transform:

    @staticmethod
    def arredondamento(valor: float | int) -> int:
        """
        Arredonda o 'valor' caso tenha casas decimais e transforma em um tipo int
        :param valor: 550.02
        :return: 550
        """
        return int(round(valor, 0))


    @staticmethod
    def tratar_coluna_decimal(tabela: pl.DataFrame, nm_coluna: str):
        """
        Realiza o processo de arredondamento para a 'nm_coluna' informada
        :param tabela: pl.DataFrame
        :param nm_coluna: nome da coluna -> vlr_mensal
        :return: pl.DataFrame
        """
        tabela = tabela.with_columns(
            pl.col(nm_coluna)
            .map_elements(Transform.arredondamento, return_dtype=pl.Int64)
        )
        return tabela

    @staticmethod
    def filtrar_colunas(tabela: pl.DataFrame) -> pl.DataFrame:
        """
        Filtra as colunas do dataframe para retorna 'id', 'vlr_mensal', 'vlr_coparticipacao'
        :param tabela: pl.DataFrame com todas as colunas
        :return: pl.DataFrame com apenas as colunas -> 'id', 'vlr_mensal', 'vlr_coparticipacao'
        """

        tabela = tabela.select(
            [
                'id',
                'vlr_mensal',
                'vlr_coparticipacao'
            ]
        )

        return tabela