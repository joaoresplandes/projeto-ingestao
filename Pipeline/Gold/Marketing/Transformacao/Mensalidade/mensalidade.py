import polars as pl


class TransformMensalidade:
    def __init__(self, tabela: pl.DataFrame):
        self.__tabela = tabela

    def determinar_outliers(self) -> pl.DataFrame | None:
        """
        Retorna a tabela filtrada com os registroa que apresentam valores em 'vlr_mensal' maior que 4500 conforme regra
        estipulada
        :return: pl.DataFrame | None
        """
        valores_outliers = self.__tabela.filter(pl.col('vlr_mensal') > 4500)
        if valores_outliers.shape[0] > 0:
            return valores_outliers
        else:
            return None

    def filtar_registros_nulos(self):
        """
        Filtra os registros que apresentam na coluna 'vlr_mensal' o valor null e/ou vos registroa que apresentam valores
        em 'vlr_mensal' maior que 4500 conforme regra estipulada
        :return: pl.DataFrame de valores nulos
        """
        valores_nulos = self.__tabela.filter(
            (pl.col('vlr_mensal').is_null())
            |
            (pl.col('vlr_mensal') > 4500)
        )
        if valores_nulos.shape[0] > 0:
            return valores_nulos
        else:
            return None

    def filtar_registros_nao_nulos(self) -> pl.DataFrame:
        """
        Filtra os registros que apresentam na coluna 'vlr_mensal' o valor preenchido e/ou vos registro que apresentam
        valores em 'vlr_mensal' abaixo de 4500 conforme regra estipulada
        :return: pl.DataFrame de valores nulos
        """
        valores_nao_nulos = self.__tabela.filter(
            (~pl.col('vlr_mensal').is_null())
            |
            (pl.col('vlr_mensal') <= 4500)
        )

        return valores_nao_nulos

    @staticmethod
    def renomear_colunas(tabela: pl.DataFrame) -> pl.DataFrame:
        """
        Remove a coluna 'vlr_mensal' que contem apenas os valores vazios e renomea a coluna 'vlr_mensal_right' para
        'vlr_mensal'
        :param tabela: pl.DataFrame
        :return: pl.DataFrame com colunas renomeadas
        """
        tabela = tabela.drop('vlr_mensal')
        tabela = tabela.rename({
            'vlr_mensal_right':'vlr_mensal'
        })

        return tabela

    def valores_vigentes(self) -> pl.DataFrame:
        """
        Cria uma tabela da média de valores de 'vlr_mensal' para cada uma das idades
        :return: pl.DataFrame
        """
        tabela_agrupada = self.__tabela.filter(
            pl.col('idade').is_not_null()
        ).group_by(['idade']).agg(
            pl.col('vlr_mensal').mean().round(0).cast(pl.Int64).alias('vlr_mensal')
        ).sort(by='idade')

        return tabela_agrupada

    def substituir_valores_nulos(self, tabela_vazios: pl.DataFrame):
        """
        Substitui os valores de 'vlr_mensal' para cada para 'idade' presente no registro
        :param tabela_vazios: tabela filtrada com 'vlr_mensal' igual a null
        :return: pl.DataFrame
        """
        tabela_tratada = tabela_vazios.join(
            self.valores_vigentes(),
            left_on='idade',
            right_on='idade',
            how='left'
        )
        tabela_tratada = self.renomear_colunas(tabela=tabela_tratada).select(tabela_vazios.columns)

        return tabela_tratada

    @staticmethod
    def tabela_completa(tb_n_vazias: pl.DataFrame, tb_vazias: pl.DataFrame) -> pl.DataFrame:
        """
        Realiza a concatenacao da tabela 'tb_n_vazias' que contem os vlr_mensal preenchidos, com a tabela
        'tb_ivazias' que sofreram alterações em sesu registros de vlr_mensal
        :param tb_n_vazias: tabela com vlr_mensal sem alteracao
        :param tb_vazias: tabela com dados de vlr_mensal preenchidos pela média por idade
        """
        tabela_resultado = pl.concat(
            [
                tb_n_vazias,
                tb_vazias
            ]
        )

        return tabela_resultado

    def executar(self) -> pl.DataFrame:
        """
        Rotina de tratamento da coluna 'vlr_mensal'
        :return: pl.DataFrame
        """
        tabela_vazios = self.filtar_registros_nulos()
        if tabela_vazios is not None:
            tabela = self.substituir_valores_nulos(tabela_vazios=tabela_vazios)
            return self.tabela_completa(
                tb_n_vazias=self.filtar_registros_nao_nulos(),
                tb_vazias=tabela
            ).sort(by='id')
        else:
            return self.__tabela
