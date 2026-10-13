import polars as pl


class TransformUFS:
    def __init__(self, tabela: pl.DataFrame):
        self.__tabela = tabela


    def filtrar_tabela_nordeste(self) -> pl.DataFrame:
        """
        Filtra a tabela pela coluna 'regiao' com apenas os registros de 'Nordeste'
        :return: pl.DataFrame -> regiao == Nordeste
        """
        tabela = self.__tabela.filter(pl.col('regiao') == 'Nordeste')

        return tabela

    def obter_moda(self) -> str:
        """
        Retorna a moda da coluna de 'uf'
        :return: 'BA'
        """
        moda = self.__tabela['uf'].mode()[0]

        return moda

    def filtrar_tabela_nao_nordeste(self) -> pl.DataFrame:
        """
        Filtra as regiões que não são do nordeste e vazios, alterando seus valores de 'uf' para a moda de 'uf'
        :return: pl.DataFrame com as 'uf' alterada para a moda
        """
        tabela_filtrar = self.__tabela.filter(
            (pl.col('regiao') != 'Nordeste')
            |
            (pl.col('regiao').is_null())
        )

        return tabela_filtrar.with_columns(pl.lit(self.obter_moda()).alias('uf'))

    @staticmethod
    def tabela_completa(tb_nordeste: pl.DataFrame, tb_n_nordeste: pl.DataFrame) -> pl.DataFrame:
        """
        Realiza a concatenacao da tabela 'tb_nordeste' com os dados de 'ufs' de nordeste e da tabela 'tb_n_nordeste'
        que tiveram seus dados modificados'
        :param tb_nordeste: tabela com regiao nordeste
        :param tb_n_nordeste: tabela com demais regioes ou vazio
        :return: pl.DataFrame -> tabela completa
        """
        tabela_resultado = pl.concat(
            [
                tb_nordeste, # dados originais da regiao nordeste
                tb_n_nordeste # dados das demais regioes com a coluna 'uf' modificada
            ]
        )

        return tabela_resultado


    def executar(self) -> pl.DataFrame:
        """
        Retorna a tabela com os tratamentos de 'uf' realizados
        :return: pl.DataFrame tratado
        """
        tabela_nordeste = self.filtrar_tabela_nordeste()
        tabela_n_nordeste = self.filtrar_tabela_nao_nordeste()

        return self.tabela_completa(tb_nordeste=tabela_nordeste, tb_n_nordeste=tabela_n_nordeste)