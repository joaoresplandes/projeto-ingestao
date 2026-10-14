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

    @staticmethod
    def renomear_colunas(tabela: pl.DataFrame) -> pl.DataFrame:
        """
        Renomea as seguintes colunas:
        'dsc_ec' -> 'estado_civil',
        'desc_escolaridade' -> 'escolaridade',
        'vlr_mensal' -> 'mensalidade',
        'vlr_coparticipacao' -> 'participacao'
        :param tabela: pl.DataFrame
        :return: pl.DataFrame com colunas renomeadas
        """
        tabela = tabela.rename(
            {
                'dsc_ec':'estado_civil',
                'desc_escolaridade': 'escolaridade',
                'vlr_mensal':'mensalidade',
                'vlr_coparticipacao':'participacao'
            }
        )

        return tabela

    @staticmethod
    def colunas_finais_transformacao(tabela: pl.DataFrame) -> pl.DataFrame:
        """
        Define quais são as colunas finais que seram armazenadas no banco de dados na cama gold
        :param tabela: pl.DataFrame
        :return: pl.DataFrame
        """
        tabela = tabela.select(
            [
                'id',
                'genero',
                'idade',
                'uf',
                'indcliente',
                'ano_mes',
                'dsc_ec',
                'desc_escolaridade',
                'vlr_mensal',
                'vlr_coparticipacao'
            ]
        )
        return SubRotinasCamada.renomear_colunas(tabela=tabela)
