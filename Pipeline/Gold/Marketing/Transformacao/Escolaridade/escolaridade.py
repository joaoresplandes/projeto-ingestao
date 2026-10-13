import polars as pl


class TransformEscolaridade:
    def __init__(self, tabela: pl.DataFrame):
        self.__tabela = tabela


    def filtrar_tabela_sem_vazios(self):
        """
        Filtra a tabela pela coluna 'escolaridade' com dados não nulos
        :return: pl.DataFrame com dados não null
        """
        tabela_filtro = self.__tabela.filter(~pl.col('desc_escolaridade').is_null())

        return tabela_filtro

    def obter_moda(self) -> str:
        """
        Retorna a moda da coluna de 'desc_escolaridade' que representa o escolaridade
        :return: 'Solteiro(a)'
        """
        moda = self.__tabela['desc_escolaridade'].mode()[0]

        return moda

    def filtrar_tabela_vazios(self) -> pl.DataFrame:
        """
        Filtra os dados da coluna 'desc_escolaridade' que representa o escolaridade como null e substituindo esses
        valores null pela moda da própria coluna
        :return: pl.DataFrame com as 'desc_escolaridade' alterada para a moda
        """
        tabela_filtrar = self.__tabela.filter(pl.col('desc_escolaridade').is_null())

        return tabela_filtrar.with_columns(pl.lit(self.obter_moda()).alias('desc_escolaridade'))

    @staticmethod
    def tabela_completa(tb_nao_vazio: pl.DataFrame, tb_vazio: pl.DataFrame) -> pl.DataFrame:
        """
        Realiza a concatenacao da tabela 'tb_nao_vazio' com os dados de 'desc_escolaridade' sem alteracao e da tabela
        'tb_vazio' alterados de vazio para a moda
        :param tb_nao_vazio: tabela com desc_escolaridade sem alteracao
        :param tb_vazio: tabela com dados de desc_escolaridade alterados pela moda
        :return: pl.DataFrame -> tabela completa
        """
        tabela_resultado = pl.concat(
            [
                tb_nao_vazio,
                tb_vazio
            ]
        )

        return tabela_resultado


    def executar(self) -> pl.DataFrame:
        """
        Retina de tratamento da coluna de escolaridade
        :return: pl.DataFrame tratado
        """
        tabela_nao_vazios = self.filtrar_tabela_sem_vazios()
        tabela_vazio = self.filtrar_tabela_vazios()

        return self.tabela_completa(tb_nao_vazio=tabela_nao_vazios, tb_vazio=tabela_vazio)